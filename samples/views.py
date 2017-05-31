from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.core.urlresolvers import reverse
from django.forms import formset_factory, modelformset_factory
from django.db import IntegrityError, transaction
from django.contrib import messages

from .models import AdmissionNote, CollectedSample, ObservedSymptom, Symptom
from .forms import (
    PatientForm, AdmissionNoteForm, FluVaccineForm,
    CollectedSampleForm, BaseCollectedSampleFormSet,
    ObservedSymptomForm, BaseObservedSymptomFormSet,
)


class IndexView(generic.ListView):
    template_name = 'samples/index.html'
    context_object_name = 'admission_note_list'

    def get_queryset(self):
        return AdmissionNote.objects.all()


class DetailView(generic.DetailView):
    template_name = 'samples/detail.html'
    context_object_name = 'admission_note'

    def get_queryset(self):
        return AdmissionNote.objects.all()

ObservedSymptomFormSet = formset_factory(
    ObservedSymptomForm,
    formset=BaseObservedSymptomFormSet,
    extra=0,
)

CollectedSampleFormSet = formset_factory(
    CollectedSampleForm,
    formset=BaseCollectedSampleFormSet
)

def create_admission_note(request):
    admission_note_form = AdmissionNoteForm(
        request.POST or None, prefix='admission_note')
    patient_form = PatientForm(
        request.POST or None, prefix='patient')
    flu_vaccine_form = FluVaccineForm(
        request.POST or None, prefix='flu_vaccine')

    observed_symptom_formset = ObservedSymptomFormSet(
        request.POST or None, prefix='observed_symptom',
        initial=ObservedSymptom.get_primary_symptoms_dict(),
    )
    collected_sample_formset = CollectedSampleFormSet(
        request.POST or None, prefix='collected_sample')


    if request.POST:
        if admission_note_form.is_valid() \
                and patient_form.is_valid() \
                and flu_vaccine_form.is_valid() \
                and collected_sample_formset.is_valid() \
                and observed_symptom_formset.is_valid():
            patient = patient_form.save(commit=False)
            admission_note = admission_note_form.save(commit=False)

            # Effectively saves only if everything is fine
            patient.save()
            admission_note.patient = patient
            admission_note.save()
            flu_vaccine_form.save_fk(admission_note)
            #observed_symptom_form.save_fk(admission_note)

            # Create all CollectedSample objects (do not persist yet)
            new_samples = []
            for sample_form in collected_sample_formset:
                collection_type = sample_form.cleaned_data.get(
                    'collection_type')
                collection_date = sample_form.cleaned_data.get(
                    'collection_date')

                if collection_type and collection_date:
                    collected_sample = CollectedSample(
                        collection_type=collection_type,
                        collection_date=collection_date,
                        admission_note=admission_note,
                    )
                    new_samples.append(collected_sample)

            # Persist in a transaction
            try:
                with transaction.atomic():
                    # If we want, replace old with new
                    # CollectedSample.objects.filter(admission_note=admission_note).delete()
                    CollectedSample.objects.bulk_create(new_samples)

                    # Notify our users
                    messages.success(request, "Registro criado com sucesso")

                    return HttpResponseRedirect(reverse('samples:index'))
            except IntegrityError:  # Transaction failed
                messages.error(request, "Erro ao salvar o registro")

    return render(request, 'samples/admission_note_create.html',
        {
            'admission_note_form': admission_note_form,
            'patient_form': patient_form,
            'flu_vaccine_form': flu_vaccine_form,
            'collected_sample_formset': collected_sample_formset,
            #'observed_symptom_form': observed_symptom_form,
            'observed_symptom_formset': observed_symptom_formset,
        }
    )
