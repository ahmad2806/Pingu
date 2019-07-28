from django.urls import path

from SmartSuperHero.views import SuperHeroListView, PatientCreateView, PatientDetail, AddQuestion, CaptureView

app_name = "SmartSuperHero"

urlpatterns = [
    path('', SuperHeroListView, name="list"),
    path('add/', PatientCreateView.as_view(), name="add"),
    path('details/<int:pk>/', PatientDetail, name="detail"),
    path('add/question/<int:pk>/', AddQuestion.as_view(), name="question"),
    path('capture/', CaptureView.as_view(), name="capture"),
]
