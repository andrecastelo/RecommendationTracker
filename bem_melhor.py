# -*- coding: utf-8 -*-
#!/usr/bin/env python

# imports
from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
                  abort, render_template, flash, Markup, jsonify

# configuração
DATABASE = 'bem_melhor.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


# aplicação
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent = True)


# funções do banco
def connect_db():
    """Funcao para conectar ao banco de dados da aplicacao"""
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    """Funcao para inicialização do banco de dados"""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as schema:
            db.cursor().executescript(schema.read())
        db.commit()

@app.before_request
def before_request():
    """Funcao que sera chamada antes de qualquer interacao com o banco"""
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    """Funcao que sera chamada depois de qualquer interacao com o banco"""
    g.db.close()


# view principal
@app.route('/')
def main_page():
    """
    Main page function. It will list the available collaborators and its
    clients.
    """
    cur = g.db.execute('select id, nome, area from colaboradores order by id asc')
    entries = [ dict(nome = row[1], id = row[0], area = row[2],
        listaIndicacoes = [], indicacoes = 0,
        indicacoesValidas = 0) for row in cur.fetchall() ]

    cur = g.db.execute('select * from clientes order by indicacao asc')
    clientsList = [ dict(id = row[0], nome = row[1],
        conta = True if row[2] else None,
        indicacao = row[3]) for row in cur.fetchall() ]

    for client in clientsList:
        colaborador = entries[client['indicacao'] - 1]
        colaborador['listaIndicacoes'].append(client)
        colaborador['indicacoes'] += 1
        if client['conta']:
            colaborador['indicacoesValidas'] += 1

    return render_template('main.html', 
        colaboradores = sorted(entries, key = lambda k: k['indicacoes'],
        reverse = True),
        listaClientes = clientsList)


@app.route('/add_client', methods = ['POST'])
def add_client():
    if request.form['cliente']:
        g.db.execute('insert into clientes (nome, indicacao) values (?, ?)',
                [ request.form['cliente'], request.form['colab-indicador'] ])
        g.db.commit()
        return redirect(url_for('main_page'))
    else:
        return redirect(url_for('main_page'))


@app.route('/_remove_client')
def remove_client():
    colab_id = request.args.get('idColaborador', 0, type=int)
    cliente = request.args.get('idCliente', None, type=int)
    g.db.execute('delete from clientes where id=?', [ cliente ])
    g.db.commit()

    if (colab_id):
        listaDeClientes = updated_recommendations(colab_id)
        contasAbertas = map(lambda x: x['conta'], listaDeClientes).count(True)

    return jsonify(total = len(listaDeClientes), abertas = contasAbertas)


@app.route('/_open_acc')
def open_account():
    cliente_id = request.args.get('idCliente', None, type=int)
    colab_id = request.args.get('idColaborador', 0, type=int)
    checked = request.args.get('checked', 0, type=int)
    
    if (cliente_id):
        g.db.execute('update clientes set conta=? where id=?', 
                [ checked, cliente_id ])
        g.db.commit()

    if (colab_id):
        listaDeClientes = updated_recommendations(colab_id)
        contasAbertas = map(lambda x: x['conta'], listaDeClientes).count(True)

    return jsonify(total = len(listaDeClientes), abertas = contasAbertas)


def updated_recommendations(colaboradorId):
    """
    This helper function is used to get the updated recommendations of a
    certain collaborator.
    """
    cur = g.db.execute('select * from clientes where indicacao=?', [ colaboradorId ])
    clientsList = [ dict(id = row[0], nome = row[1],
        conta = True if row[2] else False,
        indicacao = row[3]) for row in cur.fetchall() ]
    return clientsList





#@app.route('/add_client_ajax')
#def add_client_ajax():
#    cliente = request.args.get('cliente')
#    indicador = request.args.get('colab-indicador')    


# execução
if __name__ == '__main__':
    #init_db()
    app.run();