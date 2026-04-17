from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Veiculo(models.Model):
    modelo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    placa = models.CharField(max_length=20, unique=True)
    foto = models.ImageField(upload_to='veiculos/%Y/%m/%d/', blank=True, null=True)
    ano = models.IntegerField(
        default=2000, 
        validators=[MinValueValidator(1886), MaxValueValidator(2100)]
    )
    cor = models.CharField(max_length=100, null=True, blank=True)
    chassi = models.CharField(max_length=17, unique=True, null=True, blank=True) # Chassi tem 17 caracteres
    renavam = models.CharField(max_length=11, unique=True, null=True, blank=True) # CharField para manter zeros à esquerda
    versao = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f'{self.modelo} - {self.marca} - {self.placa}'

class Agendamento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Veículo')
    motorista = models.CharField(max_length=100)
    dataPartida = models.DateTimeField()
    dataChegada = models.DateTimeField()
    destino = models.TextField(blank=True)
    passageiros = models.IntegerField(default=1)
    
    def __str__(self):
        return f'{self.destino} - {self.motorista}'
    
    @property
    def vagas_restantes(self):
        # Útil para o sistema de reservas que você está desenvolvendo
        return 5 - self.passageiros

class Seguro(models.Model):
    # Agora o seguro está vinculado a um veículo
    veiculo = models.OneToOneField(Veiculo, on_delete=models.CASCADE, related_name='seguro_info')
    seguro = models.CharField(max_length=200)
    apolice = models.CharField(max_length=50) # Apolice também pode ter letras/zeros à esquerda
    inicio_vigencia = models.DateField()
    fim_vigencia = models.DateField()
    plano = models.CharField(max_length=200)

    def __str__(self):
        return f'Seguro: {self.seguro} - {self.veiculo.placa}'