from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
from .models import Contrato

def home(request):
    return render(request, 'home.html')

def contrato_pdf(request, contrato_id):
    contrato = get_object_or_404(Contrato, id=contrato_id)

    if contrato.aluno not in contrato.responsavel.alunos.all():
        return HttpResponse("Erro: O aluno não pertence ao responsável informado.", status=400)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="contrato_{contrato.id}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    margin_x = 50
    margin_y = 50
    line_height = 15
    current_y = height - margin_y

    def draw_wrapped_text(text, x, y, max_width):
        lines = simpleSplit(text, "Helvetica", 10, max_width)
        for line in lines:
            p.drawString(x, y, line)
            y -= line_height
        return y

    # Header
    p.setFont("Helvetica-Bold", 16)
    current_y -= 20
    p.drawString(margin_x, current_y, "CONTRATO DE MATRÍCULA ESCOLAR")

    # Introduction
    p.setFont("Helvetica", 10)
    current_y -= 30
    current_y = draw_wrapped_text(
        "Pelo presente instrumento particular, as partes abaixo assinadas, de um lado, a Escola Pedro Ludovico, "
        "doravante denominada Escola, e de outro lado, o responsável pelo aluno(a):",
        margin_x, current_y, width - 2 * margin_x
    )

    # Responsible Party Information
    p.setFont("Helvetica-Bold", 10)
    current_y -= 10
    current_y = draw_wrapped_text(
        f"Responsável: {contrato.responsavel.first_name} {contrato.responsavel.last_name}",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        f"CPF: {contrato.responsavel.cpf}",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        f"Endereço: {contrato.responsavel.address}",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        f"E-mail: {contrato.responsavel.email}",
        margin_x, current_y, width - 2 * margin_x
    )

    # Student Information
    current_y -= 10
    current_y = draw_wrapped_text(
        f"Aluno: {contrato.aluno.full_name}",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        f"Turma: {contrato.turma}",
        margin_x, current_y, width - 2 * margin_x
    )

    # Contract Clauses
    p.setFont("Helvetica", 10)
    current_y -= 20
    current_y = draw_wrapped_text(
        "Cláusula 1 - OBJETO DO CONTRATO",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        f"1.1 O presente contrato tem por objeto a matrícula do aluno(a) {contrato.aluno.full_name}, "
        f"na turma {contrato.turma} do ano letivo de {contrato.turma.turma} na Escola Pedro Ludovico.",
        margin_x, current_y, width - 2 * margin_x
    )

    current_y -= 10
    current_y = draw_wrapped_text(
        "Cláusula 2 - OBRIGAÇÕES DO RESPONSÁVEL",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        """2.1 O Responsável compromete-se a realizar o pagamento das mensalidades escolares 
        dentro dos prazos estabelecidos.""",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "2.2 O Responsável deverá comunicar à Escola qualquer alteração nos dados cadastrais do aluno(a).",
        margin_x, current_y, width - 2 * margin_x
    )

    current_y -= 10
    current_y = draw_wrapped_text(
        "Cláusula 3 - DISPOSIÇÕES GERAIS",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        """3.1 As partes acordam que todas as informações fornecidas durante o processo 
        de matrícula serão tratadas de forma confidencial.""",        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "3.2 Este contrato poderá ser alterado mediante acordo mútuo entre as partes.",
        margin_x, current_y, width - 2 * margin_x
    )

    # Signatures
    p.setFont("Helvetica-Bold", 10)
    current_y -= 30
    current_y = draw_wrapped_text(
        "Responsável:",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "Assinatura: ________________________________",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        f"Nome: {contrato.responsavel.first_name} {contrato.responsavel.last_name}",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        f"CPF: {contrato.responsavel.cpf}",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "Data: ____/____/________",
        margin_x, current_y, width - 2 * margin_x
    )

    current_y -= 20
    current_y = draw_wrapped_text(
        "Escola:",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "Assinatura: ________________________________",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "Nome do Representante: Clabreso",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "Cargo: Coordenador de Turno",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "Data: ____/____/________",
        margin_x, current_y, width - 2 * margin_x
    )

    # Witnesses
    current_y -= 20
    current_y = draw_wrapped_text(
        "Testemunhas:",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "Nome: ______________________________________",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "Assinatura: ________________________________",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "Nome: ______________________________________",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "Assinatura: ________________________________",
        margin_x, current_y, width - 2 * margin_x
    )

    p.save()

    return response