from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Contrato


def home(request):
    return render(request, 'home.html')


def contrato_pdf(request, contrato_id):
    contrato = get_object_or_404(Contrato, id=contrato_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="contrato_{contrato.id}.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, "Contrato Escolar")
    p.drawString(100, 780, f"Aluno: {contrato.aluno.full_name}")
    p.drawString(100, 760, f"Responsável: {contrato.responsavel.first_name} {contrato.responsavel.last_name}")
    p.drawString(100, 740, f"Turma: {contrato.turma}")
    p.drawString(100, 720, f"Email do Responsável: {contrato.email_responsavel}")
    p.drawString(100, 700, "O responsável se compromete a garantir que o aluno cumpra as normas da escola.")
    p.drawString(100, 680, "Além disso, o responsável assume total responsabilidade pelas ações do aluno.")
    p.drawString(100, 640, "Assinatura do Responsável: __________________________")
    p.save()

    return response