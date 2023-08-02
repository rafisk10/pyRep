from django.urls import path

from . import views

urlpatterns = [
    path("vagas/", views.vagas, name="vagas"),
    path("detalhes_vaga/<int:vaga_id>", views.detalhes_vaga, name="detalhes_vaga"),
    path(
        "detalhes_vaga_empresas/<int:vaga_id>",
        views.detalhes_vaga_empresas,
        name="detalhes_vaga_empresas",
    ),
    path("aplica_vaga/<int:vaga_id>", views.aplica_vaga, name="aplica_vaga"),
    path("vagas_cadastradas/", views.vagas_cadastradas, name="vagas_cadastradas"),
    path("cad_vagas/", views.cad_vagas, name="cad_vagas"),
    path("edita_vaga/<int:vaga_id>", views.edita_vaga, name="edita_vaga"),
    path("deleta_vaga/<int:vaga_id>", views.deleta_vaga, name="deleta_vaga"),
    path("home/", views.home, name="home"),
]
