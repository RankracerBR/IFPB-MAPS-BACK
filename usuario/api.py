from django.core.cache import cache
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password

from ninja import NinjaAPI

import hashlib
import secrets
from datetime import datetime, timedelta

from .models import Usuario
from .schemas import UsuarioSchema, VerificacaoSchema, LoginSchema
from .validation import ValidacaoUsuario

api_usuario = NinjaAPI(urls_namespace="usuario")


class UsuarioApi:
    @staticmethod
    def verficacao_email(request, verificacao: VerificacaoSchema):
        token = hashlib.sha512(secrets.token_bytes(32)).hexdigits()
        cache.set(verificacao.email, token, timeout=60*5)
        
        verificacao_url = request.build_absolute_uri(
            reverse("usuario:criar_usuario") + f"?token={token}"
        )
        
        send_mail(
            subject="Verificação de email",
            message=(
                f"Olá {verificacao.nome},\n"
                f"clique abaixo para registrar a sua conta\n{verificacao_url} \n"
                "lembrando que você tem apenas 5 minutos para se cadastrar,"
                "caso contrário o token irá se expirar"
            ),
            from_email="rankracerbr21@gmail.com",
            recipient_list=[verificacao.email],
        )
        
    @staticmethod
    def criar_conta(request, usuario: UsuarioSchema):
        try:
            email_usuario = usuario.email
            senha_usuario = usuario.senha
            ValidacaoUsuario.valida_email_usuario(email_usuario)
            ValidacaoUsuario.validacao_senha_usuario(senha_usuario)
            
            usuario_info = usuario.model_dump()
            usuario_info["senha_usuario"] = make_password(usuario_info["senha_usuario"])
            instancia_usuario = Usuario.objects.create(**usuario_info)
            
            return UsuarioSchema.model_validate(instancia_usuario)
            
        except Exception as e:
            return 400, {"error": str(e)}
    
    @staticmethod
    def login_usuario(request, login: LoginSchema):
        ...