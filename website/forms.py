from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (
    Field,
    StringField,
    IntegerField,
    DateField,
    PasswordField,
    SelectField,
    SubmitField,
    FileField,
    BooleanField,
    TimeField,
    TextAreaField,
)
from wtforms.validators import (
    ValidationError,
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
)
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.widgets import DateTimeInput
from website.models import Professor, Oficina, Aluno

DIA_SEMANA_CHOICES = [
    ('segunda', 'Segunda-feira'),
    ('terca', 'Terça-feira'),
    ('quarta', 'Quarta-feira'),
    ('quinta', 'Quinta-feira'),
    ('sexta', 'Sexta-feira'),
    ('sabado', 'Sábado'),
    ('domingo', 'Domingo'),
]

# ---------------------------------------------------------------------- CAMPOS PERSONALIZADOS
class DateTimeLocalField(Field):
    """
    Campo WTForms para inputs <input type="datetime-local">.

    Converte a string HTML5 no formato “YYYY-MM-DDTHH:MM” em
    `datetime.datetime` e vice-versa.
    """

    def __init__(
        self,
        label: str | None = None,
        validators: list | None = None,
        format: str = "%Y-%m-%dT%H:%M",
        **kwargs,
    ):
        super().__init__(label, validators, **kwargs)
        self.format = format
        self.data: datetime | None = None

    # valor que vai para o template
    def _value(self) -> str:
        return self.data.strftime(self.format) if self.data else ""

    # conversão do valor vindo do form para Python
    def process_formdata(self, valuelist):  # noqa: D401
        if not valuelist:
            self.data = None
            return

        date_str = valuelist[0]
        if not date_str:
            self.data = None
            return

        try:
            self.data = datetime.strptime(date_str, self.format)
        except ValueError as exc:
            self.data = None
            raise ValidationError(
                f"Data e hora inválidas (formato esperado: {self.format})"
            ) from exc


# ---------------------------------------------------------------------- FORMULÁRIOS
class UserForm(FlaskForm):
    nome_usuario = StringField(
        "Nome completo", validators=[DataRequired(), Length(max=120)]
    )
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha1 = PasswordField("Senha", validators=[DataRequired(), Length(min=6)])
    senha2 = PasswordField(
        "Confirme a senha",
        validators=[
            DataRequired(),
            EqualTo("senha1", message="As senhas devem coincidir"),
        ],
    )
    submit = SubmitField("Salvar")


class AlunoForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(max=255)])
    nomemae = StringField("Nome da Mãe", validators=[Optional(), Length(max=255)])
    nomepai = StringField("Nome do Pai", validators=[Optional(), Length(max=255)])
    nomeresp = StringField(
        "Responsável Legal", validators=[Optional(), Length(max=255)]
    )
    sexo = SelectField(
        "Sexo",
        choices=[("M", "Masculino"), ("F", "Feminino")],
        validators=[Optional()],
    )
    endereco = StringField("Endereço", validators=[Optional(), Length(max=500)])
    cep = StringField("CEP", validators=[Optional(), Length(max=20)])
    rg = StringField("RG", validators=[Optional(), Length(max=20)])
    cpf = StringField("CPF", validators=[Optional(), Length(max=20)])
    dtnasc = DateField("Data de Nascimento", validators=[Optional()])
    cpfmae = StringField("CPF da Mãe", validators=[Optional(), Length(max=20)])
    nisaluno = StringField("NIS do Aluno", validators=[Optional(), Length(max=20)])
    nismae = StringField("NIS da Mãe", validators=[Optional(), Length(max=20)])
    imagem = FileField("Foto")
    submit = SubmitField("Salvar")


class ProfessorForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(max=120)])
    submit = SubmitField("Salvar")


class OficinaForm(FlaskForm):
    nome = StringField("Nome da Oficina", validators=[DataRequired(), Length(max=120)])
    descricao = TextAreaField(
        "Descrição das atividades oferecidas nessa oficina", validators=[DataRequired()]
    )
    vagas = IntegerField("Número de Vagas", validators=[DataRequired()])
    mes_referencia = StringField(
        "Mês de Referência (ex: 2025-05)", validators=[DataRequired(), Length(min=7, max=7)]
    )
    professor_id = SelectField(
        "Professor Responsável", coerce=int, validators=[DataRequired()]
    )
    submit = SubmitField("Salvar")


class TurmaForm(FlaskForm):
    oficina_id = QuerySelectField("Oficina", query_factory=lambda: Oficina.query.all(), get_label="nome", validators=[DataRequired()])
    professor_id = QuerySelectField("Professor", query_factory=lambda: Professor.query.all(), get_label="nome", validators=[DataRequired()])
    dia_semana = SelectField('Dia da Semana', choices=DIA_SEMANA_CHOICES, validators=[DataRequired()])
    hora = TimeField('Horário', validators=[DataRequired()])
    alunos = QuerySelectMultipleField(
        'Alunos',
        query_factory=lambda: Aluno.query.order_by(Aluno.nome).all(),
        get_label=lambda aluno: f"{aluno.id} - {aluno.nome}",
        allow_blank=True,
    )
    submit = SubmitField("Salvar")


class PresencaForm(FlaskForm):
    oficina = SelectField("Oficina", coerce=int, validators=[DataRequired()])
    data = DateField("Data", validators=[DataRequired()])
    presente = BooleanField("Presente")
    submit = SubmitField("Registrar presença")
