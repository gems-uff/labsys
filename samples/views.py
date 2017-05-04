import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.core.urlresolvers import reverse

from .models import AdmissionNote
from .forms import (
    PatientForm, AdmissionNoteForm, FluVaccineForm, AdmissionNoteMultiForm,
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
    multi_form = AdmissionNoteMultiForm()

    if request.POST:
        return HttpResponseRedirect(reverse('samples:index'))
    else:
        return render(request, 'samples/admission_note_create.html',
            {
                'admission_note_form': multi_form,
            }
        )
