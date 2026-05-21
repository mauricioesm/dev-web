from datetime import datetime

from flask import flash, redirect, render_template, request, url_for

from extensions import db
from models.turma_models import Turma
from models.treinamento_models import Treinamento


def parse_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def listar_treinamentos():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        local = request.form.get("local", "").strip()
        data_inicio = parse_date(request.form.get("data_inicio"))
        data_fim = parse_date(request.form.get("data_fim"))

        if not titulo:
            flash("Informe o título do treinamento.", "danger")
            return redirect(url_for("treinamento.listar"))

        treinamento = Treinamento(
            titulo=titulo,
            descricao=descricao,
            local=local,
            data_inicio=data_inicio,
            data_fim=data_fim,
        )
        db.session.add(treinamento)
        db.session.commit()
        flash("Treinamento criado com sucesso.", "success")
        return redirect(url_for("treinamento.listar"))

    treinamentos = Treinamento.query.order_by(Treinamento.data_inicio.desc().nullslast(), Treinamento.titulo).all()
    return render_template("treinamentos/index_treinamentos.html", treinamentos=treinamentos)


def criar_turma(id):
    treinamento = Treinamento.query.get_or_404(id)
    titulo = request.form.get("titulo", "").strip() or f"Turma {len(treinamento.turmas) + 1}"
    vagas = int(request.form.get("vagas", 20))
    data_inicio = parse_date(request.form.get("data_inicio"))
    data_fim = parse_date(request.form.get("data_fim"))

    turma = Turma(
        titulo=titulo,
        vagas=vagas,
        data_inicio=data_inicio,
        data_fim=data_fim,
        treinamento_id=treinamento.id,
    )
    db.session.add(turma)
    db.session.commit()
    flash("Turma criada com sucesso.", "success")
    return redirect(url_for("treinamento.detalhes", id=treinamento.id))


def detalhe_treinamento(id):
    treinamento = Treinamento.query.get_or_404(id)
    turmas = Turma.query.filter_by(treinamento_id=treinamento.id).order_by(Turma.data_inicio.asc().nullslast()).all()
    return render_template(
        "treinamentos/detalhe_treinamento.html",
        treinamento=treinamento,
        turmas=turmas,
    )


def editar_treinamento(id):
    treinamento = Treinamento.query.get_or_404(id)
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        local = request.form.get("local", "").strip()
        data_inicio = parse_date(request.form.get("data_inicio"))
        data_fim = parse_date(request.form.get("data_fim"))

        if not titulo:
            flash("Informe o título do treinamento.", "danger")
            return redirect(url_for("treinamento.editar", id=treinamento.id))

        treinamento.titulo = titulo
        treinamento.descricao = descricao
        treinamento.local = local
        treinamento.data_inicio = data_inicio
        treinamento.data_fim = data_fim
        db.session.commit()
        flash("Treinamento atualizado com sucesso.", "success")
        return redirect(url_for("treinamento.detalhes", id=treinamento.id))

    return render_template("treinamentos/editar_treinamento.html", treinamento=treinamento)


def excluir_treinamento(id):
    treinamento = Treinamento.query.get_or_404(id)
    db.session.delete(treinamento)
    db.session.commit()
    flash("Treinamento excluído com sucesso.", "success")
    return redirect(url_for("treinamento.listar"))


def excluir_turma(id):
    turma = Turma.query.get_or_404(id)
    treinamento_id = turma.treinamento_id
    db.session.delete(turma)
    db.session.commit()
    flash("Turma excluída com sucesso.", "success")
    return redirect(url_for("treinamento.detalhes", id=treinamento_id))
