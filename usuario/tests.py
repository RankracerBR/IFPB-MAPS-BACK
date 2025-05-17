from django.test import TestCase
from django.core.cache import cache
from django.contrib.auth.hashers import make_password
from .models import Usuario
from ninja.testing import TestClient

import json

from usuario.api import api_usuario

class TestUsuario(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = TestClient(api_usuario)

    def test_verificacao_email(self):
        data = {
            "email": "augustopontes010@gmail.com",
            "nome": "Augusto Pontes"
        }
        response = self.client.post(
            "/usuario/verificacao_email",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_criar_conta(self):
        # Get the token from cache (mocking this in real tests)
        valid_token = "mocked_valid_token_123"
        cache.set("test1234@gmail.com", valid_token, timeout=300)
        
        data = {
            "nome": "Fulano",
            "sobrenome": "de Tal",
            "email": "test1234@gmail.com",
            "senha": "teste*" 
        }
        response = self.client.post(
            f"/usuario/criar_conta?token={valid_token}",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        # Test with invalid token
        response = self.client.post(
            "/usuario/criar_conta?token=invalid_token_456",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
        
        # Test with no token
        response = self.client.post(
            "/usuario/criar_conta",
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
    
    def test_login_conta(self):
        hashed_password = make_password("testesenha1234")
        Usuario.objects.create(
            nome="Fulano",
            sobrenome="de Tal",
            email="test123@gmail.com",
            senha=hashed_password
        )
        
        login_data = {
            "email": "test123@gmail.com",
            "senha": "testesenha1234"
        }
        
        # Send as JSON
        response = self.client.post(
            '/usuario/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())