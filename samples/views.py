import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.core.urlresolvers import reverse

from .models import AdmissionNote
from .forms import (
    PatientForm, AdmissionNoteForm, FluVaccineForm,
    CollectedSampleForm,
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


def create_admission_note(request):
    admission_note_form = AdmissionNoteForm(
        request.POST or None, prefix='admission_note')
    patient_form = PatientForm(
        request.POST or None, prefix='patient')
    flu_vaccine_form = FluVaccineForm(
        request.POST or None, prefix='flu_vaccine')
    collected_sample_form = CollectedSampleForm(
        request.POST or None, prefix='collected_sample')

    if request.POST:
        if admission_note_form.is_valid() \
                and patient_form.is_valid() \
                and flu_vaccine_form.is_valid() \
                and collected_sample_form.is_valid():
            patient = patient_form.save(commit=False)
            admission_note = admission_note_form.save(commit=False)

            # Effectively saves
            patient.save()
            admission_note.patient = patient
            admission_note.save()
            flu_vaccine_form.save_fk(admission_note)
            collected_sample_form.save_fk(admission_note)

            return HttpResponseRedirect(reverse('samples:index'))

    return render(request, 'samples/admission_note_create.html',
        {
            'admission_note_form': admission_note_form,
            'patient_form': patient_form,
            'flu_vaccine_form': flu_vaccine_form,
            'collected_sample_form': collected_sample_form,
        }
    )
