from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional


class UserCreateForm(FlaskForm):
    name = StringField("Nome completo", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=6)])
    role = SelectField(
        "Perfil",
        choices=[
            ("master", "Master"),
            ("direcao", "Direção"),
            ("coordenacao", "Coordenação"),
            ("administrativo", "Administrativo"),
        ],
    )
    submit = SubmitField("Criar usuário")


class UserEditForm(FlaskForm):
    name = StringField("Nome completo", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[Optional(), Length(min=6)])
    role = SelectField(
        "Perfil",
        choices=[
            ("master", "Master"),
            ("direcao", "Direção"),
            ("coordenacao", "Coordenação"),
            ("administrativo", "Administrativo"),
        ],
    )
    submit = SubmitField("Atualizar usuário")
