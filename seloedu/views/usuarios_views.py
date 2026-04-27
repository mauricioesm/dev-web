from flask import render_template
from models.usuario_models import Usuario


def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template("usuario/index_usuario.html", usuarios=usuarios)


def detalhes_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return render_template("usuario/detalhe_usuario.html", usuario=usuario)
