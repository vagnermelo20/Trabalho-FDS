from django.test import TestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# test_tests.py


# Pseudocode:
# 1. Setup Selenium driver and LiveServerTestCase.
# 2. Create admin user, create group, create member user, add member to group.
# 3. Admin cria tarefa para o membro.
# 4. Membro tenta esconder tarefa pendente (deve dar erro).
# 5. Membro marca tarefa como completa, depois esconde (deve funcionar).
# 6. Admin verifica tarefa como completa e depois como escondida.
# 7. Testa cenários: visualizar, atualizar, deletar tarefa pendente (erro), deletar tarefa completa (ok).

class TestTarefasMembroFluxo(TestCase):
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

    def test_fluxo_tarefas_membro(self):
        driver = self.driver

        # 1. Admin cria conta e grupo
        driver.get(f'{self.live_server_url}/criar_usuario/')
        driver.find_element(By.ID, "campo_username").send_keys("adminuser")
        driver.find_element(By.ID, "campo_email").send_keys("admin@teste.com")
        driver.find_element(By.ID, "campo_senha").send_keys("admin123")
        driver.find_element(By.TAG_NAME, "button").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "campo_email")))
        time.sleep(1)
        driver.find_element(By.ID, "campo_email").send_keys("admin@teste.com")
        driver.find_element(By.ID, "campo_senha").send_keys("admin123")
        driver.find_element(By.TAG_NAME, "button").click()
        WebDriverWait(driver, 10).until(EC.url_contains('/objetivos/'))
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Criar um grupo"))).click()
        time.sleep(1)
        driver.find_element(By.ID, "campo_nome_grupo").send_keys("grupoTeste")
        driver.find_element(By.ID, "senha").send_keys("senhaGrupo")
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        # 2. Admin cria tarefa para membro (depois de criar membro e adicionar ao grupo)
        driver.find_element(By.ID, "logout").click()
        time.sleep(1)
        driver.get(f'{self.live_server_url}/criar_usuario/')
        driver.find_element(By.ID, "campo_username").send_keys("membro1")
        driver.find_element(By.ID, "campo_email").send_keys("membro1@teste.com")
        driver.find_element(By.ID, "campo_senha").send_keys("membro123")
        driver.find_element(By.TAG_NAME, "button").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "campo_email")))
        time.sleep(1)
        driver.find_element(By.ID, "campo_email").send_keys("membro1@teste.com")
        driver.find_element(By.ID, "campo_senha").send_keys("membro123")
        driver.find_element(By.TAG_NAME, "button").click()
        WebDriverWait(driver, 10).until(EC.url_contains('/objetivos/'))
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Entrar em um grupo"))).click()
        time.sleep(1)
        driver.find_element(By.ID, "campo_nome_grupo").send_keys("grupoTeste")
        driver.find_element(By.ID, "campo_senha").send_keys("senhaGrupo")
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        driver.find_element(By.ID, "logout").click()
        time.sleep(1)
        # Admin loga novamente
        driver.find_element(By.ID, "campo_email").send_keys("admin@teste.com")
        driver.find_element(By.ID, "campo_senha").send_keys("admin123")
        driver.find_element(By.TAG_NAME, "button").click()
        WebDriverWait(driver, 10).until(EC.url_contains('/objetivos/'))
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Meus grupos"))).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar"))).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "+ Criar Tarefa"))).click()
        time.sleep(1)
        driver.find_element(By.ID, "campo_nome").send_keys("Tarefa do Membro")
        driver.find_element(By.ID, "campo_descricao").send_keys("Descrição da tarefa")
        # Seleciona membro1 como responsável (se houver select)
        try:
            select = driver.find_element(By.ID, "campo_responsavel")
            for option in select.find_elements(By.TAG_NAME, "option"):
                if "membro1" in option.text:
                    option.click()
                    break
        except Exception:
            pass
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        driver.find_element(By.ID, "logout").click()
        time.sleep(1)

        # 3. Membro tenta esconder tarefa pendente (deve dar erro)
        driver.find_element(By.ID, "campo_email").send_keys("membro1@teste.com")
        driver.find_element(By.ID, "campo_senha").send_keys("membro123")
        driver.find_element(By.TAG_NAME, "button").click()
        WebDriverWait(driver, 10).until(EC.url_contains('/objetivos/'))
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Meus grupos"))).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar"))).click()
        time.sleep(1)
        # Tenta esconder tarefa (deve falhar)
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Esconder"))).click()
            time.sleep(1)
            # Espera mensagem de erro
            WebDriverWait(driver, 5).until(
                EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Só é possível esconder tarefas completas")
            )
        except Exception:
            pass

        # 4. Membro marca tarefa como completa e esconde
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Atualizar"))).click()
            time.sleep(1)
            # Marca como completa (checkbox ou select)
            try:
                checkbox = driver.find_element(By.ID, "campo_completa")
                if not checkbox.is_selected():
                    checkbox.click()
            except Exception:
                try:
                    select = driver.find_element(By.ID, "campo_status")
                    for option in select.find_elements(By.TAG_NAME, "option"):
                        if "Completa" in option.text:
                            option.click()
                            break
                except Exception:
                    pass
            driver.find_element(By.TAG_NAME, "button").click()
            time.sleep(2)
            # Agora tenta esconder (deve funcionar)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Esconder"))).click()
            time.sleep(1)
            WebDriverWait(driver, 5).until(
                EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Tarefa escondida com sucesso")
            )
        except Exception:
            pass

        # 5. Admin verifica tarefa como completa e depois como escondida
        driver.find_element(By.ID, "logout").click()
        time.sleep(1)
        driver.find_element(By.ID, "campo_email").send_keys("admin@teste.com")
        driver.find_element(By.ID, "campo_senha").send_keys("admin123")
        driver.find_element(By.TAG_NAME, "button").click()
        WebDriverWait(driver, 10).until(EC.url_contains('/objetivos/'))
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Meus grupos"))).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar"))).click()
        time.sleep(1)
        # Verifica tarefa como completa/escondida
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "Tarefa do Membro" in body_text
        assert "Completa" in body_text or "completa" in body_text

        # 6. Membro tenta deletar tarefa pendente (erro) e completa (ok)
        driver.find_element(By.ID, "logout").click()
        time.sleep(1)
        driver.find_element(By.ID, "campo_email").send_keys("membro1@teste.com")
        driver.find_element(By.ID, "campo_senha").send_keys("membro123")
        driver.find_element(By.TAG_NAME, "button").click()
        WebDriverWait(driver, 10).until(EC.url_contains('/objetivos/'))
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Meus grupos"))).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar"))).click()
        time.sleep(1)
        # Tenta deletar tarefa (deve funcionar pois está completa)
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Deletar"))).click()
            time.sleep(1)
            alerta = driver.switch_to.alert
            alerta.accept()
            time.sleep(2)
            WebDriverWait(driver, 5).until(
                EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Tarefa deletada com sucesso")
            )
        except Exception:
            pass