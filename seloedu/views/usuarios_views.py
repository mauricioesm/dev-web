from flask import render_template, request, redirect, url_for, flash
from models.usuario_models import Usuario
from extensions import db


def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template("usuario/index_usuario.html", usuarios=usuarios)


def detalhes_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return render_template("usuario/detalhe_usuario.html", usuario=usuario)

def modificar_usuario(id):

    usuario = Usuario.query.get_or_404(id)

    if not usuario:
        return render_template("usuario/editar_usuario.html")
    
    if request.method == "POST":

        novo_nome = request.form.get("nome").strip()
        nova_funcao = request.form.get("funcao").strip()

        usuario.nome  = novo_nome
        usuario.funcao = nova_funcao
    
        db.session.commit()

        return redirect(url_for("usuario.detalhes", id=usuario.id))
       

    return render_template("usuario/modificar_usuario.html", usuario=usuario)


def deletar_usuario(id):

    usuario = Usuario.query.get_or_404(id)

    if not usuario:
        flash("Usuário não encontrado.", "error")
        return redirect(url_for("usuario.listar"))

    if request.method == "POST":
        
        usuario_id = request.form.get("id").strip()
        
        db.session.delete(usuario)
        db.session.commit()

        return redirect(url_for("usuario.listar"))

    return render_template("usuario/deletar_usuario.html", usuario=usuario)


def criar_usuario():

    if request.method == "POST":
        nome = request.form.get("nome").strip()
        email = request.form.get("email").strip()
        senha = request.form.get("senha")
        funcao = request.form.get("funcao").strip()

        if Usuario.query.filter_by(email=email).first():
            flash("Email já cadastrado. Por favor, use outro email.", "error")

        usuario = Usuario(
            nome = nome,
            email = email,
            senha_hash = senha,
            funcao = funcao,
        )

        try:
            db.session.add(usuario)
            db.session.commit()
            return render_template("usuario/detalhe_usuario.html", usuario=usuario)
        except Exception as e:
            db.session.rollback()
            return render_template("usuario/criar_usuario.html")

    return render_template("usuario/criar_usuario.html")

