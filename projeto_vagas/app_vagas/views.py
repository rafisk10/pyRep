from django.shortcuts import render, redirect
from .models import (
    Vagas,
    Candidato,
    Empresa,
    Vagas_aplicadas,
    ESCOLARIDADE_CHOICES,
    FAIXA_SALARIAL_CHOICES,
)
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect


def home(request):
    return render(request, "home.html")


def vagas(request):
    context = {}

    vagas_disponiveis = Vagas.objects.all()

    if vagas_disponiveis:
        context = {"vagas": vagas_disponiveis}
        return render(request, "vagas.html", context)
    else:
        context["aviso"] = " Não ha vagas cadastradas ainda"
        return render(request, "vagas.html", context)


def detalhes_vaga(request, vaga_id):
    vaga = Vagas.objects.filter(id=vaga_id).first()
    candidatos = Candidato.objects.filter(vagas_aplicadas__vaga_id=vaga_id).all()
    context = {"vaga": vaga, "candidatos": candidatos}

    if request.user.is_authenticated:
        return render(request, "detalhes_vaga.html", context)
    else:
        context[
            "mensagem"
        ] = "Você deve estar logado pra visualizar os detalhes das vagas"
        return render(request, "vagas.html", context)


@login_required
def aplica_vaga(request, vaga_id):
    hasattr(request.user, "candidato")
    candidato_id = request.user.candidato.id

    ja_aplicada = Vagas_aplicadas.objects.filter(
        candidato_id=candidato_id, vaga_id=vaga_id
    ).first()
    vaga = Vagas.objects.filter(id=vaga_id).first()
    candidato = Candidato.objects.filter(id=candidato_id).first()
    context = {
        "candidato": candidato,
        "vaga": vaga,
    }

    if ja_aplicada:
        context["mensagem"] = "Você já aplicou para esta vaga!"
    else:
        pontuacao = 0

        if int(vaga.faixa_salarial >= candidato.faixa_salarial):
            pontuacao += 1
        if int(candidato.escolaridade_minima >= vaga.escolaridade_minima):
            pontuacao += 1

        vaga_aplicada = Vagas_aplicadas.objects.create(
            candidato=candidato, vaga=vaga, pontuacao=pontuacao
        )
        vaga_aplicada.save()
        context["mensagem"] = "Inscrição confirmada!"
        context["pontuacao"] = vaga_aplicada.pontuacao

    return render(request, "detalhes_vaga.html", context)


@login_required
def detalhes_vaga_empresas(request, vaga_id):
    vaga = Vagas.objects.filter(id=vaga_id).first()
    candidatos = Candidato.objects.filter(vagas_aplicadas__vaga_id=vaga_id).all()

    for candidato in candidatos:
        pontuacao = (
            Vagas_aplicadas.objects.filter(candidato=candidato, vaga=vaga)
            .aggregate(Sum("pontuacao"))
            .get("pontuacao__sum")
        )
        candidato.pontuacao = pontuacao

    context = {"vaga": vaga, "candidatos": candidatos}
    return render(request, "detalhes_vaga_empresas.html", context)


@login_required
def cad_vagas(request):
    hasattr(request.user, "empresa")
    empresa_id = request.user.empresa.id

    tem_vagas = Vagas.objects.filter(empresa_id=empresa_id).all()

    context = {
        "faixa_salarial_choices": FAIXA_SALARIAL_CHOICES,
        "escolaridade_choices": ESCOLARIDADE_CHOICES,
        "vagas": tem_vagas,
    }
    if request.method == "GET":
        return render(request, "cad_vagas.html", context)
    else:
        vaga_nome = request.POST.get("nome")
        faixa_salarial = request.POST.get("faixa_salarial")
        escolaridade_minima = request.POST.get("escolaridade_minima")
        requisitos = request.POST.get("requisitos")
        empresa = Empresa.objects.filter(id=empresa_id).first()

        vaga = Vagas.objects.create(
            empresa=empresa,
            nome=vaga_nome,
            faixa_salarial=faixa_salarial,
            escolaridade_minima=escolaridade_minima,
            requisitos=requisitos,
        )
        vaga.save()
        return HttpResponseRedirect(reverse("vagas_cadastradas"))


@login_required
def edita_vaga(request, vaga_id):
    hasattr(request.user, "empresa")
    empresa_id = request.user.empresa.id

    vaga = Vagas.objects.filter(id=vaga_id).first()
    context = {
        "vaga": vaga,
        "faixa_salarial_choices": FAIXA_SALARIAL_CHOICES,
        "escolaridade_choices": ESCOLARIDADE_CHOICES,
    }
    if request.method == "GET":
        return render(request, "edita_vaga.html", context)
    else:
        vaga.nome = request.POST["nome"]
        vaga.faixa_salarial = request.POST["faixa_salarial"]
        vaga.escolaridade_minima = request.POST["escolaridade_minima"]
        vaga.requisitos = request.POST["requisitos"]
        vaga.empresa = Empresa.objects.filter(id=empresa_id).first()
        vaga.save()
        return redirect("detalhes_vaga_empresas", vaga_id=vaga.id)


@login_required
def deleta_vaga(request, vaga_id):
    aviso = ""
    vaga = Vagas.objects.filter(id=vaga_id).first()
    context = {"vaga": vaga, "aviso": aviso}

    if vaga:
        vaga.delete()
        return HttpResponseRedirect(reverse("vagas_cadastradas"))
    else:
        aviso = "Erro ao excluir a vaga"
        return render(request, "detalhes_vaga_empresas.html", context)


@login_required
def vagas_cadastradas(request):
    hasattr(request.user, "empresa")
    empresa_id = request.user.empresa.id

    vagas = Vagas.objects.filter(empresa_id=empresa_id).all()

    if vagas:
        context = {"vagas": vagas}
        return render(request, "vagas_cadastradas.html", context)
    else:
        context = {}
        return HttpResponseRedirect(reverse("cad_vagas"))
