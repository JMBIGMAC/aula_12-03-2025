from django.db import models
from django.core.exceptions import ValidationError
import re

# CPF Validator
def validate_cpf(value):
    if not re.match(r'\d{11}$', value):
        raise ValidationError('CPF must contain exactly 11 digits.')

# Phone Validator
def validate_phone(value):
    if not re.match(r'^\(\d{2}\) \d{4,5}-\d{4}$', value):
        raise ValidationError('Phone number must be in the format (XX) XXXXX-XXXX.')

class Responsavel(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Nome do responsável")
    last_name = models.CharField(max_length=50, verbose_name="Sobrenome do responsável")
    phone_number = models.CharField(max_length=15, verbose_name="Nº do celular (--) ---- ---- do responsável", validators=[validate_phone])
    email = models.CharField(max_length=100, verbose_name="Email do responsável")
    address = models.CharField(max_length=100, verbose_name="Endereço do responsável")
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF do responsável", validators=[validate_cpf])
    birthday = models.DateField()

    def __str__(self):
        return self.first_name

class Aluno(models.Model):
    TURMA_CHOICES = (
        ("1A", "1º Ano A"),
        ("1B", "1º Ano B"),
        ("1C", "1º Ano C"),
        ("2A", "2º Ano A"),
        ("2B", "2º Ano B"),
        ("2C", "2º Ano C"),
        ("3A", "3º Ano A"),
        ("3B", "3º Ano B"),
        ("3C", "3º Ano C"),
    )
    registration_number = models.AutoField(primary_key=True, verbose_name="Número de Registro")
    full_name = models.CharField(max_length=100, verbose_name="Nome Completo")
    phone_number_aluno = models.CharField(max_length=15, verbose_name="Nº do celular (--) ---- ---- do aluno", validators=[validate_phone])
    email_aluno = models.CharField(max_length=100, verbose_name="Email do aluno")
    cpf_aluno = models.CharField(max_length=11, unique=True, verbose_name="CPF do aluno", validators=[validate_cpf])
    birthday_aluno = models.DateField()
    class_choices = models.CharField(max_length=2, choices=TURMA_CHOICES, blank=True, null=False)
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE, verbose_name="Responsável")

    def __str__(self):
        return self.full_name

class Professor(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Nome")
    last_name = models.CharField(max_length=50, verbose_name="Sobrenome")
    phone_number = models.CharField(max_length=15, verbose_name="Nº do celular (--) ---- ----")
    email = models.EmailField(max_length=100, verbose_name="Email do professor")
    address = models.CharField(max_length=100, verbose_name="Endereço")
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF do professor")
    registration_number = models.CharField(max_length=20, unique=True, verbose_name="Número de Registro")
    disciplina = models.CharField(max_length=100, verbose_name="Disciplina", blank=True, null=True)  # Adicionado
    turma = models.ForeignKey(
        'Turma',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Turma",
        related_name="professores"  # Alterado para evitar conflito
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Registro: {self.registration_number})"

class Turma(models.Model):
    TURMA_CHOICES = (
        ("1A", "1º Ano A"),
        ("1B", "1º Ano B"),
        ("1C", "1º Ano C"),
        ("2A", "2º Ano A"),
        ("2B", "2º Ano B"),
        ("2C", "2º Ano C"),
        ("3A", "3º Ano A"),
        ("3B", "3º Ano B"),
        ("3C", "3º Ano C"),
    )
    ITINERARIO_CHOICES = (
        ("DS", "Desenvolvimento de Sistemas"),
        ("CN", "Ciências da Natureza"),
        ("J", "Jogos"),
    )
    turma = models.CharField(max_length=2, choices=TURMA_CHOICES, verbose_name="Turma")
    itinerario = models.CharField(max_length=2, choices=ITINERARIO_CHOICES, verbose_name="Itinerário")
    representante = models.ForeignKey(Aluno, on_delete=models.SET_NULL, related_name="representante_turma", null=True, blank=True, verbose_name="Representante")
    vice_representante = models.ForeignKey(Aluno, on_delete=models.SET_NULL, related_name="vice_representante_turma", null=True, blank=True, verbose_name="Vice-Representante")
    padrinho = models.ForeignKey(
        Professor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Padrinho",
        related_name="turmas_padrinhadas"  # Adicionado para evitar conflito
    )

    def __str__(self):
        return f"{self.turma} - {self.get_itinerario_display()}"

class Contrato(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name="Turma/Itinerário")
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name="Nome do Aluno")
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE, verbose_name="Nome do Responsável", blank=True, null=True)
    email_responsavel = models.EmailField(verbose_name="Email do Responsável", blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.aluno and not self.responsavel:
            self.responsavel = self.aluno.responsavel
            self.email_responsavel = self.aluno.responsavel.email
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Contrato: {self.aluno} - {self.turma}"