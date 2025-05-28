from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Aluno, Responsavel, Professor # Import Responsavel and Professor models

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ['registration_number', 'full_name', 'email_aluno', 'class_choices']
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user
class ResponsavelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsavel # Corrected model name
        fields = '__all__'
class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'
