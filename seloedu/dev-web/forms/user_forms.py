from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email


class UserForm(FlaskForm):
    name = StringField("Nome completo", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    role = SelectField(
        "Perfil",
        choices=[
            ("Master", "Master"),
            ("Direcao", "Direcao"),
            ("Coordenacao", "Coordenacao"),
            ("Administrativo", "Administrativo"),
        ],
    )
    status = SelectField(
        "Status",
        choices=[("Ativo", "Ativo"), ("Inativo", "Inativo")],
    )
    submit = SubmitField("Salvar usuário")