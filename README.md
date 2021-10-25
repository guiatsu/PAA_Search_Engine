# Search Engine

## Requisitos

Requer Python 3 (desenvolvido no Python 3.8.10)

Instale os requisitos pelo pip:

	pip install -r requirements.txt


## Execução

Primeiro, é necessário executar o WebCrawler:

	python WebCrawler.py

Depois, executar o Flask:
```
export FLASK_ENV=development
export FLASK_APP=main
flask run
```
ou

	python -m flask run

Feito isso, é só acessar a URL que o Flask indicar e fazer suas buscas!

## Online

Também pode ser testado online na seguinte URL:
	https://paa-search-engine.herokuapp.com/

A pesquisa tem como origem o site do [CIC](https://cic.unb.br/)