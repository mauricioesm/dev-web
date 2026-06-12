from datetime import date
from flask import redirect, render_template, request, url_for
from extensions import db
from models.treinamento_models import Treinamento


def _parse_date(value):
    return date.fromisoformat(value) if value else None


def listar_treinamentos():
    treinamentos = Treinamento.query.order_by(Treinamento.data_inicio.desc()).all()
    return render_template("treinamento/index_treinamento.html", treinamentos=treinamentos)


def novo_treinamento():
    if request.method == "POST":
        treinamento = Treinamento(
            titulo=request.form.get("titulo", "").strip(),
            descricao=request.form.get("descricao", "").strip() or None,
            data_inicio=_parse_date(request.form.get("data_inicio")),
            data_fim=_parse_date(request.form.get("data_fim")),
        )
        db.session.add(treinamento)
        db.session.commit()
        return redirect(url_for("treinamento.listar"))
    return render_template("treinamento/form_treinamento.html", treinamento=None)


def editar_treinamento(id):
    treinamento = db.get_or_404(Treinamento, id)
    if request.method == "POST":
        treinamento.titulo = request.form.get("titulo", "").strip()
        treinamento.descricao = request.form.get("descricao", "").strip() or None
        treinamento.data_inicio = _parse_date(request.form.get("data_inicio"))
        treinamento.data_fim = _parse_date(request.form.get("data_fim"))
        db.session.commit()
        return redirect(url_for("treinamento.listar"))
    return render_template("treinamento/form_treinamento.html", treinamento=treinamento)


def excluir_treinamento(id):
    treinamento = db.get_or_404(Treinamento, id)
    db.session.delete(treinamento)
    db.session.commit()
    return redirect(url_for("treinamento.listar"))
