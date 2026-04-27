from flask import render_template, redirect, url_for, flash, request
from models.usuario_models import Usuario
from forms.user_forms import UserCreateForm, UserEditForm
from extensions import db


def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template("usuario/index_usuario.html", usuarios=usuarios)


def detalhes_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return render_template("usuario/detalhe_usuario.html", usuario=usuario)


def criar_usuario():
    form = UserCreateForm()
    if form.validate_on_submit():
        # Verificar se o email já existe
        usuario_existente = Usuario.query.filter_by(email=form.email.data).first()
        if usuario_existente:
            flash("Este email já está cadastrado.", "danger")
            return redirect(url_for("usuario.criar"))
        
        # Criar novo usuário
        usuario = Usuario(
            nome=form.name.data,
            email=form.email.data,
            funcao=form.role.data
        )
        usuario.set_password(form.password.data)
        
        db.session.add(usuario)
        db.session.commit()
        
        flash(f"Usuário {usuario.nome} criado com sucesso!", "success")
        return redirect(url_for("usuario.listar"))
    
    return render_template("usuario/criar_usuario.html", form=form)


def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    form = UserEditForm()
    
    if form.validate_on_submit():
        # Verificar se o novo email já existe (excluindo o usuário atual)
        usuario_existente = Usuario.query.filter_by(email=form.email.data).first()
        if usuario_existente and usuario_existente.id != usuario.id:
            flash("Este email já está cadastrado.", "danger")
            return redirect(url_for("usuario.editar", id=usuario.id))
        
        # Atualizar dados do usuário
        usuario.nome = form.name.data
        usuario.email = form.email.data
        usuario.funcao = form.role.data
        
        # Atualizar senha se fornecida
        if form.password.data:
            usuario.set_password(form.password.data)
        
        db.session.commit()
        
        flash(f"Usuário {usuario.nome} atualizado com sucesso!", "success")
        return redirect(url_for("usuario.detalhes", id=usuario.id))
    
    elif request.method == "GET":
        form.name.data = usuario.nome
        form.email.data = usuario.email
        form.role.data = usuario.funcao
    
    return render_template("usuario/editar_usuario.html", form=form, usuario=usuario)


def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    
    db.session.delete(usuario)
    db.session.commit()
    
    flash(f"Usuário {usuario.nome} deletado com sucesso!", "success")
    return redirect(url_for("usuario.listar"))
