from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import or_

from extensions import db
from models.treinamento_model import Treinamento
from utils.form_validators import clean_text, parse_positive_int, require_fields
from utils.pagination import paginate_query


STATUS_CHOICES = ("ativo", "inativo", "rascunho")


def _form_data(treinamento=None):
    if request.method == "POST":
        return request.form

    return {
        "titulo": treinamento.titulo if treinamento else "",
        "descricao": treinamento.descricao if treinamento else "",
        "carga_horaria": treinamento.carga_horaria if treinamento else 1,
        "status": treinamento.status if treinamento else "ativo",
    }


def _validate_treinamento():
    errors = []
    require_fields(request.form, [("titulo", "Titulo")], errors)

    status = clean_text(request.form.get("status")) or "ativo"
    if status not in STATUS_CHOICES:
        errors.append("Status invalido.")

    carga_horaria = parse_positive_int(
        request.form.get("carga_horaria"),
        "Carga horaria",
        errors,
    )

    return errors, {
        "titulo": clean_text(request.form.get("titulo")),
        "descricao": clean_text(request.form.get("descricao")),
        "carga_horaria": carga_horaria,
        "status": status,
    }


def listar_treinamentos():
    busca = clean_text(request.args.get("q"))
    status = clean_text(request.args.get("status"))
    page = request.args.get("page", 1, type=int)

    query = Treinamento.query
    if busca:
        like = f"%{busca}%"
        query = query.filter(
            or_(
                Treinamento.titulo.ilike(like),
                Treinamento.descricao.ilike(like),
            )
        )
    if status:
        query = query.filter_by(status=status)

    pagination = paginate_query(
        query.order_by(Treinamento.data_criacao.desc()),
        page,
    )
    return render_template(
        "treinamentos/index.html",
        treinamentos=pagination.items,
        pagination=pagination,
        busca=busca,
        status=status,
        status_choices=STATUS_CHOICES,
    )


def criar_treinamento():
    if request.method == "POST":
        errors, data = _validate_treinamento()
        if not errors:
            treinamento = Treinamento(**data)
            db.session.add(treinamento)
            db.session.commit()
            flash("Treinamento cadastrado com sucesso.", "success")
            return redirect(url_for("treinamentos.detalhes", id=treinamento.id))

        for error in errors:
            flash(error, "danger")

    return render_template(
        "treinamentos/form.html",
        title="Novo treinamento",
        form_data=_form_data(),
        status_choices=STATUS_CHOICES,
        action_url=url_for("treinamentos.criar"),
    )


def detalhes_treinamento(id):
    treinamento = Treinamento.query.get_or_404(id)
    return render_template("treinamentos/detalhes.html", treinamento=treinamento)


def editar_treinamento(id):
    treinamento = Treinamento.query.get_or_404(id)
    if request.method == "POST":
        errors, data = _validate_treinamento()
        if not errors:
            for field, value in data.items():
                setattr(treinamento, field, value)
            db.session.commit()
            flash("Treinamento atualizado com sucesso.", "success")
            return redirect(url_for("treinamentos.detalhes", id=treinamento.id))

        for error in errors:
            flash(error, "danger")

    return render_template(
        "treinamentos/form.html",
        title="Editar treinamento",
        treinamento=treinamento,
        form_data=_form_data(treinamento),
        status_choices=STATUS_CHOICES,
        action_url=url_for("treinamentos.editar", id=treinamento.id),
    )


def excluir_treinamento(id):
    treinamento = Treinamento.query.get_or_404(id)
    db.session.delete(treinamento)
    db.session.commit()
    flash("Treinamento excluido com sucesso.", "success")
    return redirect(url_for("treinamentos.listar"))
