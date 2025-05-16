from django.core.cache import cache
from django.core.exceptions import ValidationError

from ninja.errors import HttpError

import re
import phonenumbers

from .models import Usuario


class ValidacaoUsuario:
    @staticmethod
    def validacao_senha_usuario(senha):
        try:
            erros = []

            if len(senha) < 8:
                erros.append("A senha deve ter pelo menos 8 caracteres.")
            if not re.search(r"[A-Za-z]", senha):
                erros.append("A senha deve conter pelo menos uma letra.")
            if not re.search(r"\d", senha):
                erros.append("A senha deve conter pelo menos um número.")
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
                erros.append("A senha deve conter pelo menos um caractere especial.")

        except ValidationError as e:
            error_dict = {"errors": list(e.message)}
            return 400, error_dict

    @staticmethod
    def valida_token_usuario(email, token):
        cached_token = cache.get(email)
        print(f"Cached token: {cached_token}, Provided token: {token}")
        return cached_token == token

    @staticmethod
    def valida_telefone_usuario(telefone):
        """Validate the phone number format."""
        try:
            telefone_enviado = phonenumbers.parse(telefone, "BR")
            return phonenumbers.is_valid_number(telefone_enviado)
        except phonenumbers.NumberParseException:
            raise HttpError(400, {"error": "Número de telefone inválido"})

    @staticmethod
    def valida_email_usuario(email):
        if Usuario.objects.filter(email=email).exists():
            raise HttpError(400, {"error": "O email já está registrado."})
