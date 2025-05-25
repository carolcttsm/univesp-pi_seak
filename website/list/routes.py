from flask import Blueprint, request, render_template
from website.models import User, Aluno, Professor, Oficina

list_bp = Blueprint('list', __name__)

@list_bp.route('/usuarios')
def listar_usuarios():
    usuarios = User.query.all()
    count = User.query.count()

    return render_template('list/usuarios.html', usuarios=usuarios, count=count)

@list_bp.route('/alunos')
def listar_alunos():
    alunos = Aluno.query.all()
    count = Aluno.query.count()

    return render_template('list/alunos.html', alunos=alunos, count=count)

@list_bp.route('/professores')
def listar_professores():
    professores = Professor.query.all()
    count = Professor.query.count()

    return render_template('list/professores.html', professores=professores, count=count)

@list_bp.route('/oficinas')
def listar_oficinas():
    mes_filtro = request.args.get('ano_mes')
    
    count = Oficina.query.count()
    oficinas = Oficina.query.all()
    oficinas_filtradas = []

    meses_disponiveis = sorted({oficina.ano_mes for oficina in oficinas})

    for oficina in oficinas:
        if mes_filtro and oficina.ano_mes != mes_filtro:
            continue
        
        turmas = oficina.turmas
        oficinas_filtradas.append({
            "nome": oficina.nome,
            "descricao": oficina.descricao,
            "vagas": oficina.vagas,
            "ano_mes": oficina.ano_mes,
            "turmas": turmas
        })

    return render_template("list/oficinas.html",
        oficinas=oficinas_filtradas,
        meses_disponiveis=meses_disponiveis,
        mes_selecionado=mes_filtro,
        count=count
        )
