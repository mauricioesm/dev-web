from flask import flash, redirect, render_template, request, url_for

from extensions import db
from models.usuario_models import Usuario


def listar_usuarios():
    usuarios = Usuario.query.order_by(Usuario.nome).all()
    return render_template("usuario/index_usuario.html", usuarios=usuarios)


def criar_usuario():
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip().lower()
    funcao = request.form.get("funcao", "coordenador").strip()
    senha = request.form.get("senha", "").strip()

    if not nome or not email or not senha:
        flash("Nome, e-mail e senha são obrigatórios.", "danger")
        return redirect(url_for("usuario.listar"))

    usuario = Usuario(nome=nome, email=email, funcao=funcao)
    usuario.set_password(senha)
    db.session.add(usuario)
    db.session.commit()
    flash("Usuário criado com sucesso.", "success")
    return redirect(url_for("usuario.listar"))


def detalhes_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return render_template("usuario/detalhe_usuario.html", usuario=usuario)


def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == "POST":
        usuario.nome = request.form.get("nome", usuario.nome).strip()
        usuario.email = request.form.get("email", usuario.email).strip().lower()
        usuario.funcao = request.form.get("funcao", usuario.funcao).strip()
        senha = request.form.get("senha", "").strip()
        if senha:
            usuario.set_password(senha)
        db.session.commit()
        flash("Usuário atualizado com sucesso.", "success")
        return redirect(url_for("usuario.detalhes", id=usuario.id))

    return render_template("usuario/editar_usuario.html", usuario=usuario)


def excluir_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash("Usuário excluído com sucesso.", "success")
    return redirect(url_for("usuario.listar"))
