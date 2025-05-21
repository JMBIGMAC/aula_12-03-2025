from django.contrib import admin
from django.urls import path, include
from . import views
from .views import exemplo_json
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('data/', exemplo_json, name='exemplo_json'),
    path('api_overview/', views.api_overview, name='api_overview'),
    path('alunos/', views.alunos_json, name='alunos_json'),
    path('professores/', views.professores_json, name='professores_json'),
    path('turmas/', views.turmas_json, name='turmas_json'),
    path('contratos/', views.contratos_json, name='contratos_json'),
    path('notas/', views.notas_json, name='notas_json'),
    path('materias/', views.materias_json, name='materias_json'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)