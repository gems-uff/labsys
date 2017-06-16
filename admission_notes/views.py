from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.forms import inlineformset_factory, formset_factory

from .models import AdmissionNote
from .forms import AdmissionNoteForm
import admission_notes.utils as utils
from symptoms.models import ObservedSymptom, Symptom
from symptoms.forms import ObservedSymptomFormSet, SecondarySymptomsForm
from patients.forms import PatientForm, ResidenceForm
from collected_sample.forms import CollectedSampleFormSet
from collected_sample.models import CollectedSample


class IndexView(generic.ListView):
    template_name = 'admission_notes/index.html'
    context_object_name = 'admission_notes_list'

    def get_queryset(self):
        return AdmissionNote.objects.all().order_by('id_lvrs_intern')


class DetailView(generic.DetailView):
    model = AdmissionNote
    template_name = 'admission_notes/detail.html'
    context_object_name = 'admission_note'

    def get_queryset(self):
        return AdmissionNote.objects.all()


def create_observed_symptoms(formset, admin_note):
    new_obs_symptoms = []
    for symptom_form in formset:
        # Only creates instances if symptom was not ignored
        if symptom_form.cleaned_data.get('observed') is not None:
            observed_symptom = ObservedSymptom(
                observed=symptom_form.cleaned_data.get('observed'),
                symptom=symptom_form.cleaned_data.get('symptom'),
                details=symptom_form.cleaned_data.get('details'),
                admission_note=admin_note,
            )
            new_obs_symptoms.append(observed_symptom)

    return new_obs_symptoms


def create_secondary_symptoms(form, admin_note):
    for obs_symptom in form.cleaned_data['symptoms']:
        observed_symptom = ObservedSymptom(
            observed=True,
            symptom=obs_symptom,
            details=form.cleaned_data['details'],
            admission_note=admin_note,
        )
        observed_symptom.save()


def create_collected_samples(formset, admin_note):
    for form in formset:
        collected_sample = CollectedSample(
            collection_method = form.cleaned_data.get('collection_method'),
            collection_date = form.cleaned_data.get('collection_date'),
            admission_note=admin_note,
        )
        collected_sample.save()


def create_admission_note(request):
    ### SETUP
    admission_note_form = AdmissionNoteForm(
        request.POST or None, prefix='admission_note',
        initial=utils.get_admission_note(dict=True),)
    patient_form = PatientForm(
        request.POST or None, prefix='patient_form',
        initial=utils.get_patient(dict=True),)
    residence_form = ResidenceForm(
        request.POST or None, prefix='residence_form',
        initial=utils.get_residence(dict=True),)
    observed_symptom_formset = ObservedSymptomFormSet(
        request.POST or None, prefix='observed_symptom',
        initial=Symptom.get_primary_symptoms_dict(),)
    secondary_symptoms_form = SecondarySymptomsForm(
        request.POST or None, prefix='secondary_symptoms',)
    collected_sample_formset = CollectedSampleFormSet(
        request.POST or None, prefix='collected_sample')

    forms = [
        patient_form,
        residence_form,
        admission_note_form,
        observed_symptom_formset,
        secondary_symptoms_form,
        collected_sample_formset,
    ]
    context = {
        'admission_note_form': admission_note_form,
        'patient_form': patient_form,
        'residence_form': residence_form,
        'observed_symptom_formset': observed_symptom_formset,
        'secondary_symptoms_form': secondary_symptoms_form,
        'collected_sample_formset': collected_sample_formset,
    }
    template = 'admission_notes/create.html'

    # LOGIC
    if request.POST:
        if utils.are_forms_valid(forms):
            try:
                with transaction.atomic():
                    residence = residence_form.save()
                    patient = patient_form.save(residence)
                    admin_note = admission_note_form.save(patient)
                    # TODO: check if saving the formset changes anything
                    new_obs_symptoms = create_observed_symptoms(
                        observed_symptom_formset, admin_note)
                    ObservedSymptom.objects.bulk_create(new_obs_symptoms)
                    create_secondary_symptoms(
                        secondary_symptoms_form, admin_note)
                    collected_samples = create_collected_samples(
                        collected_sample_formset, admin_note)

                    # Notify our users
                    messages.success(request, "Registro criado com sucesso")

                    return HttpResponseRedirect(
                        reverse('admission_notes:index'))
            except IntegrityError:  # Transaction failed
                messages.error(request, "Erro ao salvar o registro")

        else:
            print(admission_note_form.errors)

    return render(request, template, context)
