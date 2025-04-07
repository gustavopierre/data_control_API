# Data Control API
## Introducao
A aplicação Data Control teve origem como MVP da Sprint **Desenvolvimento Full Stack Básico** e foi complementada para atender o MVP da Sprint **Arquitetura de Software** do curso de Pós-Graduação em Engenharia de Software da PUC-Rio.
A aplicacao controla os dados utilizados para serem camadas de mapas em softwares de GIS na empresa em que trabalho. Identifiquei, ha algum tempo, que os dados sao dinamicos e os mapas devem ser o mais atualizados possivel. Nao existia uma politica de frequencia de atualizacao desses dados. Com a aplicacao DataControl, cada dado recebe uma informacao de qual a frequencia, em dias, que cada dado deve ser atualizado. Na versao atual, ele mostra na lista de dados, em quantos dias cada dado deve ser checado quanto a existencia de atualizacao. Quando o dado é do tipo Web Feature Server (WFS), o dado do bounding box dos dados geográficos é obtido via API REST externa, cujo link consta como um dos campos de informação daquele dado. A arquitetura da aplicação é representada visualmente na figura abaixo:

<p align="center">
  <img src="img\cenario.png" alt="Arquitetura do sistema" width="400"/>
  <br/>
  <strong>Figura 1</strong> – Arquitetura da aplicação
</p>

## Componentes
Os componentes da aplicação são:

 - Frontend - Interface ([Data Control Frontend](https://github.com/gustavopierre/data_control_frontend)) que acessa a Data Control API, exibindo uma lista de dados utilizados nos softwares de GIS, com informações básicas e, principalmente, há quantos dias foi a última checagem e quantos dias faltam para que seja realizada a próxima verificação. Existe um botão para inserir um novo dado no banco de dados e, cada registro na lista, tem botões que permitem:
     - Considerar checado o dado, renovando assim a data da última checagem e a quantidade de dias para a próxima checagem.
     - Excluir um dado do banco de dados.
     - Editar as informações de um dado selecionado, inclusive o retângulo envolvente (bounding box), obtido pela API externa, caso o dado seja do tipo Web Feature Server (WFS) compatível com o formato JSON da ESRI, que é, atualmente, a maioria dos dados WFS utilizados na empresa.
     - Exibir informações do dado selecionado.
     - Visualizar o dado num mapa, caso ele seja do tipo Web Feature Server (WFS) compatível com o formato JSON da ESRI.
 - Backend - Contendo API que implementa rotas de busca de dados no banco de dados, busca de um dado específico, alteração de dados, inserção de dados, deleção de dado, busca de dados por área e atualização da data de checagem do dado. A API é documentada utilizando o [Swagger](https://swagger.io/).
 - Banco de Dados - É utilizado um banco de dados sqlite3, sem suporte a GIS. Apesar da API criar um banco de dados novo na ausência do arquivo de banco de dados, foi deixado um banco de dados populado com alguns poucos registros, para que possam ser testadas as funcionalidades da aplicação.
 - API externa - A interface possibilita o acesso a APIs externas de dados cadastrados do tipo Web Feature Server (WFS) compatível com o formato JSON da ESRI, salvando o retângulo envolvente (bounding box) de um dado novo ou alterando-o, de um dado existente, em virtude de sua atualização.

## Docker
A aplicação pode ser clonada do GitHub e executada criando um ambiente com os devidos requisitos ou utilizando containers [Docker](https://www.docker.com/). Criam-se duas imagens, uma para o frontend e outra para o backend, conforme instruções nos respectivos repositórios, e executam-se essas imagens. Os arquivos README.md têm instruções para criação das imagens, execução delas e execução do frontend ou do backend.

## Detalhamento
Data Control API é o backend da aplicação de controle dos dados usados para serem camadas (layers) nos softwares de geoprocessamento. As principais tecnologias utilizadas são:
 - [Flask](https://flask.palletsprojects.com/en/stable/)
 - [SQLAlchemy](https://www.sqlalchemy.org/)
 - [OpenAPI3](https://swagger.io/specification/)
 - [SQLite](https://www.sqlite.org/index.html)
 - [Docker](https://www.docker.com/)

A API é acessada pelo [Data Control Frontend](https://github.com/gustavopierre/data_control_frontend), disponibilizado no GitHub também. A documentação e uso, sem interface, pode ser realizada através do [Swagger](https://swagger.io/). O repositório contém um banco de dados SQLite com alguns registros populados para que seja feita a verificação da utilização de API externa via Frontend ou via Swagger.

### *Execução*
#### 1) Sem Docker
Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

Para instalar as dependências/bibliotecas, descritas no arquivo `requirements.txt`, utilize o comando:

```
(env)$ pip install -r requirements.txt
```
---

Para executar a API utilize o comando:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro **_reload_**, que reiniciará o servidor
automaticamente após uma mudança no código fonte.

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```
---
Para acessar o Swagger, abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador e selecione `Swagger`.

---
#### 2) Usando Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build -t rest-api .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```
$ docker run -p 5000:5000 rest-api
```

Uma vez executando, para acessar a API, basta abrir o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador.

#### Alguns comandos úteis do Docker

**Para verificar se a imagem foi criada** você pode executar o seguinte comando:

```
$ docker images
```

 Caso queira **remover uma imagem**, basta executar o comando:
```
$ docker rmi <IMAGE ID
```
Subistituindo o `IMAGE ID` pelo código da imagem

**Para verificar se o container está em exceução** você pode executar o seguinte comando:

```
$ docker container ls --all
```

 Caso queira **parar um container**, basta executar o comando:
```
$ docker stop <CONTAINER ID>
```
Subistituindo o `CONTAINER ID` pelo ID do container


 Caso queira **destruir um container**, basta executar o comando:
```
$ docker rm <CONTAINER ID>
```
Para mais comandos, veja a [documentação do docker](https://docs.docker.com/engine/reference/run/).

### TODO List
- Verificar a implementacao das rotas nao utilizadas pela interface.
- criar rota de informacao de dados existentes com base em coordenadas geograficas fornecidas