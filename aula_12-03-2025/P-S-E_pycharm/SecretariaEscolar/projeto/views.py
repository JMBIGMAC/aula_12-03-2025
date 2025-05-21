from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
from .models import Contrato, Aluno, Responsavel, Professor, Turma, Nota, Materia
from django.contrib.auth.models import User, Group, Permission
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
import json

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

def exemplo_json(request):
    try:
        data = {"mensagem": "Dados enviados do backend Django!", "status": "ok"}
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def api_overview(request):
    """Endpoint para overview das rotas da API."""
    data = {
        "alunos": "/api/alunos/",
        "professores": "/api/professores/",
        "turmas": "/api/turmas/",
        "contratos": "/api/contratos/",
        "notas": "/api/notas/",
        "materias": "/api/materias/",
    }
    return JsonResponse(data)

# API para listar alunos
from django.forms.models import model_to_dict

def alunos_json(request):
    alunos = Aluno.objects.all()
    data = [model_to_dict(aluno) for aluno in alunos]
    return JsonResponse(data, safe=False)

def professores_json(request):
    professores = Professor.objects.all()
    data = []
    for prof in professores:
        prof_dict = model_to_dict(prof)
        # Serializar o campo ManyToMany 'materias' como lista de nomes
        prof_dict['materias'] = list(prof.materias.values_list('name', flat=True))
        data.append(prof_dict)
    return JsonResponse(data, safe=False)

def turmas_json(request):
    turmas = Turma.objects.all()
    data = [model_to_dict(turma) for turma in turmas]
    return JsonResponse(data, safe=False)

def contratos_json(request):
    contratos = Contrato.objects.all()
    data = [model_to_dict(contrato) for contrato in contratos]
    return JsonResponse(data, safe=False)

def notas_json(request):
    notas = Nota.objects.all()
    data = [model_to_dict(nota) for nota in notas]
    return JsonResponse(data, safe=False)

def materias_json(request):
    materias = Materia.objects.all()
    data = [model_to_dict(materia) for materia in materias]
    return JsonResponse(data, safe=False)

def usuarios_json(request):
    users = User.objects.all()
    data = [
        {
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'is_superuser': u.is_superuser,
            'groups': list(u.groups.values_list('name', flat=True)),
        } for u in users
    ]
    return JsonResponse(data, safe=False)

def grupos_json(request):
    grupos = Group.objects.all()
    data = [
        {
            'id': g.id,
            'name': g.name,
            'usuarios': list(g.user_set.values_list('username', flat=True)),
        } for g in grupos
    ]
    return JsonResponse(data, safe=False)

# Página de administração customizada

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@csrf_exempt
@require_http_methods(["POST"])
def criar_usuario(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    grupos = data.get('grupos', [])
    if not username or not password:
        return JsonResponse({'error': 'Usuário e senha obrigatórios.'}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Usuário já existe.'}, status=400)
    user = User.objects.create_user(username=username, password=password, email=email)
    for g in grupos:
        grupo, _ = Group.objects.get_or_create(name=g)
        user.groups.add(grupo)
    user.save()
    return JsonResponse({'success': True, 'id': user.id})

@csrf_exempt
@require_http_methods(["POST"])
def criar_grupo(request):
    data = json.loads(request.body)
    nome = data.get('nome')
    permissoes = data.get('permissoes', [])
    if not nome:
        return JsonResponse({'error': 'Nome do grupo obrigatório.'}, status=400)
    grupo, created = Group.objects.get_or_create(name=nome)
    if permissoes:
        perms = Permission.objects.filter(codename__in=permissoes)
        grupo.permissions.set(perms)
    grupo.save()
    return JsonResponse({'success': True, 'id': grupo.id, 'created': created})

@csrf_exempt
@require_http_methods(["POST"])
def login_api(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        groups = list(user.groups.values_list('name', flat=True))
        permissions = list(user.get_all_permissions())
        return JsonResponse({"success": True, "groups": groups, "permissions": permissions})
    else:
        return JsonResponse({"success": False, "error": "Usuário ou senha inválidos"})