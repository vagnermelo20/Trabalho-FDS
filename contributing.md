## Bem-vindo(a) ao projeto

Obrigado por considerar contribuir com este projeto! Estamos animados para ter você conosco. Este guia vai te ajudar a configurar o ambiente de desenvolvimento, seguir as boas práticas e enviar suas contribuições da melhor forma possível.


## Índice

- [Bem-vindo(a) ao projeto](#bem-vindoa-ao-projeto)
- [Executaveis](#executaveis)
  - [Criar ambiente virtual](#criar-ambiente-virtual)
  - [Instalar dependências](#instalar-dependencias)
  - [Aplicar migrações](#aplicar-migracoes)
  - [Rodar o servidor local](#rodar-o-servidor-local)
  - [Executar os testes automatizados](#executar-os-testes-automatizados)
- [Links uteis](#links-úteis)
- [Templates para contribuicao](#templates-para-contribuição)
- [Submissao de mudancas](#submissão-de-mudanças)
- [Instrucoes passo a passo (How To)](#instruções-passo-a-passo-how-to)
  - [Como relatar um bug](#como-relatar-um-bug)
  - [Como corrigir um bug](#como-corrigir-um-bug)
  - [Como sugerir melhorias](#como-sugerir-melhorias)
  - [Convencoes de codigo e estilo](#convenções-de-código-e-estilo)
- [Codigo de Conduta](#código-de-conduta)
- [Reconhecimento](#reconhecimento)
- [Quem somos](#quem-somos)
- [Onde obter ajuda](#onde-obter-ajuda)




## Executáveis

Este projeto utiliza o framework Django e testes automatizados com o **Selenium**, simulando interações reais com o navegador.

### 1. Criar ambiente virtual

#### 💻 Windows (CMD ou PowerShell):

python -m venv venv
venv\Scripts\activate

#### 🐧 Linux / macOS:

python3 -m venv venv
source venv/bin/activate


---

### 2. Instalar dependências

Certifique-se de estar dentro do ambiente virtual, então rode:

pip install -r requirements.txt

---

### 3. Aplicar migrações (caso necessário)

python manage.py migrate

---

### 4. Rodar o servidor local

python manage.py runserver


Acesse no navegador: `http://127.0.0.1:8000/`

---

### 5. Executar os testes automatizados

python manage.py test

Os testes utilizam o Selenium e abrem um navegador real. Certifique-se de ter o **`webdriver-manager`** instalado e funcional.


 

  

## Links úteis

### 📂 Estrutura do Projeto


- **apps**  
  - Login: [`login`](./login/)
  - Objetivos: [`objetivos`](./objetivos)  

- **Projeto**  
  - Projeto: [`projeto`](./projeto/)

- **Templates (HTML)**  
  - Login: [`login/templates/login`](./login/templates/login/)  
  - Objetivos: [`objetivos/templates/objetivos`](./objetivos/templates/objetivos/)  

- **Testes**  
  - Módulo `login`: [`login/tests.py`](./login/tests.py)  
  - Módulo `objetivos`: [`objetivos/tests.py`](./objetivos/tests.py)

- **Ambiente de desenvolvimento**  
  As instruções completas estão em - [Executaveis](#executaveis)
--- 
  
### Templates para contribuição

- [Template para relatório de bugs](./.github/ISSUE_TEMPLATE/bug_report.md) *(adicione este arquivo se ainda não existir)*
- [Template para sugestão de melhorias](./.github/ISSUE_TEMPLATE/enhancement.md) *(adicione este arquivo se ainda não existir)*

---

### Submissão de mudanças

Contribuições são bem-vindas via pull requests:

1. Crie um fork do projeto
2. Crie uma branch com sua mudança
3. Envie um [Pull Request](https://github.com/vagnermelo20/Trabalho-FDS/pulls)
4. Aguarde revisão


## Instruções passo a passo (How To)

### Como relatar um bug

Se você encontrou um problema no sistema, siga este processo:

1. **Verifique se o bug já foi relatado** nas [issues existentes](https://github.com/vagnermelo20/Trabalho-FDS/issues).
2. Caso não tenha sido reportado:
   - Acesse a aba de [Issues](https://github.com/vagnermelo20/Trabalho-FDS/issues/new?assignees=&labels=bug&template=bug_report.md)
   - Use o [template de bug report](./.github/ISSUE_TEMPLATE/bug_report.md)
   - Descreva claramente:
     - O que você esperava que acontecesse
     - O que aconteceu de fato
     - Como reproduzir o erro passo a passo
     - Prints de tela e logs, se possível

---

### Como corrigir um bug

Se quiser tentar corrigir um bug:

1. Comente na issue que você está assumindo a tarefa.
2. Faça um fork e crie uma branch específica, ex:  
   `fix/erro-login-usuarios`
3. Ao resolver, envie um Pull Request mencionando a issue com `Closes #número-da-issue`.
4. Aguarde a revisão.

> Recomendação: bugs mais simples incluem erros de formatação, redirecionamento incorreto, ou falhas em validações de formulário.

---

### Como sugerir melhorias

1. Verifique se já há sugestões similares nas [issues](https://github.com/vagnermelo20/Trabalho-FDS/issues?q=is%3Aissue+label%3Aenhancement).
2. Caso seja algo novo:
   - Crie uma nova issue com o label `enhancement`
   - Use o [template de sugestões](./.github/ISSUE_TEMPLATE/enhancement.md)
   - Seja o mais específico possível:
     - Qual funcionalidade propõe
     - Qual problema resolve
     - Impacto esperado
3. Se possível, mencione exemplos de como outros projetos abordam a mesma ideia.

---

### Convenções de código e estilo

**Commits:**
- Use o tempo verbal no **presente do indicativo**
- Limite a primeira linha a no máximo **72 caracteres**
- Não use emojis
- Referencie issues com `#ID`, ex: `Corrige erro de login (#45)`















## Código de Conduta

Todos os contribuidores devem seguir um comportamento respeitoso, colaborativo e inclusivo. Esperamos que todos ajam com empatia, profissionalismo e paciência.



## Reconhecimento

Agradecemos profundamente a todas as pessoas que dedicam seu tempo e esforço para melhorar este projeto. Reconhecemos as contribuições por:

- Daniel Andrade Ferreira Silva
- David Magalhães Porto Oliveira
- Leonardo de Queiroz Chaves
- Tomás de Aquino Vieira Jamacaru
- Vagner Montenegro de Melo
- Willian de Souza Bezerra

## Quem somos

Este projeto foi idealizado e é mantido por:

- Daniel Andrade Ferreira Silva
- David Magalhães Porto Oliveira
- Leonardo de Queiroz Chaves
- Tomás de Aquino Vieira Jamacaru
- Vagner Montenegro de Melo
- Willian de Souza Bezerra

com o intuito de criar uma aplicação de um gerenciador de tarefas para o nosso segundo periodo do curso de  **FDS (Fundamentos de Desenvolvimento de Software) da turma 2A da Cesar School do curso de Ciência da Computação**

---

## Onde obter ajuda

Se você tiver dúvidas ou dificuldades para contribuir:

- Consulte as [Issues](https://github.com/vagnermelo20/Trabalho-FDS/issues)
- Veja a seção de [Discussões](https://github.com/vagnermelo20/Trabalho-FDS/discussions)
- Fique à vontade para sugerir melhorias na documentação

Queremos tornar sua experiência a melhor possível, então não hesite em nos procurar!
