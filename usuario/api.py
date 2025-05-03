from ninja import NinjaAPI

from schemas import UsuarioSchema, VerificacaoASchema, LoginSchema

api_usuario = NinjaAPI(urls_namespace="usuario")


class UsuarioApi:
    @staticmethod
    def verficacao_email(request, verficacao: VerificacaoASchema):
        ...
    
    @staticmethod
    def criar_conta(request, usuario: UsuarioSchema):
        ...
    
    @staticmethod
    def login_usuario(request, login: LoginSchema):
        ...