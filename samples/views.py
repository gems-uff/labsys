import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.core.urlresolvers import reverse

from .models import AdmissionNote
from .forms import PatientForm, AdmissionNoteForm, FluVaccineForm


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
    admission_note_form = AdmissionNoteForm(request.POST or None, prefix='admission_note')
    patient_form = PatientForm(request.POST or None, prefix='patient')
    flu_vaccine_form = FluVaccineForm(request.POST or None, prefix='flu_vaccine')

    if request.POST:
        if admission_note_form.is_valid() \
                and patient_form.is_valid() \
                and flu_vaccine_form.is_valid():
            admission_note = admission_note_form.save(commit=False)
            admission_note.patient = patient_form.save()
            admission_note.save()
            flu_vaccine = flu_vaccine_form.save(commit=False)
            flu_vaccine.admission_note = admission_note
            flu_vaccine.save()

            return HttpResponseRedirect(reverse('samples:index'))

    return render(request, 'samples/admission_note_create.html',
        {
            'admission_note_form': admission_note_form,
            'patient_form': patient_form,
            'flu_vaccine_form': flu_vaccine_form,
        }
    )
