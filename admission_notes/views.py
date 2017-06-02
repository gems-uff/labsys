from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.db import IntegrityError, transaction
from django.contrib import messages

from .models import AdmissionNote
from .forms import AdmissionNoteForm


class IndexView(generic.ListView):
    template_name = 'admission_notes/index.html'
    context_object_name = 'admission_notes_list'

    def get_queryset(self):
        return AdmissionNote.objects.all().order_by('id_gal')


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

def create_admission_note(request):
    admission_note_form = AdmissionNoteForm(
        request.POST or None, prefix='admission_note')

    forms = []
    forms.append(admission_note_form)

    if request.POST:
        if are_valid(forms):
            try:
                with transaction.atomic():
                    admission_note_form.save()

                    # Notify our users
                    messages.success(request, "Registro criado com sucesso")

                    return HttpResponseRedirect(
                        reverse('admission_notes:index'))
            except IntegrityError:  # Transaction failed
                messages.error(request, "Erro ao salvar o registro")


    return render(request, 'admission_notes/admission_note_create.html',
        {
            'admission_note_form': admission_note_form,
        }
    )
