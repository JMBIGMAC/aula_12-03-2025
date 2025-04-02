from django.db import models

class Responsavel(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Nome do responsável")
    last_name = models.CharField(max_length=50, verbose_name="Sobrenome do responsável")
    phone_number = models.CharField(max_length=15, verbose_name="Nº do celular (--) ---- ---- do responsável")
    email = models.CharField(max_length=100, verbose_name="Email do responsável")
    address = models.CharField(max_length=100, verbose_name="Endereço do responsável")
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF do responsável")
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
    first_name_aluno = models.CharField(max_length=50, verbose_name="Nome")
    last_name_aluno = models.CharField(max_length=50, verbose_name="Sobrenome")
    phone_number_aluno = models.CharField(max_length=15, verbose_name="Nº do celular (--) ---- ---- do aluno")
    email_aluno = models.CharField(max_length=100, verbose_name="Email do aluno")
    cpf_aluno = models.CharField(max_length=11, unique=True, verbose_name="CPF do aluno")
    birthday_aluno = models.DateField()
    class_choices = models.CharField(max_length=2, choices=TURMA_CHOICES, blank=True, null=False)

    def __str__(self):
        return self.first_name_aluno

class Professor(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Nome")
    last_name = models.CharField(max_length=50, verbose_name="Sobrenome")
    phone_number = models.CharField(max_length=15, verbose_name="Nº do celular (--) ---- ----")
    email = models.EmailField(max_length=100, verbose_name="Email do professor")
    address = models.CharField(max_length=100, verbose_name="Endereço")
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF do professor")
    registration_number = models.CharField(max_length=20, unique=True, verbose_name="Número de Registro")

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

    def __str__(self):
        return f"{self.turma} - {self.get_itinerario_display()}"

class Contrato(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name="Turma/Itinerário")
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name="Nome do Aluno")
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE, verbose_name="Nome do Responsável")
    email_responsavel = models.EmailField(verbose_name="Email do Responsável")

    def __str__(self):
        return f"Contrato: {self.aluno} - {self.turma}"