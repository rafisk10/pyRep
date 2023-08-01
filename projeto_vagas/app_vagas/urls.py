from django.urls import path

from . import views

urlpatterns = [
    path("vagas/", views.vagas, name="vagas"),
    path("detalhes_vaga/<vaga_id>", views.detalhes_vaga, name = 'detalhes_vaga'),
    path("aplica_vaga/<int:vaga_id>", views.aplica_vaga, name = 'aplica_vaga')
    
]