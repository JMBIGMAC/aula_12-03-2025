from django.contrib import admin
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Responsavel, Aluno, Professor, Turma, Contrato

class ResponsaveisAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'email', 'address', 'cpf', 'birthday')
    list_display_links = ('id', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    list_filter = ('first_name', 'last_name')

class AlunoAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number_aluno', 'email_aluno', 'cpf_aluno', 'birthday_aluno', 'registration_number', 'class_choices', 'responsavel')
    list_display_links = ('full_name',)
    search_fields = ('full_name', 'registration_number', 'responsavel__first_name', 'responsavel__last_name')
    list_filter = ('class_choices', 'responsavel')

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'email', 'address', 'cpf', 'registration_number', 'disciplina', 'turma')  # Adicionado disciplina e turma
    list_display_links = ('id', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'disciplina')  # Adicionado disciplina
    list_filter = ('first_name', 'last_name', 'disciplina')  # Adicionado disciplina

class TurmaAdmin(admin.ModelAdmin):
    list_display = ('turma', 'itinerario', 'representante', 'vice_representante', 'padrinho')  # Adicionado padrinho
    list_display_links = ('turma',)
    search_fields = ('turma', 'itinerario', 'representante__first_name_aluno', 'vice_representante__first_name_aluno', 'padrinho__first_name')  # Adicionado padrinho
    list_filter = ('itinerario',)

class ContratoAdmin(admin.ModelAdmin):
    list_display = ('turma', 'aluno', 'responsavel', 'email_responsavel')
    list_display_links = ('turma', 'aluno')
    search_fields = ('aluno__full_name', 'responsavel__first_name', 'turma__turma')
    list_filter = ('turma',)

    actions = ['generate_pdf']

    def generate_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="contratos.pdf"'

        p = canvas.Canvas(response)

        for contrato in queryset:
            p.drawString(100, 800, "Contrato Escolar")
            p.drawString(100, 780, f"Aluno: {contrato.aluno.full_name}")
            p.drawString(100, 760, f"Responsável: {contrato.responsavel.first_name} {contrato.responsavel.last_name}")
            p.drawString(100, 740, f"Turma: {contrato.turma}")
            p.drawString(100, 720, f"Email do Responsável: {contrato.email_responsavel}")
            p.drawString(100, 700, "Este contrato confirma a matrícula do aluno na instituição de ensino.")
            p.showPage()

        p.save()
        return response

    generate_pdf.short_description = "Gerar PDF dos Contratos"

# Registrando os modelos no admin
admin.site.register(Responsavel, ResponsaveisAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Contrato, ContratoAdmin)
