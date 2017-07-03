from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.forms import inlineformset_factory, formset_factory

from .models import AdmissionNote
from .forms import (
    AdmissionNoteForm,
    FluVaccineForm,
    ClinicalEvolutionForm,
    HospitalizationForm,
    UTIHospitalizationForm,
    AntiviralUseForm,
    XRayExamForm,
)
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
        # TODO: transfer this logic to the model
        # Only creates instances if symptom was not ignored
        if symptom_form.cleaned_data.get('observed') is not None:
            observed_symptom = ObservedSymptom(
                observed=symptom_form.cleaned_data.get('observed'),
                symptom=symptom_form.cleaned_data.get('symptom'),
                details=symptom_form.cleaned_data.get('details'),
                admission_note=admin_note,
            )
            new_obs_symptoms.append(observed_symptom)

    ObservedSymptom.objects.bulk_create(new_obs_symptoms)


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
    new_collected_samples = []
    for form in formset:
        if form.cleaned_data:
            print(form.cleaned_data)
            collected_sample = CollectedSample(
                collection_method = form.cleaned_data.get('collection_method'),
                collection_date = form.cleaned_data.get('collection_date'),
                details = form.cleaned_data.get('details'),
                admission_note=admin_note,
            )
            new_collected_samples.append(collected_sample)

    CollectedSample.objects.bulk_create(new_collected_samples)


def create_admission_note(request):
    #region Forms, Context and Template setup
    admission_note_form = AdmissionNoteForm(
        request.POST or None, prefix='admission_note',
        initial=utils.get_admission_note(dict=True, form=True),
    )
    patient_form = PatientForm(
        request.POST or None, prefix='patient_form',
        initial=utils.get_patient(dict=True, form=True),
    )
    residence_form = ResidenceForm(
        request.POST or None, prefix='residence_form',
        initial=utils.get_locality(dict=True, form=True),
    )
    observed_symptom_formset = ObservedSymptomFormSet(
        request.POST or None, prefix='observed_symptom',
        initial=Symptom.get_primary_symptoms_dict(),
    )
    secondary_symptoms_form = SecondarySymptomsForm(
        request.POST or None, prefix='secondary_symptoms',
    )
    collected_sample_formset = CollectedSampleFormSet(
        request.POST or None, prefix='collected_samples',
    )
    flu_vaccine_form = FluVaccineForm(
        request.POST or None, prefix='flu_vaccine',
    )
    clinical_evolution_form = ClinicalEvolutionForm(
        request.POST or None, prefix='clinical_evolution',
    )
    hospitalization_form = HospitalizationForm(
        request.POST or None, prefix='hospitalization',
    )
    uti_hospitalization_form = UTIHospitalizationForm(
        request.POST or None, prefix='uti_hospitalization'
    )
    antiviral_form = AntiviralUseForm(
        request.POST or None, prefix='antiviral_form',
    )
    xray_form = XRayExamForm(
        request.POST or None, prefix='xray_form',
    )

    forms = [
        patient_form,
        residence_form,
        admission_note_form,
        observed_symptom_formset,
        secondary_symptoms_form,
        collected_sample_formset,
        flu_vaccine_form,
        clinical_evolution_form,
        hospitalization_form,
        uti_hospitalization_form,
        antiviral_form,
        xray_form,
    ]
    context = {
        'forms': forms,
        'admission_note_form': admission_note_form,
        'patient_form': patient_form,
        'residence_form': residence_form,
        'observed_symptom_formset': observed_symptom_formset,
        'secondary_symptoms_form': secondary_symptoms_form,
        'collected_sample_formset': collected_sample_formset,
        'flu_vaccine_form': flu_vaccine_form,
        'clinical_evolution_form': clinical_evolution_form,
        'hospitalization_form': hospitalization_form,
        'uti_hospitalization_form': uti_hospitalization_form,
        'antiviral_form': antiviral_form,
        'xray_form': xray_form,
    }
    template = 'admission_notes/create.html'
    #endregion

    #region Request handling
    if request.POST:
        if utils.are_forms_valid(forms):
            try:
                with transaction.atomic():
                    residence = residence_form.save()
                    patient = patient_form.save(residence)
                    admin_note = admission_note_form.save(patient)
                    create_secondary_symptoms(
                        secondary_symptoms_form, admin_note
                    )
                    # TODO: check if saving the formset changes anything
                    # instead of using bulky create
                    create_observed_symptoms(
                        observed_symptom_formset, admin_note
                    )
                    create_collected_samples(
                        collected_sample_formset, admin_note
                    )
                    flu_vaccine_form.save(admin_note)
                    clinical_evolution_form.save(admin_note)
                    hospitalization_form.save(admin_note)
                    uti_hospitalization_form.save(admin_note)
                    antiviral_form.save(admin_note)
                    xray_form.save(admin_note)

                    # Notify our users
                    messages.success(request, "Registro criado com sucesso")

                    return HttpResponseRedirect(
                        reverse('admission_notes:index'))
            except IntegrityError:  # Transaction failed
                messages.error(request, "Erro ao salvar o registro")
        else:
            messages.error(request, "Por favor, corrigir campos abaixo")

    #endregion
    return render(request, template, context)
