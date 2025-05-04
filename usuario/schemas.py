from ninja.schema import Schema


class UsuarioSchema(Schema):
    nome: str
    sobrenome: str
    email: str
    senha: str


class VerificacaoSchema(Schema):
    email: str
    nome: str

class LoginSchema(Schema):
    email: str
    senha: str

