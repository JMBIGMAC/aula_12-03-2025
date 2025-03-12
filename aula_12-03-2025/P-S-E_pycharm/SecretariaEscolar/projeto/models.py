from django.db import models
class Responsavel(models.Model):
    fist_name = models.CharField(max_length=50, verbose_name="nome do responsavel")
    last_name = models.CharField(max_length=50, verbose_name="sobre nome do responsavel")
    phone_number = models.CharField(max_length=15, verbose_name="Nº do celular (--) ---- ---- do responsavel")
    email = models.CharField(max_length=100, verbose_name="email do responsavel")
    adress = models.CharField(max_length=100, verbose_name="endereço do responsavel")#coloque um validador/buscador de senha
    cpf = models.CharField(max_length=11, unique= True, verbose_name="cpf do responsavel")
    birthday = models.DateField()

    def __str__(self):
        return self.fist_name

class Aluno(models.Model):
    TURMA_CHOICES=(
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
    fist_name_aluno = models.CharField(max_length=50, verbose_name="Nome")
    last_name_aluno = models.CharField(max_length=50, verbose_name="Sobrenome")
    phone_number_aluno = models.CharField(max_length=15, verbose_name="Nº do celular (--) ---- ---- do aluno")
    email_aluno = models.CharField(max_length=100, verbose_name="email do aluno")
    cpf_aluno = models.CharField(max_length=11, unique=True, verbose_name="cpf do aluno")
    birthday_aluno = models.DateField()
    class_choices= models.CharField(max_length=2,choices=TURMA_CHOICES,blank=True,null=False)
    def __str__(self):
        return self.fist_name_aluno

class Professor(models.Model):
    last_name = models.CharField(max_length=50, verbose_name="Sobrenome")
    phone_number = models.CharField(max_length=15, verbose_name="Nº do celular (--) ---- ----")
    email = models.EmailField(max_length=100, verbose_name="Email do professor")
    address = models.CharField(max_length=100, verbose_name="Endereço")
    cpf = models.CharField(max_length=11, unique= True, verbose_name="cpf do professor")
    registration_number = models.CharField(max_length=20, unique=True, verbose_name="Número de Registro")

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Registro: {self.registration_number})"