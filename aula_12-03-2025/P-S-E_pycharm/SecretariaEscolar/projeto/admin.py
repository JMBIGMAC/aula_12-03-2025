from django.contrib import admin
from .models import Responsavel, Aluno, Professor
class ResponsaveisAdimin(admin.ModelAdmin):
    list_display = ('id','fist_name','last_name','phone_number','email','adress','cpf','birthday')
    list_display_links = ('','fist_name','last_name','phone_number','email','adress')
    search_fields = ('fist_name','last_name')
    list_filter = ('fist_name','last_name')
class AlunoAdimin(admin.ModelAdmin):
    list_display = ('fist_name_aluno', 'last_name_aluno', 'phone_number_aluno', 'email_aluno', 'cpf_aluno', 'birthday_aluno')
    list_display_links = ('fist_name_aluno', 'last_name_aluno', 'phone_number_aluno', 'email_aluno')
    search_fields = ('fist_name', 'last_name')
    list_filter = ('fist_name', 'last_name')
class ProfessorAdimin(admin.ModelAdmin):
    list_display = ('id', 'fist_name', 'last_name', 'phone_number', 'email', 'adress', 'cpf', 'birthday')
    list_display_links = ('', 'fist_name', 'last_name', 'phone_number', 'email', 'adress')
    search_fields = ('fist_name', 'last_name')
    list_filter = ('fist_name', 'last_name')

admin.site.register(Responsavel)
admin.site.register(Aluno)
admin.site.register(Professor)
