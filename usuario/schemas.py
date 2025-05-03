from ninja.schema import Schema


class UsuarioSchema(Schema):
    nome: str
    sobrenome: str
    email: str
    senha: str


class VerificacaoASchema(Schema):
    email: str
    senha: str

class LoginSchema(Schema):
    email: str
    senha: str
    
