from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional


class UserForm(FlaskForm):
    nome = StringField("Nome completo", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[Optional(), Length(min=6, message="A senha deve ter no mínimo 6 caracteres")])
    funcao = SelectField(
        "Perfil",
        choices=[
            ("Master", "Master"),
            ("Direcao", "Direção"),
            ("Coordenacao", "Coordenação"),
            ("Administrativo", "Administrativo"),
        ],
    )
    status = SelectField(
        "Status",
        choices=[("Ativo", "Ativo"), ("Inativo", "Inativo")],
    )
    submit = SubmitField("Salvar usuário")
