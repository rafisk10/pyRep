from django.contrib import admin
from .models import Vagas, Empresa, Candidato, Vagas_aplicadas


# Register your models here.


class vagaAdmin(admin.ModelAdmin):
    fields = [
        "nome",
        "faixa_salarial",
        "escolaridade_minima",
        "requisitos",
        "empresa",
        "candidatosInscritos",
    ]


class empresaAdmin(admin.ModelAdmin):
    fields = ["user", "nome_empresa"]


class candidatoAdmin(admin.ModelAdmin):
    fields = ["user", "nome_candidato", "faixa_salarial", "escolaridade_minima"]


class vagas_aplicadasAdmin(admin.ModelAdmin):
    fields = ["candidato", "vaga", "pontuacao"]


admin.site.register(Empresa, empresaAdmin)
admin.site.register(Vagas, vagaAdmin)
admin.site.register(Candidato, candidatoAdmin)
admin.site.register(Vagas_aplicadas, vagas_aplicadasAdmin)
