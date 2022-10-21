from django.db import models


class Voos(models.Model):
    STATUS_CHOICES = (
        ('embarcando', 'embarcando'), 
        ('cancelado', 'cancelado'), 
        ('programado', 'programado'), 
        ('taxiando', 'taxiando'), 
        ('pronto', 'pronto'), 
        ('autorizado', 'autorizado'), 
        ('em voo', 'em voo'), 
        ('aterrissado', 'aterrissado'),
    )

    companhia_aerea = models.CharField(max_length=100, blank=False)
    codigo = models.CharField(max_length=6, blank=False)  # codigo precisa ser 2 letras e 4 números (XX1111)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    origem = models.CharField(max_length=100, blank=False)
    destino = models.CharField(max_length=100, blank=False)
    partida_prevista = models.DateTimeField(blank=False)
    chegada_prevista = models.DateTimeField(blank=False)
    partida_real = models.DateTimeField(blank=True, null=True)
    chegada_real = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'voos'


class Partidas(models.Model):
    STATUS_CHOICES = (
        ('embarcando', 'embarcando'), 
        ('cancelado', 'cancelado'), 
        ('programado', 'programado'), 
        ('taxiando', 'taxiando'), 
        ('pronto', 'pronto'), 
        ('autorizado', 'autorizado'), 
        ('em voo', 'em voo'), 
        ('aterrissado', 'aterrissado'),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    destino = models.CharField(max_length=100, blank=False)
    partida_prevista = models.DateTimeField(blank=False)
    partida_real = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'partidas'


class Chegadas(models.Model):
    origem = models.CharField(max_length=100, blank=False)
    chegada_prevista = models.DateTimeField(blank=False)
    chegada_real = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'chegadas'
