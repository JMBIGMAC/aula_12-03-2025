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

# Add these validation functions at the top of the file
def validate_nota(value):
    if not -100 <= value <= 100:
        raise ValidationError("Nota deve estar entre -100 e 100.")

class Responsavel(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Nome do responsável")
    last_name = models.CharField(max_length=50, verbose_name="Sobrenome do responsável")
    phone_number = models.CharField(max_length=15, verbose_name="Nº do celular (--) ---- ---- do responsável", validators=[validate_phone])
    email = models.CharField(max_length=100, verbose_name="Email do responsável")
    address = models.CharField(max_length=100, verbose_name="Endereço do responsável")
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF do responsável", validators=[validate_cpf])
    birthday = models.DateField()
    alunos = models.ManyToManyField(
        'Aluno',
        related_name='responsaveis',
        verbose_name="Alunos do Responsável",
        blank=True  # Allow Responsavel to be created without associating Aluno
    )

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
    responsavel = models.ForeignKey(
        Responsavel,
        on_delete=models.CASCADE,
        verbose_name="Responsável",
        related_name="Aluno"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Automatically create Notas for each Materia in the Turma
        turma = Turma.objects.filter(turma=self.class_choices).first()
        if turma:
            materias = [turma.materia_1, turma.materia_2, turma.materia_3, turma.materia_4]
            for materia in materias:
                if materia:
                    Notas.objects.get_or_create(aluno=self, turma=turma, materia=materia)

    def __str__(self):
        return self.full_name

class Materia(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome da Matéria")
    professor = models.ForeignKey(
        'Professor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="materias_responsaveis",  # Updated related_name to avoid conflict
        verbose_name="Professor Responsável"
    )

    def __str__(self):
        return self.name

class Professor(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Nome")
    last_name = models.CharField(max_length=50, verbose_name="Sobrenome")
    phone_number = models.CharField(max_length=15, verbose_name="Nº do celular (--) ---- ----")
    email = models.EmailField(max_length=100, verbose_name="Email do professor")
    address = models.CharField(max_length=100, verbose_name="Endereço")
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF do professor")
    registration_number = models.CharField(max_length=20, unique=True, verbose_name="Número de Registro")
    materias = models.ManyToManyField(
        'Materia',
        related_name="professores_responsaveis",  # Updated related_name to avoid conflict
        verbose_name="Matérias",
        blank=True  # Allow professors to be created without assigning materias
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
    turma = models.CharField(max_length=2, choices=TURMA_CHOICES, verbose_name="Turma")
    materia_1 = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="turma_materia_1", verbose_name="Matéria 1",blank=True)
    materia_2 = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="turma_materia_2", verbose_name="Matéria 2",blank=True)
    materia_3 = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="turma_materia_3", verbose_name="Matéria 3",blank=True)
    materia_4 = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="turma_materia_4", verbose_name="Matéria 4",blank=True)
    representante = models.ForeignKey(Aluno, on_delete=models.SET_NULL, related_name="representante_turma", null=True, blank=True, verbose_name="Representante")
    vice_representante = models.ForeignKey(Aluno, on_delete=models.SET_NULL, related_name="vice_representante_turma", null=True, blank=True, verbose_name="Vice-Representante")
    padrinho = models.ForeignKey(
        Professor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Padrinho",
        related_name="turmas_padrinhadas"
    )

    def __str__(self):
        return f"{self.turma}"

class Contrato(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name="Turma/Itinerário", blank=True, null=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name="Nome do Aluno")
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE, verbose_name="Nome do Responsável", blank=True, null=True)
    email_responsavel = models.EmailField(verbose_name="Email do Responsável", blank=True, null=True)
    signed_contract = models.FileField(upload_to='signed_contracts/', blank=True, null=True, verbose_name="Contrato Assinado")

    def save(self, *args, **kwargs):
        if self.aluno and self.responsavel:
            if self.aluno not in self.responsavel.alunos.all():
                raise ValidationError("O aluno selecionado não pertence ao responsável informado.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Contrato: {self.aluno} - {self.turma}"

class Nota(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name="Turma")
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, verbose_name="Matéria")
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name="Aluno")
    nota_presenca = models.FloatField(
        verbose_name="Nota de Presença (Diário)",
        default=0,
        validators=[validate_nota]
    )
    nota_atividade = models.FloatField(
        verbose_name="Nota de Atividade (Diário)",
        default=0,
        validators=[validate_nota]
    )
    nota_avaliativa = models.FloatField(
        verbose_name="Nota Avaliativa (Mensal)",
        default=0,
        validators=[validate_nota]
    )
    nota_final = models.FloatField(verbose_name="Nota Final (0 a 100)", editable=False)

    class Meta:
        unique_together = ('turma', 'materia', 'aluno')  # Ensure unique Notas per aluno, turma, and materia

    def save(self, *args, **kwargs):
        self.nota_final = (self.nota_presenca + self.nota_atividade + self.nota_avaliativa) / 3
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Notas de {self.aluno.full_name} - {self.materia} ({self.turma})"