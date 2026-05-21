from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import or_

from extensions import db
from models.treinamento_model import Treinamento
from models.turma_model import Turma
from utils.form_validators import clean_text, parse_date, parse_positive_int, require_fields
from utils.pagination import paginate_query


STATUS_CHOICES = ("planejada", "em_andamento", "encerrada")


def _treinamentos():
    return Treinamento.query.order_by(Treinamento.titulo.asc()).all()


def _form_data(turma=None):
    if request.method == "POST":
        return request.form

    return {
        "nome": turma.nome if turma else "",
        "treinamento_id": turma.treinamento_id if turma else "",
        "vagas": turma.vagas if turma else 20,
        "data_inicio": turma.data_inicio.isoformat() if turma and turma.data_inicio else "",
        "data_fim": turma.data_fim.isoformat() if turma and turma.data_fim else "",
        "status": turma.status if turma else "planejada",
    }


def _validate_turma():
    errors = []
    require_fields(
        request.form,
        [("nome", "Nome"), ("treinamento_id", "Treinamento")],
        errors,
    )

    treinamento_id = parse_positive_int(
        request.form.get("treinamento_id"),
        "Treinamento",
        errors,
    )
    if treinamento_id and not db.session.get(Treinamento, treinamento_id):
        errors.append("Treinamento informado nao existe.")

    vagas = parse_positive_int(request.form.get("vagas"), "Vagas", errors)
    status = clean_text(request.form.get("status")) or "planejada"
    if status not in STATUS_CHOICES:
        errors.append("Status invalido.")

    data_inicio = parse_date(request.form.get("data_inicio"), "Data de inicio", errors)
    data_fim = parse_date(request.form.get("data_fim"), "Data de encerramento", errors)
    if data_inicio and data_fim and data_fim < data_inicio:
        errors.append("Data de encerramento nao pode ser anterior ao inicio.")

    return errors, {
        "nome": clean_text(request.form.get("nome")),
        "treinamento_id": treinamento_id,
        "vagas": vagas,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "status": status,
    }


def listar_turmas():
    busca = clean_text(request.args.get("q"))
    status = clean_text(request.args.get("status"))
    treinamento_id = request.args.get("treinamento_id", type=int)
    page = request.args.get("page", 1, type=int)

    query = Turma.query.filter_by(ativo=True)
    if busca:
        like = f"%{busca}%"
        query = query.filter(
            or_(
                Turma.nome.ilike(like),
                Turma.treinamento.has(Treinamento.titulo.ilike(like)),
            )
        )
    if status:
        query = query.filter_by(status=status)
    if treinamento_id:
        query = query.filter_by(treinamento_id=treinamento_id)

    pagination = paginate_query(query.order_by(Turma.criado_em.desc()), page)
    return render_template(
        "turmas/index.html",
        turmas=pagination.items,
        pagination=pagination,
        busca=busca,
        status=status,
        treinamento_id=treinamento_id,
        status_choices=STATUS_CHOICES,
        treinamentos=_treinamentos(),
    )


def criar_turma():
    if request.method == "POST":
        errors, data = _validate_turma()
        if not errors:
            turma = Turma(**data)
            db.session.add(turma)
            db.session.commit()
            flash("Turma cadastrada com sucesso.", "success")
            return redirect(url_for("turmas.listar"))

        for error in errors:
            flash(error, "danger")

    return render_template(
        "turmas/form.html",
        title="Nova turma",
        form_data=_form_data(),
        status_choices=STATUS_CHOICES,
        treinamentos=_treinamentos(),
        action_url=url_for("turmas.criar"),
    )


def editar_turma(id):
    turma = Turma.query.filter_by(id=id, ativo=True).first_or_404()
    if request.method == "POST":
        errors, data = _validate_turma()
        if not errors:
            for field, value in data.items():
                setattr(turma, field, value)
            db.session.commit()
            flash("Turma atualizada com sucesso.", "success")
            return redirect(url_for("turmas.listar"))

        for error in errors:
            flash(error, "danger")

    return render_template(
        "turmas/form.html",
        title="Editar turma",
        turma=turma,
        form_data=_form_data(turma),
        status_choices=STATUS_CHOICES,
        treinamentos=_treinamentos(),
        action_url=url_for("turmas.editar", id=turma.id),
    )


def excluir_turma(id):
    turma = Turma.query.filter_by(id=id, ativo=True).first_or_404()
    turma.ativo = False
    db.session.commit()
    flash("Turma excluida com sucesso.", "success")
    return redirect(url_for("turmas.listar"))
