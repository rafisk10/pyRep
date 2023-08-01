from django.shortcuts import render,redirect
from .models import Vagas,Candidato,Empresa,Vagas_aplicadas
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

@login_required
def vagas(request):
    
    vagas_disponiveis = Vagas.objects.all()
    
    context = {"vagas": vagas_disponiveis}
    return render(request, 'vagas.html', context)

@login_required
def detalhes_vaga(request, vaga_id):
    vaga = Vagas.objects.filter(id = vaga_id).first()
    candidatos = Candidato.objects.filter(vagas_aplicadas__vaga_id = vaga_id).all() 

    context = {'vaga': vaga, 'candidatos': candidatos}
    
    return render(request, 'detalhes_vaga.html', context)

@login_required
def aplica_vaga(request, vaga_id):
   
    hasattr(request.user, 'candidato')
    candidato_id = request.user.candidato.id
    
    ja_aplicada = Vagas_aplicadas.objects.filter(candidato_id = candidato_id, vaga_id = vaga_id).first()
    vaga = Vagas.objects.filter(id = vaga_id).first()
    candidato = Candidato.objects.filter(id = candidato_id).first()
    context = {
        'candidato': candidato,
        'vaga': vaga,
    }
    
    if ja_aplicada:
        context['mensagem'] = 'Você já aplicou para esta vaga!'
    else:
        vaga_aplicada = Vagas_aplicadas.objects.create(candidato=candidato, vaga=vaga)
        vaga_aplicada.save()
        context['mensagem'] = 'Inscrição confirmada!'
        context['pontuacao'] = vaga_aplicada.pontuacao

    return render(request, 'detalhes_vaga.html', context)
    
@login_required
def vagas_cadastradas(request):
    
    hasattr(request.user, 'empresa')
    empresa_id = request.user.empresa.id
    
    vagas = Vagas.objects.filter(vagas__empresa_id = empresa_id).all()
    
    
    
    context = {'vagas': vagas}
    return(request, 'vagas_cadastradas.html', context)