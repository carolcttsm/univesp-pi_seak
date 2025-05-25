from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Boolean, Column
from werkzeug.security import generate_password_hash, check_password_hash
from website import db, login_manager

# ---------------------------------------------------------------------- MODELO DE USUÁRIO
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_default_admin = Column(Boolean, default=False)

    def set_senha(self, senha):
        self.password_hash = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.password_hash, senha)

    def __repr__(self):
        return f'<User {self.nome_usuario}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------------------------------------------------------------- MODELO DE ALUNO
class Aluno(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    nomemae = db.Column(db.String(150))
    nomepai = db.Column(db.String(150))
    nomeresp = db.Column(db.String(150))
    sexo = db.Column(db.String(1))
    endereco = db.Column(db.String(255))
    cep = db.Column(db.String(20))
    rg = db.Column(db.String(20))
    cpf = db.Column(db.String(20))
    dtnasc = db.Column(db.Date)
    cpfmae = db.Column(db.String(20))
    nisaluno = db.Column(db.String(20))
    nismae = db.Column(db.String(20))
    imagem = db.Column(db.String(255))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    turmas = db.relationship('Turma', secondary='aluno_turma', back_populates='alunos')

    def __repr__(self):
        return f'<Aluno {self.nome}>'


# ---------------------------------------------------------------------- MODELO DE PROFESSOR
class Professor(db.Model):
    __tablename__ = 'professores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    oficinas = db.relationship('Oficina', back_populates='professor')

    def __repr__(self):
        return f'<Professor {self.nome}>'


# ---------------------------------------------------------------------- MODELO DE OFICINA
class Oficina(db.Model):
    __tablename__ = 'oficinas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    vagas = db.Column(db.Integer, nullable=False)

    ano_mes = db.Column(db.String(7), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=False)
    professor = db.relationship('Professor', back_populates='oficinas')

    turmas = db.relationship('Turma', back_populates='oficina')
    presencas = db.relationship('Presenca', back_populates='oficina')

    def __repr__(self):
        return f'<Oficina {self.nome}>'
    
    @property
    def vagas_ocupadas(self):
        return len(self.alunos)



# ---------------------------------------------------------------------- MODELO DE TURMA
class Turma(db.Model):
    __tablename__ = 'turmas'

    id = db.Column(db.Integer, primary_key=True)
    dia_semana = db.Column(db.String(10), nullable=False)  # Ex: "terca"
    hora = db.Column(db.Time, nullable=False)              # Ex: 15:00
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    oficina_id = db.Column(db.Integer, db.ForeignKey('oficinas.id'), nullable=False)
    oficina = db.relationship('Oficina', back_populates='turmas')

    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=False)
    professor = db.relationship('Professor')

    alunos = db.relationship('Aluno', secondary='aluno_turma', back_populates='turmas')

    def __repr__(self):
        return f'<Turma {self.id}>'


# ---------------------------------------------------------------------- MODELO DE PRESENÇA
class Presenca(db.Model):
    __tablename__ = 'presencas'

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    oficina_id = db.Column(db.Integer, db.ForeignKey('oficinas.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)

    aluno = db.relationship('Aluno', backref='presencas')
    oficina = db.relationship('Oficina', back_populates='presencas')

    __table_args__ = (
        db.UniqueConstraint('aluno_id', 'oficina_id', 'data', name='uq_presenca'),
    )

    def __repr__(self):
        return f"<Presenca aluno={self.aluno_id} oficina={self.oficina_id} data={self.data}>"


# ---------------------------------------------------------------------- TABELA ASSOCIATIVA
aluno_turma = db.Table('aluno_turma',
    db.Column('aluno_id', db.Integer, db.ForeignKey('alunos.id'), primary_key=True),
    db.Column('turma_id', db.Integer, db.ForeignKey('turmas.id'), primary_key=True)
)
