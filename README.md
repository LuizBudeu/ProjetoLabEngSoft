# ProjetoLabEngSoft

## Projeto de PCS3643 - Laboratório de Engenharia de Software 2022

Grupo 3:

- Felipe Batista Arrais (11804268)

- Gabriel Stephano Santos (11831999)

- Luiz Guilherme Budeu (11821639)

## Organização básica do projeto

O projeto web consta dentro da pasta `projeto` do repositório. Ele consiste em três partes principais: a pasta `projeto`, que contém as configurações globais do projeto (como o arquivo `settings.py`), a pasta `monitoramento`, que contém as configurações específicas da aplicação do sistema de monitoramento de voos (como os models e views), e a pasta `template`, que contém os arquivos HTML das páginas web.

## Roteiro de Execução e login do Projeto:

1. Criar pasta nova no computador (nome sugerido: "ProjetoLabEngSoft")

2. Entrar na pasta recém-criada e executar o seguinte comando no terminal:

```
git clone https://github.com/LuizBudeu/ProjetoLabEngSoft.git
```

3. Crie o ambiente virtual Python com os seguintes comandos:

```
python -m venv env
```

4. Ativar o ambiente virtual pelo terminal, dentro da pasta criada, utilizando o comando:

```
/env/Scripts/Activate.ps1
```

Caso haja algum erro no processo de rodar o comando, tal como o computador não conseguir achar o path para o arquivo Activate.ps1, você pode encontrá-lo manualmente na pasta 'Scripts' do ambiente virtual do repositório e copiar seu path absoluto. Feito isso, é possível colar diretamente o path para o terminal para ativar o ambiente.

5. Baixar as dependências do projeto com o comando:

```
pip install -r requirements.txt
```

6. Com o ambiente ativo, para começar o webserver, rodar o comando:

```
python manage.py runserver
```

7. Acesse o endereço `localhost:8000/login` em seu navegador de preferência para visualizar a página de login.

8. Para acessar a página principal, utilize um dos seguintes dados de login e senha a seguir. Cada um contém um tipo diferente de autorização para acessar as funcionalidades do Sistema:

| Nome de usuário | senha   | Acesso                     |
| --------------- | ------- | -------------------------- |
| luiz            | luiz    | Controle de Dados de Voos  |
| gabriel         | gabriel | Monitoramento de voos      |
| felipe          | felipe  | Gerar Relatórios           |
| admin           | admin   | Acesso geral               |

9. Após o login, está a tela "Home", contendo botões que direcionam a diferentes telas da interface do Sistema. Há também o botão "Sair", que retorna o usuário à tela de login.

## Roteiro de Execução de Testes (CRUD)

1. Seguir o passo-a-passo anterior (passo 1 até o passo 5) para clonar o repositório, criar e ativar o ambiente virtual e baixar as dependências.

2. Aplicar as migrações (criar banco de dados):

```
python manage.py migrate
```

3. Executar os testes:

```
python manage.py test
```
