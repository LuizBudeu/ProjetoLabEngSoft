# ProjetoLabEngSoft


## Projeto de PCS3643 - Laboratório de Engenharia de Software 2022
Grupo 3:

- Felipe Batista Arrais   (11804268)

- Gabriel Stephano Santos (11831999)

- Luiz Guilherme Budeu    (11821639)


## Roteiro de Execução do Projeto:
1. Criar pasta nova no computador (nome sugerido: "ProjetoLabEngSoft")


2. Entrar na pasta recém-criada e executar o seguinte comando no terminal:
```
git clone https://github.com/LuizBudeu/ProjetoLabEngSoft.git
```
Esse comando instala o ambiente virtual Python dentro da pasta criada.


3. Entre na pasta ```projeto``` com o seguinte comando:
```
cd projeto
```


4. Ativar o ambiente virtual pelo terminal, dentro da pasta criada, utilizando o comando:
```
/bin/Activate.ps1
```
Caso haja algum erro no processo de rodar o comando, tal como o computador não conseguir achar o path para o arquivo Activate.ps1, você pode encontrá-lo manualmente na pasta 'bin' do repositório e copiar seu path absoluto. Feito isso, é possível colar diretamente o path para o terminal para ativar o ambiente.


5. Com o ambiente ativo, para começar o webserver, rodar o comando:
```
python manage.py runserver
```


6. Acesse o endereço ```localhost:8000/FIRST``` em seu navegador de preferência para visualizar a página. 


## Organização básica do projeto


O projeto web consta dentro da pasta ```projeto``` do repositório. Ele consiste em três partes principais: a pasta ```projeto```, que contém as configurações globais do projeto (como o arquivo ```settings.py```), a pasta ```monitoramento```, que contém as configurações específicas da aplicação do sistema de monitoramento de voos (como os models e views), e a pasta ```template```, que contém os arquivos HTML das páginas web.