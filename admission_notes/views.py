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
from symptoms.forms import ObservedSymptomForm


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


def get_initial_admission_note():
    admin_note = AdmissionNote.objects.all().first()

    return {
        'id_gal': admin_note.id_gal,
        'requester': admin_note.requester,
        'health_unit': admin_note.health_unit,
        'state': admin_note.state,
        'city': admin_note.city,
        'admission_date': admin_note.admission_date,
        'patient': admin_note.patient,
    }


ObservedSymptomFormSet = formset_factory(
    ObservedSymptomForm,
    extra=0,
)
def create_admission_note(request):

    admission_note_form = AdmissionNoteForm(
        initial=get_initial_admission_note()
        # request.POST or None, prefix='admission_note')
    )
    admin_note = AdmissionNote.objects.all().first()

    observed_symptom_formset = ObservedSymptomFormSet(
        request.POST or None, prefix='observed_symptom',
        initial=ObservedSymptom.get_primary_symptoms_dict(),
    )

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

        else:
            print(admission_note_form.errors)


    return render(request, 'admission_notes/create.html',
        {
            'admission_note_form': admission_note_form,
            'observed_symptom_formset': observed_symptom_formset,
        }
    )
