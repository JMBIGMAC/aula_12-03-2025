from django.contrib import admin
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.utils.html import format_html
from django.urls import reverse
from .models import Responsavel, Aluno, Professor, Turma, Contrato
from .models import Nota, Materia

class ResponsaveisAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'email', 'address', 'cpf', 'birthday')
    list_display_links = ('id', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    list_filter = ('first_name', 'last_name')

class NotasInline(admin.TabularInline):
    model = Nota
    fields = ('materia', 'nota_presenca', 'nota_atividade', 'nota_avaliativa', 'nota_final')
    readonly_fields = ('nota_final',)
    extra = 0  # Do not show extra empty forms

class AlunoAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number_aluno', 'email_aluno', 'cpf_aluno', 'birthday_aluno', 'registration_number', 'class_choices', 'responsavel')
    list_display_links = ('full_name',)
    search_fields = ('full_name', 'registration_number', 'responsavel__first_name', 'responsavel__last_name')
    list_filter = ('class_choices', 'responsavel')
    inlines = [NotasInline]  # Add NotasInline to display and edit Notas for each Materia

    def view_notas(self, obj):
        url = reverse('admin:projeto_notas_changelist') + f'?aluno__id__exact={obj.id}'
        return format_html('<a href="{}">Ver Notas</a>', url)

    view_notas.short_description = "Notas"

class MateriaInline(admin.TabularInline):
    model = Materia
    extra = 1

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'email', 'address', 'cpf', 'registration_number')
    list_display_links = ('id', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    list_filter = ('first_name', 'last_name')
    filter_horizontal = ('materias',)  # Allow selecting multiple existing Materias
    inlines = [MateriaInline]

class TurmaAdmin(admin.ModelAdmin):
    list_display = ('turma', 'materia_1', 'materia_2', 'materia_3', 'materia_4', 'representante', 'vice_representante', 'padrinho')
    list_display_links = ('turma',)
    search_fields = ('turma', 'materia_1__name', 'materia_2__name', 'materia_3__name', 'materia_4__name')
    list_filter = ('turma',)

class ContratoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'responsavel', 'turma', 'email_responsavel', 'download_signed_contract')
    list_display_links = ('aluno',)
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
            p.drawString(100, 700, "O responsável se compromete a garantir que o aluno cumpra as normas da escola.")
            p.drawString(100, 680, "Além disso, o responsável assume total responsabilidade pelas ações do aluno.")
            p.drawString(100, 640, "Assinatura do Responsável: __________________________")
            p.showPage()

        p.save()
        return response

    def download_signed_contract(self, obj):
        if obj.signed_contract:
            return format_html('<a href="{}" download>Baixar Contrato Assinado</a>', obj.signed_contract.url)
        return "Contrato não enviado"

    download_signed_contract.short_description = "Contrato Assinado"

    generate_pdf.short_description = "Gerar PDF dos Contratos"

class NotasAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'turma', 'materia', 'nota_presenca', 'nota_atividade', 'nota_avaliativa', 'nota_final')
    search_fields = ('aluno__full_name', 'materia__name', 'turma__turma')
    list_filter = ('turma', 'materia')  # Filter by Turma and Materia
    readonly_fields = ('nota_final',)

    def get_queryset(self, request):
        # Filter queryset to show only relevant data
        qs = super().get_queryset(request)
        turma_id = request.GET.get('turma__id__exact')
        aluno_id = request.GET.get('aluno__id__exact')
        if turma_id:
            qs = qs.filter(turma_id=turma_id)
        if aluno_id:
            qs = qs.filter(aluno_id=aluno_id)
        return qs

    def changelist_view(self, request, extra_context=None):
        # Add hierarchical filtering to the admin interface
        turma_id = request.GET.get('turma__id__exact')
        aluno_id = request.GET.get('aluno__id__exact')
        extra_context = extra_context or {}
        if turma_id:
            extra_context['title'] = f"Notas - Turma {Turma.objects.get(id=turma_id)}"
        if aluno_id:
            extra_context['title'] = f"Notas - Aluno {Aluno.objects.get(id=aluno_id)}"
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Materia)
admin.site.register(Responsavel, ResponsaveisAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Nota, NotasAdmin)
