from django.contrib.auth import logout as logout_user
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.urls import reverse
from app_vagas.models import (
    Candidato,
    Empresa,
    ESCOLARIDADE_CHOICES,
    FAIXA_SALARIAL_CHOICES,
)


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST.get("username")
        senha = request.POST.get("password")

        user = authenticate(username=username, password=senha)

        if user:
            login_django(request, user)
            candidato = hasattr(request.user, "candidato")
            if candidato:
                return redirect(reverse("vagas"))
            else:
                return redirect(reverse("vagas_cadastradas"))
        else:
            return render(
                request, "login.html", {"error_message": "Usuário ou senha inválidos"}
            )


def logout_view(request):
    logout_user(request)
    return redirect("login")


def cadastro(request):
    context = {
        "faixa_salarial_choices": FAIXA_SALARIAL_CHOICES,
        "escolaridade_choices": ESCOLARIDADE_CHOICES,
    }
    if request.method == "GET":
        return render(request, "cadastro.html", context)
    else:
        email = request.POST.get("email")
        nome = request.POST.get("first_name")
        senha = request.POST.get("password")
        sobrenome = request.POST.get("last_name")
        faixa_salarial_escolhida = request.POST.get("faixa_salarial")
        escolaridade_minima_escolhida = request.POST.get("escolaridade_minima")

        user = User.objects.filter(username=email).first()
        if user:
            context["aviso"] = "Usuario ja cadastrado"
            return render(request, "cadastro.html", context)

        if sobrenome is None:
            nome_empresa = request.POST.get("nome_empresa")
            user = User.objects.create_user(username=email, email=email, password=senha)
            empresa = Empresa.objects.create(user=user, nome_empresa=nome_empresa)
            empresa.save()
            return HttpResponseRedirect(reverse("login"))
        else:
            sobrenome = request.POST.get("last_name")
            nome_candidato = nome + " " + sobrenome
            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=nome,
                last_name=sobrenome,
                password=senha,
            )
            candidato = Candidato.objects.create(
                user=user,
                nome_candidato=nome_candidato,
                faixa_salarial=faixa_salarial_escolhida,
                escolaridade_minima=escolaridade_minima_escolhida,
            )
            candidato.save()

            return HttpResponseRedirect(reverse("login"))
