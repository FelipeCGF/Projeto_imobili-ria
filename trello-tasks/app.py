from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
ARQUIVO_TAREFAS = 'tasks.json'

def carregar_tarefas():
    if not os.path.exists(ARQUIVO_TAREFAS):
        return []
    with open(ARQUIVO_TAREFAS, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)

def salvar_tarefas(tarefas):
    with open(ARQUIVO_TAREFAS, 'w', encoding='utf-8') as arquivo:
        json.dump(tarefas, arquivo, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    tarefas = carregar_tarefas()
    return render_template('index.html', tarefas=tarefas)

@app.route('/adicionar', methods=['POST'])
def adicionar_tarefa():
    tarefas = carregar_tarefas()
    nova_tarefa = {
        'id': len(tarefas) + 1,
        'titulo': request.form['titulo'],
        'concluida': False
    }
    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas)
    return redirect(url_for('index'))

@app.route('/concluir/<int:tarefa_id>')
def concluir_tarefa(tarefa_id):
    tarefas = carregar_tarefas()
    for tarefa in tarefas:
        if tarefa['id'] == tarefa_id:
            tarefa['concluida'] = True
            break
    salvar_tarefas(tarefas)
    return redirect(url_for('index'))

@app.route('/excluir/<int:tarefa_id>')
def excluir_tarefa(tarefa_id):
    tarefas = carregar_tarefas()
    tarefas = [t for t in tarefas if t['id'] != tarefa_id]
    salvar_tarefas(tarefas)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
