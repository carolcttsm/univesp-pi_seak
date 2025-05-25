from flask import Blueprint, request, render_template
from sqlalchemy.orm import joinedload
from sqlalchemy import cast, String
from website.models import Aluno, Oficina, Turma
from website import db

search = Blueprint('search', __name__)

@search.route('/alunos', methods=['GET'])
def buscar_aluno():
    identificador = request.args.get('identificador')
    nome = request.args.get('nome')

    query = Aluno.query

    if identificador:
        query = query.filter(Aluno.id == identificador)
    if nome:
        query = query.filter(Aluno.nome.ilike(f"%{nome}%"))

    resultados = query.all() if identificador or nome else None
    count = Aluno.query.count()

    return render_template(
        'search/aluno.html',
        resultados=resultados,
        count=count,
        busca_feita=bool(identificador or nome)  # envia flag para controle no template
    )

@search.route('/turma', methods=['GET'])
def buscar_turma():
    identificador = request.args.get('identificador', '').strip()
    dia_semana = request.args.get('dia_semana', '').strip().lower()
    hora = request.args.get('hora', '').strip()

    query = Turma.query

    if identificador:
        try:
            query = query.filter(Turma.id == int(identificador))
        except ValueError:
            query = query.filter(Turma.id == -1)

    if dia_semana:
        query = query.filter(Turma.dia_semana.ilike(f"%{dia_semana}%"))
    if hora:
        query = query.filter(cast(Turma.hora, String).ilike(f"%{hora}%"))

    resultados = query.all() if (identificador or dia_semana or hora) else None
    count = Turma.query.count()

    return render_template(
        'search/turma.html',
        resultados=resultados,
        count=count,
        busca_feita=bool(identificador or dia_semana or hora)
    )

@search.route('/oficina', methods=['GET'])
def buscar_oficina():
    nome = request.args.get('nome', '').strip()
    resultados = []

    if nome:
        resultados = Oficina.query.filter(Oficina.nome.ilike(f"%{nome}%")).all()

    count = Oficina.query.count()
    return render_template(
        'search/oficina.html',
        resultados=resultados,
        nome_busca=nome,
        count=count,
        busca_feita=bool(nome)
    )

