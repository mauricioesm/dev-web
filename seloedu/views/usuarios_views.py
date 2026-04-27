from flask import render_template, redirect, url_for, flash, request
from models.usuario_models import Usuario
from forms.user_forms import UserForm
from extensions import db


def listar_usuarios():
    """Lista todos os usuários do sistema"""
    usuarios = Usuario.query.all()
    return render_template("usuario/index_usuario.html", usuarios=usuarios)


def detalhes_usuario(id):
    """Mostra os detalhes de um usuário específico"""
    usuario = Usuario.query.get_or_404(id)
    return render_template("usuario/detalhe_usuario.html", usuario=usuario)


def criar_usuario():
    """Cria um novo usuário"""
    form = UserForm()
    if form.validate_on_submit():
        # Verificar se email já existe
        if Usuario.query.filter_by(email=form.email.data).first():
            flash("Email já cadastrado no sistema.", "error")
            return redirect(url_for("usuario.criar"))
        
        # Criar novo usuário
        novo_usuario = Usuario(
            nome=form.nome.data,
            email=form.email.data,
            funcao=form.funcao.data,
            status=form.status.data
        )
        novo_usuario.set_password(form.senha.data)
        
        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash(f"Usuário '{novo_usuario.nome}' criado com sucesso!", "success")
            return redirect(url_for("usuario.detalhes", id=novo_usuario.id))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao criar usuário: {str(e)}", "error")
            return redirect(url_for("usuario.criar"))
    
    return render_template("usuario/form_usuario.html", form=form, titulo="Criar Usuário")


def editar_usuario(id):
    """Edita um usuário existente"""
    usuario = Usuario.query.get_or_404(id)
    form = UserForm()
    
    if form.validate_on_submit():
        # Verificar se o novo email já existe (excluindo o email atual)
        if form.email.data != usuario.email and Usuario.query.filter_by(email=form.email.data).first():
            flash("Email já cadastrado no sistema.", "error")
            return redirect(url_for("usuario.editar", id=usuario.id))
        
        # Atualizar dados
        usuario.nome = form.nome.data
        usuario.email = form.email.data
        usuario.funcao = form.funcao.data
        usuario.status = form.status.data
        
        # Atualizar senha se foi fornecida
        if form.senha.data:
            usuario.set_password(form.senha.data)
        
        try:
            db.session.commit()
            flash(f"Usuário '{usuario.nome}' atualizado com sucesso!", "success")
            return redirect(url_for("usuario.detalhes", id=usuario.id))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar usuário: {str(e)}", "error")
            return redirect(url_for("usuario.editar", id=usuario.id))
    
    elif request.method == "GET":
        # Pré-preencher o formulário com os dados atuais
        form.nome.data = usuario.nome
        form.email.data = usuario.email
        form.funcao.data = usuario.funcao
        form.status.data = usuario.status
    
    return render_template("usuario/form_usuario.html", form=form, titulo="Editar Usuário", usuario=usuario)


def deletar_usuario(id):
    """Deleta um usuário"""
    usuario = Usuario.query.get_or_404(id)
    
    try:
        nome_usuario = usuario.nome
        db.session.delete(usuario)
        db.session.commit()
        flash(f"Usuário '{nome_usuario}' deletado com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao deletar usuário: {str(e)}", "error")
    
    return redirect(url_for("usuario.listar"))
