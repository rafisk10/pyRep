from django.db import models
from django.contrib.auth.models import User

FAIXA_SALARIAL_CHOICES = [
    (1, 'Até 1.000'),
    (2, 'De 1.000 a 2.000'),
    (3, 'De 2.000 a 3.000'),
    (4, 'Acima de 3.000'),
]

ESCOLARIDADE_CHOICES = [
    (1, 'Ensino Fundamental'),
    (2, 'Ensino Médio'),
    (3, 'Tecnólogo'),
    (4, 'Ensino Superior'),
    (5, 'Pós / MBA / Mestrado'),
    (6, 'Doutorado'),
]

class Empresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_empresa = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_empresa

class Candidato(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_candidato = models.CharField(max_length=100)
    faixa_salarial = models.IntegerField(choices=FAIXA_SALARIAL_CHOICES)
    escolaridade_minima = models.IntegerField(choices=ESCOLARIDADE_CHOICES)

    def __str__(self):
        return self.nome_candidato

class Vagas(models.Model):

    nome = models.CharField(max_length=100)
    faixa_salarial = models.IntegerField(choices=FAIXA_SALARIAL_CHOICES)
    escolaridade_minima = models.IntegerField(choices=ESCOLARIDADE_CHOICES)
    requisitos = models.TextField()
    empresa = models.ForeignKey(Empresa, related_name='vagas', on_delete=models.CASCADE)
    candidatosInscritos = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.nome
    
class Vagas_aplicadas(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vagas, related_name='Vagas_aplicadas', on_delete=models.CASCADE)
    pontuacao = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.candidato.nome_candidato} - {self.vaga.nome}'
    
    def save(self, *args, **kwargs):
        pontuacao = 0

        if self.vaga.faixa_salarial == self.candidato.faixa_salarial:
            pontuacao += 1

        if self.candidato.escolaridade_minima >= self.vaga.escolaridade_minima:
            pontuacao += 1

        self.pontuacao = pontuacao
        super(Vagas_aplicadas, self).save(*args, **kwargs)