from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
import os
from datetime import date
from collections import defaultdict

from website.models import User, Aluno, Presenca, Professor, Oficina, Turma
from website.forms import UserForm, ProfessorForm, AlunoForm, OficinaForm, PresencaForm, TurmaForm
from website import db

admin = Blueprint('admin', __name__)

# ---------------------------------------------------------------------- PAINEL ADMINISTRATIVO
@admin.route('/', methods=['GET', 'POST'])
@login_required
def painel():
    return render_template('admin-panel.html',
        current_user=current_user,
        data_hoje=date.today().strftime('%d/%m/%Y'),
        total_alunos=Aluno.query.count(),
        total_oficinas=Oficina.query.count(),
        total_turmas=Turma.query.count(),
        total_professores=Professor.query.count()
    )

# ---------------------------------------------------------------------- USUÁRIOS (ADMINS)
@admin.route('/admins/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_admin():
    form = UserForm()
    if form.validate_on_submit():
        novo_usuario = User(
            nome_usuario=form.nome_usuario.data,
            email=form.email.data
        )
        novo_usuario.set_senha(form.senha1.data)
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('admin.listar_usuarios'))

    return render_template('add/usuario.html', form=form)

@admin.route('/admins/<int:usuario_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_usuario(usuario_id):
    usuario = User.query.get_or_404(usuario_id)
    form = UserForm(obj=usuario)
    if form.validate_on_submit():
        usuario.nome_usuario = form.nome_usuario.data
        usuario.email = form.email.data
        if form.senha1.data:
            usuario.set_senha(form.senha1.data)
        db.session.commit()
        flash('Usuário atualizado com sucesso.', 'success')
        return redirect(url_for('admin.listar_usuarios'))

    return render_template('edit/usuario.html', form=form)

@admin.route('/admins/list')
@login_required
def listar_usuarios():
    usuarios = User.query.all()
    return render_template('list/usuarios.html', usuarios=usuarios, count=len(usuarios))

@admin.route('/admins/<int:usuario_id>/deletar', methods=['POST'])
@login_required
def deletar_usuario(usuario_id):
    usuario = User.query.get_or_404(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário removido com sucesso.', 'info')
    return redirect(url_for('admin.listar_usuarios'))

# ---------------------------------------------------------------------- ALUNOS
@admin.route('/alunos/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_aluno():
    form = AlunoForm()

    if form.validate_on_submit():
        dtnasc_date = form.dtnasc.data

        imagem_file = request.files.get('imagem')
        imagem_filename = None
        if imagem_file and imagem_file.filename != '':
            filename = secure_filename(imagem_file.filename)
            caminho = os.path.join('website/static/uploads', filename)
            imagem_file.save(caminho)
            imagem_filename = filename

        novo_aluno = Aluno(
            nome=form.nome.data,
            nomemae=form.nomemae.data,
            nomepai=form.nomepai.data,
            nomeresp=form.nomeresp.data,
            sexo=form.sexo.data,
            endereco=form.endereco.data,
            cep=form.cep.data,
            rg=form.rg.data,
            cpf=form.cpf.data,
            dtnasc=dtnasc_date,
            cpfmae=form.cpfmae.data,
            nisaluno=form.nisaluno.data,
            nismae=form.nismae.data,
            imagem=imagem_filename
        )

        db.session.add(novo_aluno)
        db.session.commit()
        flash('Aluno cadastrado com sucesso!', category='success')
        return redirect(url_for('list.listar_alunos'))

    return render_template('add/aluno.html', form=form)

@admin.route('/alunos/<int:aluno_id>', methods=['GET', 'POST'])
@login_required
def ver_aluno(aluno_id):
    aluno = Aluno.query.get_or_404(aluno_id)
    turmas = aluno.turmas
    oficinas = {t.oficina for t in turmas}

    form = PresencaForm()
    form.oficina.choices = [(o.id, o.nome) for o in oficinas]

    if request.method == 'POST':
        # Registro de presença
        if 'oficina' in request.form:
            if form.validate_on_submit() and form.presente.data:
                nova = Presenca(
                    aluno_id=aluno.id,
                    oficina_id=form.oficina.data,
                    data=form.data.data
                )
                try:
                    db.session.add(nova)
                    db.session.commit()
                    flash('Presença registrada!', 'success')
                except IntegrityError:
                    db.session.rollback()
                    flash('Presença já registrada para esse dia.', 'warning')
            return redirect(url_for('admin.ver_aluno', aluno_id=aluno.id))

        # Adição do aluno a turmas
        turma_ids = request.form.getlist("turmas")
        for turma_id in turma_ids:
            turma = Turma.query.get(int(turma_id))
            if turma and aluno not in turma.alunos and len(turma.alunos) < turma.oficina.vagas:
                turma.alunos.append(aluno)
        db.session.commit()
        flash("Aluno adicionado às turmas selecionadas.", "success")
        return redirect(url_for("admin.ver_aluno", aluno_id=aluno.id))

    # Presenças agrupadas por oficina
    presencas_raw = Presenca.query.filter_by(aluno_id=aluno.id).join(Oficina).order_by(Presenca.data).all()
    presencas_por_oficina = defaultdict(list)
    for p in presencas_raw:
        presencas_por_oficina[p.oficina.nome].append(p.data)

    turmas_disponiveis = Turma.query.filter(~Turma.alunos.any(id=aluno.id)).all()

    return render_template(
        'view/aluno.html',
        aluno=aluno,
        turmas=turmas,
        turmas_disponiveis=turmas_disponiveis,
        presencas_por_oficina=presencas_por_oficina,
        form=form
    )

@admin.route('/alunos/<int:aluno_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_aluno(aluno_id):
    aluno = Aluno.query.get_or_404(aluno_id)
    form = AlunoForm(obj=aluno)

    if form.validate_on_submit():
        form.populate_obj(aluno)
        db.session.commit()
        flash('Aluno atualizado com sucesso.', 'success')
        return redirect(url_for('admin.ver_aluno', aluno_id=aluno.id))

    return render_template('edit/aluno.html', form=form, aluno=aluno)

@admin.route('/alunos/<int:aluno_id>/deletar', methods=['POST'])
@login_required
def deletar_aluno(aluno_id):
    aluno = Aluno.query.get_or_404(aluno_id)
    db.session.delete(aluno)
    db.session.commit()
    flash('Aluno excluído com sucesso.', 'success')
    return redirect(url_for('list.alunos'))

# ---------------------------------------------------------------------- PROFESSORES
@admin.route('/professores/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_professor():
    form = ProfessorForm()
    if form.validate_on_submit():
        professor = Professor(nome=form.nome.data)
        db.session.add(professor)
        db.session.commit()
        flash('Professor cadastrado com sucesso!', 'success')
        return redirect(url_for('list.listar_professores'))

    return render_template('add/professor.html', form=form)

@admin.route('/professores/<int:professor_id>/deletar', methods=['POST'])
@login_required
def deletar_professor(professor_id):
    professor = Professor.query.get_or_404(professor_id)
    db.session.delete(professor)
    db.session.commit()
    flash('Professor deletado com sucesso!', 'success')
    return redirect(url_for('list.listar_professores'))

# ---------------------------------------------------------------------- OFICINAS
@admin.route('/oficinas/criar', methods=['GET', 'POST'])
@login_required
def criar_oficina():
    form = OficinaForm()
    form.professor_id.choices = [(p.id, p.nome) for p in Professor.query.order_by(Professor.nome).all()]

    if form.validate_on_submit():
        oficina = Oficina(
            nome=form.nome.data,
            descricao=form.descricao.data,
            vagas=form.vagas.data,
            ano_mes=form.mes_referencia.data,
            professor_id=form.professor_id.data
        )
        db.session.add(oficina)
        db.session.commit()
        flash('Oficina criada com sucesso!', 'success')
        return redirect(url_for('list.listar_oficinas'))

    return render_template('add/oficina.html', form=form)

@admin.route('/oficinas/<int:oficina_id>')
@login_required
def ver_oficina(oficina_id):
    oficina = Oficina.query.get_or_404(oficina_id)
    turmas = oficina.turmas  # se houver relacionamento definido

    return render_template('view/oficina.html', oficina=oficina, turmas=turmas)

@admin.route('/oficinas/<int:id>/deletar', methods=['POST'])
@login_required
def deletar_oficina(id):
    oficina = Oficina.query.get_or_404(id)
    db.session.delete(oficina)
    db.session.commit()
    flash(f'Oficina "{oficina.nome}" deletada com sucesso.', 'success')
    return redirect(url_for('search.listar_oficinas'))

# ---------------------------------------------------------------------- TURMAS
@admin.route("/turmas/criar", methods=["GET", "POST"])
@login_required
def criar_turma():
    form = TurmaForm()
    if form.validate_on_submit():
        nova_turma = Turma(
            oficina=form.oficina_id.data,
            professor=form.professor_id.data,
            hora=form.hora.data,
            dia_semana=form.dia_semana.data,
            alunos=form.alunos.data,
        )
        db.session.add(nova_turma)
        db.session.commit()
        flash("Turma criada com sucesso.", "success")
        return redirect(url_for("admin.ver_turma", turma_id=nova_turma.id))

    return render_template("add/turma.html", form=form)

@admin.route('/turmas/<int:turma_id>', methods=['GET', 'POST'])
@login_required
def ver_turma(turma_id):
    turma = Turma.query.get_or_404(turma_id)
    oficina = turma.oficina

    if request.method == 'POST':
        # Adição de alunos
        if 'adicionar' in request.form:
            alunos_ids = request.form.getlist('alunos_disponiveis')
            for aluno_id in alunos_ids:
                aluno = Aluno.query.get(int(aluno_id))
                if aluno and aluno not in turma.alunos:
                    turma.alunos.append(aluno)

        # Remoção de alunos
        elif 'remover' in request.form:
            alunos_ids = request.form.getlist('alunos_matriculados')
            for aluno_id in alunos_ids:
                aluno = Aluno.query.get(int(aluno_id))
                if aluno and aluno in turma.alunos:
                    turma.alunos.remove(aluno)

        # Atualiza vagas ocupadas
        oficina.vagas_ocupadas = len(set(a for t in oficina.turmas for a in t.alunos))
        db.session.commit()
        flash('Atualização realizada com sucesso.', 'success')
        return redirect(url_for('admin.ver_turma', turma_id=turma_id))

    alunos_matriculados = turma.alunos
    todos_alunos = Aluno.query.all()
    alunos_disponiveis = [a for a in todos_alunos if a not in alunos_matriculados]

    return render_template(
        'view/turma.html',
        turma=turma,
        alunos_matriculados=alunos_matriculados,
        alunos_disponiveis=alunos_disponiveis
    )

@admin.route("/turmas/<int:turma_id>/editar", methods=["GET", "POST"])
@login_required
def editar_turma(turma_id):
    turma = Turma.query.get_or_404(turma_id)
    form = TurmaForm(obj=turma)
    form.alunos.data = turma.alunos

    if form.validate_on_submit():
        form.populate_obj(turma)
        turma.alunos = form.alunos.data
        db.session.commit()
        flash("Turma atualizada com sucesso.", "success")
        return redirect(url_for("admin.ver_turma", turma_id=turma.id))

    return render_template("edit/turma.html", form=form, turma=turma)

@admin.route('/turmas/<int:turma_id>/deletar', methods=['POST'])
@login_required
def deletar_turma(turma_id):
    turma = Turma.query.get_or_404(turma_id)
    db.session.delete(turma)
    db.session.commit()
    flash('Turma excluída com sucesso.', 'success')
    return redirect(url_for('list.turmas'))
