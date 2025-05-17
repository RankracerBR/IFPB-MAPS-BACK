from django.contrib.auth import logout
from django.core.cache import cache
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse

from ninja import NinjaAPI
from ninja.errors import HttpError

import hashlib
import secrets
from datetime import datetime, timedelta
import os
import jwt

from .models import Usuario
from .schemas import UsuarioSchema, VerificacaoSchema, LoginSchema
from .validation import ValidacaoUsuario


api_usuario = NinjaAPI(urls_namespace="usuario")

SECRET_KEY2 = os.getenv("SECRET_KEY2")


class UsuarioApi:
    @staticmethod
    @api_usuario.post('/verificacao_email')
    def verificacao_email(request, verificacao: VerificacaoSchema):
        try:
            token = hashlib.sha512(secrets.token_bytes(32)).hexdigest()
            cache.set(verificacao.email, token, timeout=60*5)
            
            verificacao_url = request.build_absolute_uri(
                reverse("usuario:criar_conta") + f"?token={token}"
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
            return {"message": "Verificação de email feita com sucesso!"}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    @api_usuario.post('/criar_conta', response={
        200: UsuarioSchema,
        400: dict,
        401: dict  # For invalid token
    })
    def criar_conta(request, token: str = None, usuario: UsuarioSchema = None):
        try:
            # Validate token first
            if not token or not cache.get(usuario.email) == token:
                return 401, {"error": "Token inválido ou expirado"}
                
            # Rest of your validation
            email_usuario = usuario.email
            senha_usuario = usuario.senha
            ValidacaoUsuario.valida_email_usuario(email_usuario)
            ValidacaoUsuario.validacao_senha_usuario(senha_usuario)
            
            usuario_info = usuario.model_dump()
            usuario_info["senha"] = make_password(usuario_info["senha"])
            instancia_usuario = Usuario.objects.create(**usuario_info)
            
            # Clear the token after successful account creation
            cache.delete(usuario.email)
            
            return 200, UsuarioSchema.model_validate(instancia_usuario)
            
        except Exception as e:
            return 400, {"error": str(e)}

    @staticmethod
    @api_usuario.post("/login", response=UsuarioSchema)
    def login_usuario(request, data: LoginSchema):
        try:
            usuario = Usuario.objects.filter(email=data.email).first()
            
            if not usuario:
                return JsonResponse({"error": "usuário não encontrado"}, status=404)
            
            if not check_password(data.senha, usuario.senha):
                return JsonResponse({"error": "Senha incorreto"}, status=400)
            
            tempo_expiracao = datetime.now() + timedelta(days=1)
            token = jwt.encode(
                {"email": usuario.email, "exp": tempo_expiracao},
                SECRET_KEY2,
                algorithm="HS256",
            )
            
            return JsonResponse({"message": "Login bem-sucedido", "token": token})
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    @staticmethod
    @api_usuario.post("/logout")
    def logout_usuario(request):
        if "user_id" in request.session:
            logout(request)
            return {"message": "Logout realizado sucesso"}
        else:
            raise HttpError(401, "Usuário não autênticado")

    @staticmethod
    def mudar_parametros_conta(request):
        ...
    
    @staticmethod
    def lugares_favoritos(request):
        ...
