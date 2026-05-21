from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import or_

from extensions import db
from models.funcionario_model import Funcionario
from utils.form_validators import clean_email, clean_text, parse_date, require_fields
from utils.pagination import paginate_query


STATUS_CHOICES = ("ativo", "inativo", "afastado")


def _form_data(funcionario=None):
    if request.method == "POST":
        return request.form

    return {
        "nome": funcionario.nome if funcionario else "",
        "email": funcionario.email if funcionario else "",
        "cargo": funcionario.cargo if funcionario else "",
        "telefone": funcionario.telefone if funcionario else "",
        "status": funcionario.status if funcionario else "ativo",
        "data_admissao": (
            funcionario.data_admissao.isoformat()
            if funcionario and funcionario.data_admissao
            else ""
        ),
    }


def _validate_funcionario(funcionario=None):
    errors = []
    require_fields(
        request.form,
        [("nome", "Nome"), ("email", "E-mail"), ("cargo", "Cargo")],
        errors,
    )

    email = clean_email(request.form.get("email"))
    if email and "@" not in email:
        errors.append("Informe um e-mail valido.")

    status = clean_text(request.form.get("status")) or "ativo"
    if status not in STATUS_CHOICES:
        errors.append("Status invalido.")

    query = Funcionario.query.filter_by(email=email)
    if funcionario:
        query = query.filter(Funcionario.id != funcionario.id)
    if email and query.first():
        errors.append("Ja existe um funcionario com este e-mail.")

    data_admissao = parse_date(
        request.form.get("data_admissao"),
        "Data de admissao",
        errors,
    )

    return errors, {
        "nome": clean_text(request.form.get("nome")),
        "email": email,
        "cargo": clean_text(request.form.get("cargo")),
        "telefone": clean_text(request.form.get("telefone")),
        "status": status,
        "data_admissao": data_admissao,
    }


def listar_funcionarios():
    busca = clean_text(request.args.get("q"))
    status = clean_text(request.args.get("status"))
    page = request.args.get("page", 1, type=int)

    query = Funcionario.query
    if busca:
        like = f"%{busca}%"
        query = query.filter(
            or_(
                Funcionario.nome.ilike(like),
                Funcionario.email.ilike(like),
                Funcionario.cargo.ilike(like),
            )
        )
    if status:
        query = query.filter_by(status=status)

    pagination = paginate_query(query.order_by(Funcionario.nome.asc()), page)
    return render_template(
        "funcionarios/index.html",
        funcionarios=pagination.items,
        pagination=pagination,
        busca=busca,
        status=status,
        status_choices=STATUS_CHOICES,
    )


def criar_funcionario():
    if request.method == "POST":
        errors, data = _validate_funcionario()
        if not errors:
            funcionario = Funcionario(**data)
            db.session.add(funcionario)
            db.session.commit()
            flash("Funcionario cadastrado com sucesso.", "success")
            return redirect(url_for("funcionarios.detalhes", id=funcionario.id))

        for error in errors:
            flash(error, "danger")

    return render_template(
        "funcionarios/form.html",
        title="Novo funcionario",
        form_data=_form_data(),
        status_choices=STATUS_CHOICES,
        action_url=url_for("funcionarios.criar"),
    )


def detalhes_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    return render_template("funcionarios/detalhes.html", funcionario=funcionario)


def editar_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    if request.method == "POST":
        errors, data = _validate_funcionario(funcionario)
        if not errors:
            for field, value in data.items():
                setattr(funcionario, field, value)
            db.session.commit()
            flash("Funcionario atualizado com sucesso.", "success")
            return redirect(url_for("funcionarios.detalhes", id=funcionario.id))

        for error in errors:
            flash(error, "danger")

    return render_template(
        "funcionarios/form.html",
        title="Editar funcionario",
        funcionario=funcionario,
        form_data=_form_data(funcionario),
        status_choices=STATUS_CHOICES,
        action_url=url_for("funcionarios.editar", id=funcionario.id),
    )


def excluir_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    db.session.delete(funcionario)
    db.session.commit()
    flash("Funcionario excluido com sucesso.", "success")
    return redirect(url_for("funcionarios.listar"))
