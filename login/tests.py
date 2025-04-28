from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from login.models import Usuario
from django.contrib.auth.hashers import make_password

class TesteUsuarioE2E(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        # Cria um usuário de teste para o teste de login
        Usuario.objects.create(
            email='teste@teste.com',
            senha=make_password('senha123')
        )

    def test_login_sucesso(self):
        """
        Testa se o login do usuário funciona corretamente.
        """
        # Acessa a página de login
        self.driver.get(f'{self.live_server_url}/')

        campo_email = self.driver.find_element(By.ID, "campo_email")
        campo_senha = self.driver.find_element(By.ID, "campo_senha")
        botao_entrar = self.driver.find_element(By.TAG_NAME, "button")

        campo_email.send_keys('teste@teste.com')
        campo_senha.send_keys('senha123')
        botao_entrar.click()

        # Espera redirecionar corretamente para objetivos
        self.driver.implicitly_wait(5)

        self.assertIn('/objetivos/', self.driver.current_url)


    def test_cadastro_usuario(self):
        """
        Testa se é possível cadastrar um novo usuário.
        """
        self.driver.get(f'{self.live_server_url}/criar_usuario/')

        self.driver.find_element(By.ID, "campo_username").send_keys("NovoUsuarioTeste")
        self.driver.find_element(By.ID, "campo_email").send_keys("novo@teste.com")
        self.driver.find_element(By.ID, "campo_senha").send_keys("senha321")
        self.driver.find_element(By.TAG_NAME, "button").click()

        self.assertEqual(self.driver.current_url, f'{self.live_server_url}/')

