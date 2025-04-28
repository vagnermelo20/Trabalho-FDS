from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

class TesteFluxoCompletoObjetivos(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_fluxo_completo_usuario_objetivos(self):
        driver = self.driver

        # ---------- 1. Cadastro de novo usuário ----------
        driver.get(f'{self.live_server_url}/criar_usuario/')
        time.sleep(1)

        driver.find_element(By.ID, "campo_username").send_keys("UsuarioNovoTeste")
        time.sleep(1)
        driver.find_element(By.ID, "campo_email").send_keys("novousuario@teste.com")
        time.sleep(1)
        driver.find_element(By.ID, "campo_senha").send_keys("senha321")
        time.sleep(1)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        # Após cadastro, volta para página de login
        self.assertEqual(driver.current_url, f'{self.live_server_url}/')

        # ---------- 2. Login com o novo usuário ----------
        campo_email = driver.find_element(By.ID, "campo_email")
        time.sleep(1)
        campo_senha = driver.find_element(By.ID, "campo_senha")
        time.sleep(1)
        botao_entrar = driver.find_element(By.TAG_NAME, "button")
        time.sleep(1)

        campo_email.send_keys("novousuario@teste.com")
        time.sleep(1)
        campo_senha.send_keys("senha321")
        time.sleep(1)
        botao_entrar.click()

        WebDriverWait(driver, 10).until(
            EC.url_contains('/objetivos/')
        )
        time.sleep(1)

        self.assertIn('/objetivos/', driver.current_url)

        # ---------- 3. Criação de objetivo com sucesso ----------
        driver.find_element(By.LINK_TEXT, "+ Criar tarefas").click()
        time.sleep(1)

        driver.find_element(By.ID, "campo_nome").send_keys("Objetivo Teste 1")
        time.sleep(1)
        driver.find_element(By.ID, "campo_descricao").send_keys("Descrição do objetivo 1.")
        time.sleep(1)
        driver.find_element(By.ID, "campo_urgencia").send_keys("2")
        time.sleep(1)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        driver.find_element(By.LINK_TEXT, "📋 Ver todos os objetivos").click()
        time.sleep(1)

        body_text = driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Objetivo Teste 1", body_text)

        # ---------- 4. Tentativa de criar objetivo sem nome ----------
        driver.find_element(By.LINK_TEXT, "+ Criar tarefas").click()
        time.sleep(1)

        driver.find_element(By.ID, "campo_descricao").send_keys("Descrição sem título.")
        time.sleep(1)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        # Valida que deu erro
        body_text = driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("É necessário preencher o nome do objetivo.", body_text)

        # ---------- 5. Tentativa de criar objetivo duplicado ----------
        driver.find_element(By.ID, "campo_nome").send_keys("Objetivo Teste 1")
        time.sleep(1)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        # Valida que deu erro de duplicidade
        body_text = driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Você já tem uma tarefa com este nome. Por favor, escolha um nome diferente.", body_text)

        # Clicar em Voltar para voltar para objetivos

        driver.find_element(By.LINK_TEXT, "Voltar").click()
        time.sleep(1)

        driver.find_element(By.LINK_TEXT, "Editar").click()
        time.sleep(1)

        campo_nome = driver.find_element(By.ID, "campo_nome")
        time.sleep(1)
        campo_nome.clear()
        campo_nome.send_keys("Objetivo Teste Editado")
        time.sleep(1)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        self.assertIn('/objetivos/', driver.current_url)

        # ---------- 7. Deletar o objetivo criado ----------
        botao_deletar = driver.find_element(By.XPATH, "//form/button[contains(text(), 'Deletar')]")
        botao_deletar.click()
        time.sleep(1)
        alerta = driver.switch_to.alert
        alerta.accept()
        time.sleep(2)

        body_text = driver.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Objetivo Teste Editado", body_text)
