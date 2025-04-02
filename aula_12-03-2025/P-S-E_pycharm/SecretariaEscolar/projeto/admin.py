from django.contrib import admin
from .models import Responsavel, Aluno, Professor, Turma, Contrato

class ResponsaveisAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'email', 'address', 'cpf', 'birthday')
    list_display_links = ('id', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    list_filter = ('first_name', 'last_name')

class AlunoAdmin(admin.ModelAdmin):
    list_display = ('first_name_aluno', 'last_name_aluno', 'phone_number_aluno', 'email_aluno', 'cpf_aluno', 'birthday_aluno', 'class_choices')
    list_display_links = ('first_name_aluno', 'last_name_aluno')
    search_fields = ('first_name_aluno', 'last_name_aluno')
    list_filter = ('class_choices',)

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'email', 'address', 'cpf', 'registration_number')
    list_display_links = ('id', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    list_filter = ('first_name', 'last_name')

class TurmaAdmin(admin.ModelAdmin):
    list_display = ('turma', 'itinerario', 'representante', 'vice_representante')
    list_display_links = ('turma',)
    search_fields = ('turma', 'itinerario')
    list_filter = ('itinerario',)

class ContratoAdmin(admin.ModelAdmin):
    list_display = ('turma', 'aluno', 'responsavel', 'email_responsavel')
    list_display_links = ('turma', 'aluno')
    search_fields = ('aluno__first_name_aluno', 'responsavel__first_name')
    list_filter = ('turma',)

# Registrando os modelos no admin
admin.site.register(Responsavel, ResponsaveisAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Contrato, ContratoAdmin)
