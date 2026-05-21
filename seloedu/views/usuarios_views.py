from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import or_

from extensions import db
from models.usuario_models import Usuario
from utils.form_validators import clean_email, clean_text, require_fields
from utils.pagination import paginate_query


FUNCAO_CHOICES = ("master", "coordenador", "coordenacao", "administrativo")


def _form_data(usuario=None):
    if request.method == "POST":
        return request.form

    return {
        "nome": usuario.nome if usuario else "",
        "email": usuario.email if usuario else "",
        "funcao": usuario.funcao if usuario else "coordenador",
    }


def _validate_usuario(usuario=None):
    errors = []
    require_fields(
        request.form,
        [("nome", "Nome"), ("email", "E-mail"), ("funcao", "Perfil")],
        errors,
    )

    email = clean_email(request.form.get("email"))
    if email and "@" not in email:
        errors.append("Informe um e-mail valido.")

    funcao = clean_text(request.form.get("funcao")) or "coordenador"
    if funcao not in FUNCAO_CHOICES:
        errors.append("Perfil invalido.")

    senha = request.form.get("senha", "")
    if not usuario and not senha:
        errors.append("Senha e obrigatoria para novo usuario.")
    if senha and len(senha) < 6:
        errors.append("Senha deve ter pelo menos 6 caracteres.")

    query = Usuario.query.filter_by(email=email)
    if usuario:
        query = query.filter(Usuario.id != usuario.id)
    if email and query.first():
        errors.append("Ja existe um usuario com este e-mail.")

    return errors, {
        "nome": clean_text(request.form.get("nome")),
        "email": email,
        "funcao": funcao,
        "senha": senha,
    }


def listar_usuarios():
    busca = clean_text(request.args.get("q"))
    page = request.args.get("page", 1, type=int)

    query = Usuario.query
    if busca:
        like = f"%{busca}%"
        query = query.filter(
            or_(
                Usuario.nome.ilike(like),
                Usuario.email.ilike(like),
                Usuario.funcao.ilike(like),
            )
        )

    pagination = paginate_query(query.order_by(Usuario.nome.asc()), page)
    return render_template(
        "usuario/index_usuario.html",
        usuarios=pagination.items,
        pagination=pagination,
        busca=busca,
    )


def criar_usuario():
    if request.method == "POST":
        errors, data = _validate_usuario()
        if not errors:
            usuario = Usuario(
                nome=data["nome"],
                email=data["email"],
                funcao=data["funcao"],
            )
            usuario.set_password(data["senha"])
            db.session.add(usuario)
            db.session.commit()
            flash("Usuario cadastrado com sucesso.", "success")
            return redirect(url_for("usuario.detalhes", id=usuario.id))

        for error in errors:
            flash(error, "danger")

    return render_template(
        "usuario/form_usuario.html",
        title="Novo usuario",
        form_data=_form_data(),
        funcao_choices=FUNCAO_CHOICES,
        action_url=url_for("usuario.criar"),
    )


def detalhes_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return render_template("usuario/detalhe_usuario.html", usuario=usuario)


def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == "POST":
        errors, data = _validate_usuario(usuario)
        if not errors:
            usuario.nome = data["nome"]
            usuario.email = data["email"]
            usuario.funcao = data["funcao"]
            if data["senha"]:
                usuario.set_password(data["senha"])
            db.session.commit()
            flash("Usuario atualizado com sucesso.", "success")
            return redirect(url_for("usuario.detalhes", id=usuario.id))

        for error in errors:
            flash(error, "danger")

    return render_template(
        "usuario/form_usuario.html",
        title="Editar usuario",
        usuario=usuario,
        form_data=_form_data(usuario),
        funcao_choices=FUNCAO_CHOICES,
        action_url=url_for("usuario.editar", id=usuario.id),
    )


def excluir_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if usuario.id == current_user.id:
        flash("Voce nao pode excluir o proprio usuario logado.", "danger")
        return redirect(url_for("usuario.listar"))

    db.session.delete(usuario)
    db.session.commit()
    flash("Usuario excluido com sucesso.", "success")
    return redirect(url_for("usuario.listar"))
