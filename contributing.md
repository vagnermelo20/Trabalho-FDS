## Bem-vindo(a) ao projeto

Obrigado por considerar contribuir com este projeto! Estamos animados para ter você conosco. Este guia vai te ajudar a configurar o ambiente de desenvolvimento, seguir as boas práticas e enviar suas contribuições da melhor forma possível.


## Índice


- [Bem-vindo(a) ao projeto](#bem-vindoa-ao-projeto)
- [Rodar os testes](#rodar-os-testes)
- [Links uteis](#links-úteis)
- [Templates para contribuicao](#templates-para-contribuicao)
- [Submissao de mudancas](#submissao-de-mudancas)
- [Instrucoes passo a passo (How To)](#instrucoes-passo-a-passo-how-to)
  - [Como relatar um bug](#como-relatar-um-bug)
  - [Como corrigir um bug](#como-corrigir-um-bug)
  - [Como sugerir melhorias](#como-sugerir-melhorias)
  - [Convencoes de codigo e estilo](#convencoes-de-codigo-e-estilo)
- [Codigo de Conduta](#codigo-de-conduta)
- [Reconhecimento](#reconhecimento)
- [Quem somos](#quem-somos)
- [Onde obter ajuda](#onde-obter-ajuda)



## Rodar os testes

Este projeto utiliza testes automatizados com o **Selenium**, simulando interações reais com o navegador.

### Como executar os testes:

1.  Certifique-se de que as dependências estão instaladas:

    ```bash
    pip install -r requirements.txt
    ```

2.  execute os testes com
    python manage.py test

---

 

  

## Links úteis

### 📂 Estrutura do Projeto


- **apps**  
  - Login: [`login/`](./login/)
  - Objetivos: [`objetivos`](./objetivos)  

- **Projeto**  
  - Projeto: [`projeto/`](./projeto/)

- **Templates (HTML)**  
  - Login: [`login/templates/login/`](./login/templates/login/)  
    - `base.html`, `criar_usuario.html`, `logar.html`  
  - Objetivos: [`objetivos/templates/objetivos/`](./objetivos/templates/objetivos/)  
    - `criar_objetivo.html`, `criar_tarefa_adm.html`, `visualizar_grupos_adm.html`, etc.

- **Testes**  
  - Módulo `login`: [`login/tests.py`](./login/tests.py)  
  - Módulo `objetivos`: [`objetivos/tests.py`](./objetivos/tests.py)

- **Ambiente de desenvolvimento**  
  As instruções completas estão no [`README.md`](./README.md)

--- 
  
### 📑 Templates para contribuição

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
