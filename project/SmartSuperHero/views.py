import subprocess

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from SmartSuperHero.models import Patient, Doctor, Report, Question


@login_required
def SuperHeroListView(request):
    m_filter = Patient.objects.filter(doctor__first_name=request.user)

    return render(request, "../templates/SmartSuperHero/patient_list.html", {
        'object_list': m_filter
    })


@login_required
def PatientDetail(requst, pk):
    m_filter = Report.objects.filter(patient__pk=pk)
    my_pk = 0
    if m_filter.count() != 0:
        my_pk = m_filter[0].patient.pk
    return render(requst, '../templates/SmartSuperHero/patient_detail.html', {
        'reports': m_filter,
        'first': my_pk,
    })


class AddQuestion(LoginRequiredMixin, CreateView):
    model = Question
    template_name = '../templates/SmartSuperHero/question_form.html'
    fields = (
        'question',
    )


    def dispatch(self, request, *args, **kwargs):
        self.patient = get_object_or_404(Patient, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.patient = self.patient
        form.instance.answer = ""
        return super().form_valid(form)


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    template_name = "../templates/SmartSuperHero/t1.html"
    fields = (
        'first_name',
        'last_name',
        'patient_id',
        'diagnosis',
        'birthday',
        'parent_fullname',
    )
    success_url = reverse_lazy("SmartSuperHero:list")

    def form_valid(self, form):
        form.instance.doctor = Doctor.objects.filter(first_name=self.request.user)[0]
        return super().form_valid(form)


class CaptureView(LoginRequiredMixin, View):

    def post(self):
        subprocess.run("python FacialRecognition/01_face_dataset.py 1")
        return redirect(reverse_lazy("SmartSuperHero:list",))
