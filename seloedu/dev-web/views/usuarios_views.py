from flask import redirect, render_template, request, url_for
from extensions import db
from models.usuario_models import Usuario


def listar_usuarios():
    usuarios = Usuario.query.order_by(Usuario.nome).all()
    return render_template("usuario/index_usuario.html", usuarios=usuarios)


def detalhes_usuario(id):
    usuario = db.get_or_404(Usuario, id)
    return render_template("usuario/detalhe_usuario.html", usuario=usuario)


def novo_usuario():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        funcao = request.form.get("funcao", "coordenador")
        usuario = Usuario(nome=nome, email=email, funcao=funcao)
        usuario.set_password(senha)
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for("usuario.listar"))
    return render_template("usuario/form_usuario.html", usuario=None)


def editar_usuario(id):
    usuario = db.get_or_404(Usuario, id)
    if request.method == "POST":
        usuario.nome = request.form.get("nome", "").strip()
        usuario.email = request.form.get("email", "").strip().lower()
        usuario.funcao = request.form.get("funcao", "coordenador")
        nova_senha = request.form.get("senha", "").strip()
        if nova_senha:
            usuario.set_password(nova_senha)
        db.session.commit()
        return redirect(url_for("usuario.listar"))
    return render_template("usuario/form_usuario.html", usuario=usuario)


def excluir_usuario(id):
    usuario = db.get_or_404(Usuario, id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for("usuario.listar"))
