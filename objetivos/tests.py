from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

class CriarObjetivo(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def teste_Criar(self):
        driver = self.driver

        # 1. Cadastro de novo usuário
        driver.get(f'{self.live_server_url}/criar_usuario/')
        driver.find_element(By.ID, "campo_username").send_keys("UsuarioNovoTeste")
        driver.find_element(By.ID, "campo_email").send_keys("novousuario@teste.com")
        driver.find_element(By.ID, "campo_senha").send_keys("senha321")
        driver.find_element(By.TAG_NAME, "button").click()

        self.assertEqual(driver.current_url, f'{self.live_server_url}/')

        # 2. Login
        driver.find_element(By.ID, "campo_email").send_keys("novousuario@teste.com")
        driver.find_element(By.ID, "campo_senha").send_keys("senha321")
        driver.find_element(By.TAG_NAME, "button").click()

        WebDriverWait(driver, 10).until(EC.url_contains('/objetivos/'))
        time.sleep(1)

        # 3. Criar objetivo
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

        # 4. Criar objetivo sem nome
        driver.find_element(By.LINK_TEXT, "+ Criar tarefas").click()
        time.sleep(1)
        driver.find_element(By.ID, "campo_descricao").send_keys("Descrição sem título.")
        time.sleep(1)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        self.assertIn("É necessário preencher o nome do objetivo.", driver.find_element(By.TAG_NAME, "body").text)
        time.sleep(1)

        # 5. Criar objetivo duplicado
        driver.find_element(By.ID, "campo_nome").send_keys("Objetivo Teste 1")
        time.sleep(1)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        self.assertIn("Você já tem uma tarefa com este nome.", driver.find_element(By.TAG_NAME, "body").text)
        time.sleep(1)

        driver.find_element(By.LINK_TEXT, "Voltar").click()
        time.sleep(1)



class GerenciarObjetivo(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_Gerenciar(self):
        driver = self.driver

        # 1. Cadastro de novo usuário
        driver.get(f'{self.live_server_url}/criar_usuario/')
        driver.find_element(By.ID, "campo_username").send_keys("UsuarioNovoTeste")
        driver.find_element(By.ID, "campo_email").send_keys("novousuario@teste.com")
        driver.find_element(By.ID, "campo_senha").send_keys("senha321")
        driver.find_element(By.TAG_NAME, "button").click()

        self.assertEqual(driver.current_url, f'{self.live_server_url}/')

        # 2. Login
        driver.find_element(By.ID, "campo_email").send_keys("novousuario@teste.com")
        driver.find_element(By.ID, "campo_senha").send_keys("senha321")
        driver.find_element(By.TAG_NAME, "button").click()

        WebDriverWait(driver, 10).until(EC.url_contains('/objetivos/'))
        time.sleep(1)

        # 3. Criar objetivo 1
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

        # 3. Criar objetivo 2
        driver.find_element(By.LINK_TEXT, "+ Criar tarefas").click()
        time.sleep(1)
        driver.find_element(By.ID, "campo_nome").send_keys("Objetivo Teste 2")
        time.sleep(1)
        driver.find_element(By.ID, "campo_descricao").send_keys("Descrição do objetivo 2.")
        time.sleep(1)
        driver.find_element(By.ID, "campo_urgencia").send_keys("2")
        time.sleep(1)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        # 6. Editar objetivo
        driver.find_element(By.LINK_TEXT, "Editar").click()
        time.sleep(1)
        campo_nome = driver.find_element(By.ID, "campo_nome")
        campo_nome.clear()
        campo_nome.send_keys("Objetivo Teste Editado")
        time.sleep(1)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        driver.find_element(By.LINK_TEXT, "Visualizar subtarefas").click()
        time.sleep(1)

        self.assertIn("Não há subtarefas cadastradas para este objetivo", driver.find_element(By.TAG_NAME, "body").text)
        time.sleep(1)

                # 12. Deletar objetivo
        botao_deletar_obj = driver.find_element(By.XPATH, "//form/button[contains(text(), 'Deletar')]")
        botao_deletar_obj.click()
        time.sleep(1)
        alerta = driver.switch_to.alert
        alerta.accept()
        time.sleep(2)

        self.assertNotIn("Objetivo Teste Editado", driver.find_element(By.TAG_NAME, "body").text)





# class TesteCriarSubtarefa(LiveServerTestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         options = Options()
#         if os.environ.get('GITHUB_ACTIONS') == 'true':
#             options.add_argument('--headless')
#             options.add_argument('--no-sandbox')
#             options.add_argument('--disable-dev-shm-usage')
#         cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#         cls.driver.implicitly_wait(10)

#     @classmethod
#     def tearDownClass(cls):
#         cls.driver.quit()
#         super().tearDownClass()

#     def test_fluxo_completo_usuario_objetivos(self):
#         driver = self.driver

#         # 1. Cadastro de novo usuário
#         driver.get(f'{self.live_server_url}/criar_usuario/')
#         driver.find_element(By.ID, "campo_username").send_keys("UsuarioNovoTeste")
#         driver.find_element(By.ID, "campo_email").send_keys("novousuario@teste.com")
#         driver.find_element(By.ID, "campo_senha").send_keys("senha321")
#         driver.find_element(By.TAG_NAME, "button").click()

#         self.assertEqual(driver.current_url, f'{self.live_server_url}/')

#         # 2. Login
#         driver.find_element(By.ID, "campo_email").send_keys("novousuario@teste.com")
#         driver.find_element(By.ID, "campo_senha").send_keys("senha321")
#         driver.find_element(By.TAG_NAME, "button").click()

#         WebDriverWait(driver, 10).until(EC.url_contains('/objetivos/'))
#         time.sleep(1)

#         # 7. Criar subtarefa
#         driver.find_element(By.LINK_TEXT, "+ Criar subtarefa").click()
#         time.sleep(1)
#         driver.find_element(By.ID, "campo_nome").send_keys("Subtarefa Teste 1")
#         time.sleep(1)
#         driver.find_element(By.ID, "campo_descricao").send_keys("Descrição da subtarefa 1.")
#         time.sleep(1)
#         driver.find_element(By.TAG_NAME, "button").click()
#         time.sleep(2)

#         driver.find_element(By.LINK_TEXT, "Visualizar subtarefas").click()
#         time.sleep(1)

#         self.assertIn("Subtarefa Teste 1", driver.find_element(By.TAG_NAME, "body").text)
#         time.sleep(1)

#         # 8. Criar subtarefa sem nome
#         driver.find_element(By.LINK_TEXT, "+ Criar subtarefa").click()
#         time.sleep(1)
#         driver.find_element(By.ID, "campo_descricao").send_keys("Subtarefa sem nome")
#         time.sleep(1)
#         driver.find_element(By.TAG_NAME, "button").click()
#         time.sleep(2)
        
#         self.assertIn("O nome da subtarefa é obrigatório.", driver.find_element(By.TAG_NAME, "body").text)

#         # 9. Criar subtarefa duplicada
#         time.sleep(1)
#         driver.find_element(By.ID, "campo_nome").send_keys("Subtarefa Teste 1")
#         time.sleep(1)
#         driver.find_element(By.ID, "campo_descricao").send_keys("Outra descrição.")
#         time.sleep(1)
#         driver.find_element(By.TAG_NAME, "button").click()
#         time.sleep(2)

#         driver.find_element(By.LINK_TEXT, "Voltar para Subtarefas").click()
        
    





# class GerenciarSubtarefa(LiveServerTestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         options = Options()
#         if os.environ.get('GITHUB_ACTIONS') == 'true':
#             options.add_argument('--headless')
#             options.add_argument('--no-sandbox')
#             options.add_argument('--disable-dev-shm-usage')
#         cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#         cls.driver.implicitly_wait(10)

#     @classmethod
#     def tearDownClass(cls):
#         cls.driver.quit()
#         super().tearDownClass()

#     def test_fluxo_completo_usuario_objetivos(self):
#         driver = self.driver

#         # 1. Cadastro de novo usuário
#         driver.get(f'{self.live_server_url}/criar_usuario/')
#         driver.find_element(By.ID, "campo_username").send_keys("UsuarioNovoTeste")
#         driver.find_element(By.ID, "campo_email").send_keys("novousuario@teste.com")
#         driver.find_element(By.ID, "campo_senha").send_keys("senha321")
#         driver.find_element(By.TAG_NAME, "button").click()

#         self.assertEqual(driver.current_url, f'{self.live_server_url}/')

#         # 2. Login
#         driver.find_element(By.ID, "campo_email").send_keys("novousuario@teste.com")
#         driver.find_element(By.ID, "campo_senha").send_keys("senha321")
#         driver.find_element(By.TAG_NAME, "button").click()

#         WebDriverWait(driver, 10).until(EC.url_contains('/objetivos/'))
#         time.sleep(1)
        
#         # 10. Editar subtarefa
#         driver.find_element(By.LINK_TEXT, "Editar").click()
#         time.sleep(1)
#         campo_nome = driver.find_element(By.ID, "campo_nome")
#         campo_nome.clear()
#         campo_nome.send_keys("Subtarefa Editada")
#         time.sleep(1)
#         campo_descricao = driver.find_element(By.ID, "campo_descricao")
#         campo_descricao.clear()
#         campo_descricao.send_keys("Subtarefa editada descrição.")
#         time.sleep(1)
#         driver.find_element(By.CSS_SELECTOR, "select#campo_status option[value='em andamento']").click()
#         time.sleep(1)
#         driver.find_element(By.TAG_NAME, "button").click()
#         time.sleep(2)

#         driver.find_element(By.LINK_TEXT, "Visualizar subtarefas").click()
#         time.sleep(1)

#         self.assertIn("Subtarefa Editada", driver.find_element(By.TAG_NAME, "body").text)
#         time.sleep(1)

#         # 11. Deletar subtarefa
#         botao_deletar_sub = driver.find_element(By.XPATH, "//form/button[contains(text(), 'Deletar')]")
#         botao_deletar_sub.click()
#         time.sleep(1)
#         alerta = driver.switch_to.alert
#         alerta.accept()
#         time.sleep(2)

#         # 12. Deletar objetivo
#         botao_deletar_obj = driver.find_element(By.XPATH, "//form/button[contains(text(), 'Deletar')]")
#         botao_deletar_obj.click()
#         time.sleep(1)
#         alerta = driver.switch_to.alert
#         alerta.accept()
#         time.sleep(2)

#         self.assertNotIn("Objetivo Teste Editado", driver.find_element(By.TAG_NAME, "body").text)
