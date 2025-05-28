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


# Teste 1
class Test1_GerenciarObjetivo(LiveServerTestCase):
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

        # 2. Login - Usando WebDriverWait com retries para garantir estabilidade
        # Aguardar até que o redirecionamento para a página de login esteja completo
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_email"))
        )
        
        # Uma pausa breve para garantir a estabilidade da página
        time.sleep(1)
        
        # Localizar o campo email novamente (para evitar StaleElementReferenceException)
        campo_email = driver.find_element(By.ID, "campo_email")
        campo_email.clear()  # Limpar o campo antes de digitar
        campo_email.send_keys("novousuario@teste.com")
        
        # Localizar o campo senha
        campo_senha = driver.find_element(By.ID, "campo_senha") 
        campo_senha.clear()  # Limpar o campo antes de digitar
        campo_senha.send_keys("senha321")
        
        # Clicar no botão de login
        driver.find_element(By.TAG_NAME, "button").click()

        # Aguardar o redirecionamento para a página de objetivos
        WebDriverWait(driver, 10).until(EC.url_contains('/objetivos/'))
        time.sleep(1)

        # 3. Criar objetivo
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "+ Criar tarefas"))
        ).click()
        time.sleep(1)
        
        campo_nome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome"))
        )
        campo_nome.send_keys("Objetivo Teste 1")
        
        campo_descricao = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_descricao"))
        )
        campo_descricao.send_keys("Descrição do objetivo 1.")
        
        campo_urgencia = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_urgencia"))
        )
        campo_urgencia.send_keys("2")
        
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "📋 Ver todos os objetivos"))
        ).click()
        time.sleep(1)

        # 4. Criar objetivo sem nome
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "+ Criar tarefas"))
        ).click()
        time.sleep(1)
        
        campo_descricao = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_descricao"))
        )
        campo_descricao.send_keys("Descrição sem título.")
        
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        # Verificar mensagem de erro
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "É necessário preencher o nome do objetivo.")
        )
        time.sleep(1)

        # 5. Criar objetivo duplicado
        campo_nome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome"))
        )
        campo_nome.send_keys("Objetivo Teste 1")
        
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        # Verificar mensagem de erro
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Você já tem uma tarefa com este nome.")
        )
        time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()
        time.sleep(1)


# Teste 2

class Test2_GerenciarObjetivo(LiveServerTestCase):
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

        # 2. Login - Usando WebDriverWait com retries para garantir estabilidade
        # Aguardar até que o redirecionamento para a página de login esteja completo
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_email"))
        )
        
        # Uma pausa breve para garantir a estabilidade da página
        time.sleep(1)
        
        # Localizar o campo email novamente (para evitar StaleElementReferenceException)
        campo_email = driver.find_element(By.ID, "campo_email")
        campo_email.clear()  # Limpar o campo antes de digitar
        campo_email.send_keys("novousuario@teste.com")
        
        # Localizar o campo senha
        campo_senha = driver.find_element(By.ID, "campo_senha") 
        campo_senha.clear()  # Limpar o campo antes de digitar
        campo_senha.send_keys("senha321")
        
        # Clicar no botão de login
        driver.find_element(By.TAG_NAME, "button").click()

        # Aguardar o redirecionamento para a página de objetivos
        WebDriverWait(driver, 10).until(EC.url_contains('/objetivos/'))
        time.sleep(1)

        # 3. Criar objetivo 1
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "+ Criar tarefas"))
        ).click()
        time.sleep(1)
        
        campo_nome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome"))
        )
        campo_nome.send_keys("Objetivo Teste 1")
        
        campo_descricao = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_descricao"))
        )
        campo_descricao.send_keys("Descrição do objetivo 1.")
        
        campo_urgencia = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_urgencia"))
        )
        campo_urgencia.send_keys("2")
        
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "📋 Ver todos os objetivos"))
        ).click()
        time.sleep(1)

        # 4. Criar objetivo 2
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "+ Criar tarefas"))
        ).click()
        time.sleep(1)
        
        campo_nome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome"))
        )
        campo_nome.send_keys("Objetivo Teste 2")
        
        campo_descricao = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_descricao"))
        )
        campo_descricao.send_keys("Descrição do objetivo 2.")
        
        campo_urgencia = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_urgencia"))
        )
        campo_urgencia.send_keys("2")
        
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "📋 Ver todos os objetivos"))
        ).click()
        time.sleep(1)
        
        # 5. Editar objetivo
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Editar"))
        ).click()
        time.sleep(1)
        
        campo_nome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome"))
        )
        campo_nome.clear()
        campo_nome.send_keys("Objetivo Teste Editado")
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.TAG_NAME, "button"))
        ).click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Editar"))
        ).click()
        time.sleep(1)
        
        campo_nome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome"))
        )
        campo_nome.clear()
        campo_nome.send_keys("Objetivo Teste 2")
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.TAG_NAME, "button"))
        ).click()
        time.sleep(2)
        
        # Verificar mensagem de erro
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), 
                                           "Você já tem uma tarefa com este nome. Por favor, escolha um nome diferente.")
        )
        
        campo_nome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome"))
        )
        campo_nome.clear()
        time.sleep(1)
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.TAG_NAME, "button"))
        ).click()
        time.sleep(2)
        
        # Verificar mensagem de erro
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), 
                                           "É necessário preencher o nome do objetivo.")
        )
        time.sleep(1)
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()
        time.sleep(1)

        # 12. Deletar objetivo
        botao_deletar_obj = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//form/button[contains(text(), 'Deletar')]"))
        )
        botao_deletar_obj.click()
        time.sleep(1)
        
        alerta = driver.switch_to.alert
        alerta.accept()
        time.sleep(2)
        
        botao_deletar_obj = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//form/button[contains(text(), 'Deletar')]"))
        )
        botao_deletar_obj.click()
        time.sleep(1)
        
        alerta = driver.switch_to.alert
        alerta.accept()
        time.sleep(2)

# Teste 3
class Test3_VerPrioridade(LiveServerTestCase):
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

    def test_Prioridades(self):
        driver = self.driver

        # 1. Cadastro de novo usuário
        driver.get(f'{self.live_server_url}/criar_usuario/')
        driver.find_element(By.ID, "campo_username").send_keys("UsuarioNovoTeste")
        driver.find_element(By.ID, "campo_email").send_keys("novousuario@teste.com")
        driver.find_element(By.ID, "campo_senha").send_keys("senha321")
        driver.find_element(By.TAG_NAME, "button").click()

        # 2. Login - Usando WebDriverWait com retries para garantir estabilidade
        # Aguardar até que o redirecionamento para a página de login esteja completo
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_email"))
        )
        
        # Uma pausa breve para garantir a estabilidade da página
        time.sleep(1)
        
        # Localizar o campo email novamente (para evitar StaleElementReferenceException)
        campo_email = driver.find_element(By.ID, "campo_email")
        campo_email.clear()  # Limpar o campo antes de digitar
        campo_email.send_keys("novousuario@teste.com")
        
        # Localizar o campo senha
        campo_senha = driver.find_element(By.ID, "campo_senha") 
        campo_senha.clear()  # Limpar o campo antes de digitar
        campo_senha.send_keys("senha321")
        
        # Clicar no botão de login
        driver.find_element(By.TAG_NAME, "button").click()

        # Aguardar o redirecionamento para a página de objetivos
        WebDriverWait(driver, 10).until(EC.url_contains('/objetivos/'))
        time.sleep(1)

        # Verificar filtros de prioridade
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Alta/Nível 3"))
        ).click()
        time.sleep(1)
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Todas"))
        ).click()
        time.sleep(1)

       # 3. Criar objetivo 1
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "+ Criar tarefas"))
        ).click()
        time.sleep(1)
        
        campo_nome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome"))
        )
        campo_nome.send_keys("Objetivo Prioridade 1")
        
        campo_descricao = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_descricao"))
        )
        campo_descricao.send_keys("Descrição do objetivo 1.")
        
        campo_urgencia = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_urgencia"))
        )
        campo_urgencia.send_keys("1")
        
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "📋 Ver todos os objetivos"))
        ).click()
        time.sleep(1)

        # Criar objetivo 2
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "+ Criar tarefas"))
        ).click()
        time.sleep(1)
        
        campo_nome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome"))
        )
        campo_nome.send_keys("Objetivo Prioridade 3")
        
        campo_descricao = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_descricao"))
        )
        campo_descricao.send_keys("Descrição do objetivo 3.")
        
        campo_urgencia = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_urgencia"))
        )
        campo_urgencia.send_keys("3")
        
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "📋 Ver todos os objetivos"))
        ).click()
        time.sleep(1)
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Alta/Nível 3"))
        ).click()
        time.sleep(1)

# Teste 4
class Test4_CriarSubtarefa(LiveServerTestCase):
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

    def test_criarSubtarefa(self):
        driver = self.driver

        # 1. Cadastro de novo usuário
        driver.get(f'{self.live_server_url}/criar_usuario/')
        driver.find_element(By.ID, "campo_username").send_keys("UsuarioNovoTeste")
        driver.find_element(By.ID, "campo_email").send_keys("novousuario@teste.com")
        driver.find_element(By.ID, "campo_senha").send_keys("senha321")
        driver.find_element(By.TAG_NAME, "button").click()

        # 2. Login - Usando WebDriverWait com retries para garantir estabilidade
        # Aguardar até que o redirecionamento para a página de login esteja completo
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_email"))
        )
        
        # Uma pausa breve para garantir a estabilidade da página
        time.sleep(1)
        
        # Localizar o campo email novamente (para evitar StaleElementReferenceException)
        campo_email = driver.find_element(By.ID, "campo_email")
        campo_email.clear()  # Limpar o campo antes de digitar
        campo_email.send_keys("novousuario@teste.com")
        
        # Localizar o campo senha
        campo_senha = driver.find_element(By.ID, "campo_senha") 
        campo_senha.clear()  # Limpar o campo antes de digitar
        campo_senha.send_keys("senha321")
        
        # Clicar no botão de login
        driver.find_element(By.TAG_NAME, "button").click()

        # Aguardar o redirecionamento para a página de objetivos
        WebDriverWait(driver, 10).until(EC.url_contains('/objetivos/'))
        time.sleep(1)

       # 3. Criar objetivo 1
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "+ Criar tarefas"))
        ).click()
        time.sleep(1)
        
        campo_nome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome"))
        )
        campo_nome.send_keys("Objetivo Teste 1")
        
        campo_descricao = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_descricao"))
        )
        campo_descricao.send_keys("Descrição do objetivo 1.")
        
        campo_urgencia = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_urgencia"))
        )
        campo_urgencia.send_keys("2")
        
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "📋 Ver todos os objetivos"))
        ).click()
        time.sleep(1)
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar subtarefas"))
        ).click()
        time.sleep(1)


        # 4. Criar subtarefa
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "+ Criar subtarefa"))
        ).click()
        time.sleep(1)
        
        campo_nome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome"))
        )
        campo_nome.send_keys("Subtarefa Teste 1")
        
        campo_descricao = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_descricao"))
        )
        campo_descricao.send_keys("Descrição da subtarefa 1.")
        
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar subtarefas"))
        ).click()
        time.sleep(1)

        # Verificar se subtarefa foi criada
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Subtarefa Teste 1")
        )
        time.sleep(1)

        # 8. Criar subtarefa sem nome
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "+ Criar subtarefa"))
        ).click()
        time.sleep(1)
        
        campo_descricao = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_descricao"))
        )
        campo_descricao.send_keys("Subtarefa sem nome")
        
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        
        # Verificar mensagem de erro
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "O nome da subtarefa é obrigatório.")
        )

        # 9. Criar subtarefa duplicada
        time.sleep(1)
        
        campo_nome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome"))
        )
        campo_nome.send_keys("Subtarefa Teste 1")
        
        campo_descricao = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_descricao"))
        )
        campo_descricao.clear()
        campo_descricao.send_keys("Outra descrição.")
        
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Voltar para Subtarefas"))
        ).click()
        
# Teste 5
class Test5_GerenciarSubtarefa(LiveServerTestCase):
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

    def test_fluxo_completo_usuario_objetivos(self):
        driver = self.driver

        # 1. Cadastro de novo usuário
        driver.get(f'{self.live_server_url}/criar_usuario/')
        driver.find_element(By.ID, "campo_username").send_keys("UsuarioNovoTeste")
        driver.find_element(By.ID, "campo_email").send_keys("novousuario@teste.com")
        driver.find_element(By.ID, "campo_senha").send_keys("senha321")
        driver.find_element(By.TAG_NAME, "button").click()

        # 2. Login - Usando WebDriverWait com retries para garantir estabilidade
        # Aguardar até que o redirecionamento para a página de login esteja completo
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_email"))
        )
        
        # Uma pausa breve para garantir a estabilidade da página
        time.sleep(1)
        
        # Localizar o campo email novamente (para evitar StaleElementReferenceException)
        campo_email = driver.find_element(By.ID, "campo_email")
        campo_email.clear()  # Limpar o campo antes de digitar
        campo_email.send_keys("novousuario@teste.com")
        
        # Localizar o campo senha
        campo_senha = driver.find_element(By.ID, "campo_senha") 
        campo_senha.clear()  # Limpar o campo antes de digitar
        campo_senha.send_keys("senha321")
        
        # Clicar no botão de login
        driver.find_element(By.TAG_NAME, "button").click()

        # Aguardar o redirecionamento para a página de objetivos
        WebDriverWait(driver, 10).until(EC.url_contains('/objetivos/'))
        time.sleep(1)

        
       # 3. Criar objetivo
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "+ Criar tarefas"))
        ).click()
        time.sleep(1)
        
        campo_nome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome"))
        )
        campo_nome.send_keys("Objetivo Teste 1")
        
        campo_descricao = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_descricao"))
        )
        campo_descricao.send_keys("Descrição do objetivo 1.")
        
        campo_urgencia = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_urgencia"))
        )
        campo_urgencia.send_keys("2")
        
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "📋 Ver todos os objetivos"))
        ).click()
        time.sleep(1)
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar subtarefas"))
        ).click()
        time.sleep(1)


        # 4. Criar subtarefa 1
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "+ Criar subtarefa"))
        ).click()
        time.sleep(1)
        
        campo_nome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome"))
        )
        campo_nome.send_keys("Subtarefa Teste 1")
        
        campo_descricao = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_descricao"))
        )
        campo_descricao.send_keys("Descrição da subtarefa 1.")
        
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        # 5. Criar subtarefa 2
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar subtarefas"))
        ).click()
        time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "+ Criar subtarefa"))
        ).click()
        time.sleep(1)
        
        campo_nome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome"))
        )
        campo_nome.send_keys("Subtarefa Teste 2")
        
        campo_descricao = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_descricao"))
        )
        campo_descricao.send_keys("Descrição da subtarefa 2.")
        
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        
        # 6. Editar subtarefa
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar subtarefas"))
        ).click()
        time.sleep(1)
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Editar"))
        ).click()
        time.sleep(1)
        
        campo_nome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome"))
        )
        campo_nome.clear()
        campo_nome.send_keys("Subtarefa Editada")
        
        campo_descricao = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_descricao"))
        )
        campo_descricao.clear()
        campo_descricao.send_keys("Subtarefa editada descrição.")
        
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        # 7. Editar subtarefa sem nome
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar subtarefas"))
        ).click()
        time.sleep(1)
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Editar"))
        ).click()
        time.sleep(1)
        
        campo_nome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome"))
        )
        campo_nome.clear()
        
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        
        # Verificar mensagem de erro
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "O nome da subtarefa é obrigatório.")
        )
        time.sleep(1)

        # 8. Editar subtarefa duplicada
        campo_nome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome"))
        )
        campo_nome.clear()
        campo_nome.send_keys("Subtarefa Teste 2")
        
        driver.find_element(By.TAG_NAME, "button").click()
        
        # Verificar mensagem de erro
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), 
                                           "Já existe outra subtarefa com esse nome para este objetivo.")
        )
        time.sleep(1)
        
        # 9. Deletar subtarefa
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Voltar para Subtarefas"))
        ).click()
        time.sleep(1)
        
        botao_deletar_sub = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//form/button[contains(text(), 'Deletar')]"))
        )
        botao_deletar_sub.click()
        time.sleep(1)
        
        alerta = driver.switch_to.alert
        alerta.accept()
        time.sleep(2)
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar subtarefas"))
        ).click()
        time.sleep(1)

# Teste 6

class Test6_CriarGrupo(LiveServerTestCase):
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

    def test_fluxo_completo_usuario_objetivos(self):
        driver = self.driver

        # 1. Cadastro de novo usuário
        driver.get(f'{self.live_server_url}/criar_usuario/')
        driver.find_element(By.ID, "campo_username").send_keys("UsuarioNovoTeste")
        driver.find_element(By.ID, "campo_email").send_keys("novousuario@teste.com")
        driver.find_element(By.ID, "campo_senha").send_keys("senha321")
        driver.find_element(By.TAG_NAME, "button").click()


        # 2. Login - Usando WebDriverWait com retries para garantir estabilidade
        # Aguardar até que o redirecionamento para a página de login esteja completo
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_email"))
        )
        
        # Uma pausa breve para garantir a estabilidade da página
        time.sleep(1)
        
        # Localizar o campo email novamente (para evitar StaleElementReferenceException)
        campo_email = driver.find_element(By.ID, "campo_email")
        campo_email.clear()  # Limpar o campo antes de digitar
        campo_email.send_keys("novousuario@teste.com")
        
        # Localizar o campo senha
        campo_senha = driver.find_element(By.ID, "campo_senha") 
        campo_senha.clear()  # Limpar o campo antes de digitar
        campo_senha.send_keys("senha321")
        
        # Clicar no botão de login
        driver.find_element(By.TAG_NAME, "button").click()

        # Aguardar o redirecionamento para a página de objetivos
        WebDriverWait(driver, 10).until(EC.url_contains('/objetivos/'))
        time.sleep(1)

        # 3. Criar grupo com titulo e descrição
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Criar um grupo"))
        ).click()
        time.sleep(1)
        
        campo_nome_grupo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome_grupo"))
        )
        campo_nome_grupo.send_keys("grupo 1")
        
        campo_senha = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "senha"))
        )
        campo_senha.send_keys("senha321")
        
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()
        time.sleep(1)

        # 4. Criar grupo sem nome
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Criar um grupo"))
        ).click()
        time.sleep(1)
        
        campo_senha = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "senha"))
        )
        campo_senha.send_keys("senha321")
        
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        
        # Verificar mensagem de erro
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "O nome do grupo é obrigatório.")
        )
        time.sleep(1)

        # 5. Criar grupo com nome duplicado
        campo_nome_grupo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome_grupo"))
        )
        campo_nome_grupo.send_keys("grupo 1")
        
        campo_senha = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "senha"))
        )
        campo_senha.send_keys("senha321")
        
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        
        # Verificar mensagem de erro
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Esse grupo já existe")
        )
        time.sleep(1)
        
        # 6. Criar um grupo sem senha
        campo_nome_grupo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_nome_grupo"))
        )
        campo_nome_grupo.clear()
        campo_nome_grupo.send_keys("grupo 2")
        
        campo_senha = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "senha"))
        )
        campo_senha.clear()
        
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        
        # Verificar mensagem de erro
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "A senha do grupo é obrigatória.")
        )
        time.sleep(1)
