from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.forms import inlineformset_factory, formset_factory

from .models import AdmissionNote
from .forms import AdmissionNoteForm
from symptoms.models import ObservedSymptom, Symptom
from symptoms.forms import ObservedSymptomFormSet, SecondarySymptomsForm
from patients.models import Patient, Locality
from patients.forms import PatientForm, ResidenceForm


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


def are_valid(forms):
    for form in forms:
        if not form.is_valid():
            return False
    return True


def get_initial_admission_note():

    return {
        'id_request_gal': 'teste_gal',
        'id_lvrs_intern': '334/2017',
        'requester': 'teste requestes',
        'health_unit': 'teste health unit',
        'state': 'rj',
        'city': 'niteroi',
        'admission_date': '20-12-2012',
        'details': 'Teste de details'
    }


def get_initial_patient():
    return {
        'name': 'Nome de Teste dos Santos',
        'birth_date': '19/12/1994',
        'age': 12,
        'age_unit': 'A',
        'gender': 'M',
        'pregnant': 6,
    }


def get_initial_residence():
    return {
        'country': 1,
        'state': 'RJ',
        'city': 'Niteroi',
        'neighborhood': 'Icarai',
        'zone': 9,
    }


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


def create_admission_note(request):

    patient_form = PatientForm(
        request.POST or None, prefix='patient_form',
        initial=get_initial_patient(),
    )
    residence_form = ResidenceForm(
        request.POST or None, prefix='residence_form',
        initial=get_initial_residence(),
    )

    admission_note_form = AdmissionNoteForm(
        request.POST or None, prefix='admission_note',
        initial=get_initial_admission_note(),
    )

    observed_symptom_formset = ObservedSymptomFormSet(
        request.POST or None, prefix='observed_symptom',
        initial=Symptom.get_primary_symptoms_dict(),
    )

    secondary_symptoms_form = SecondarySymptomsForm(
        request.POST or None, prefix='secondary_symptoms',
    )

    forms = []
    forms.append(patient_form)
    forms.append(residence_form)
    forms.append(admission_note_form)
    forms.append(observed_symptom_formset)
    forms.append(secondary_symptoms_form)

    if request.POST:
        if are_valid(forms):
            try:
                with transaction.atomic():
                    residence = residence_form.save()
                    patient = patient_form.save(residence)
                    admin_note = admission_note_form.save(patient)
                    new_obs_symptoms = create_observed_symptoms(
                        observed_symptom_formset, admin_note)
                    ObservedSymptom.objects.bulk_create(new_obs_symptoms)

                    create_secondary_symptoms(
                        secondary_symptoms_form, admin_note)

                    # Notify our users
                    messages.success(request, "Registro criado com sucesso")

                    return HttpResponseRedirect(
                        reverse('admission_notes:index'))
            except IntegrityError:  # Transaction failed
                messages.error(request, "Erro ao salvar o registro")

        else:
            print(admission_note_form.errors)


    return render(request, 'admission_notes/create.html',
        {
            'patient_form': patient_form,
            'residence_form': residence_form,
            'admission_note_form': admission_note_form,
            'observed_symptom_formset': observed_symptom_formset,
            'secondary_symptoms_form': secondary_symptoms_form,
        }
    )
