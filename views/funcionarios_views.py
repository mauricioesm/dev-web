from flask import flash, redirect, render_template, request, url_for

from extensions import db
from models.funcionario_models import Funcionario


def listar_funcionarios():
    funcionarios = Funcionario.query.order_by(Funcionario.nome).all()
    return render_template("funcionarios/index_funcionarios.html", funcionarios=funcionarios)


def criar_funcionario():
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip().lower()
    cargo = request.form.get("cargo", "").strip()
    telefone = request.form.get("telefone", "").strip()

    if not nome or not email:
        flash("Nome e e-mail são obrigatórios.", "danger")
        return redirect(url_for("funcionario.listar"))

    funcionario = Funcionario(nome=nome, email=email, cargo=cargo, telefone=telefone)
    db.session.add(funcionario)
    db.session.commit()
    flash("Funcionário cadastrado com sucesso.", "success")
    return redirect(url_for("funcionario.listar"))


def detalhes_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    return render_template("funcionarios/detalhe_funcionario.html", funcionario=funcionario)


def editar_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    if request.method == "POST":
        funcionario.nome = request.form.get("nome", funcionario.nome).strip()
        funcionario.email = request.form.get("email", funcionario.email).strip().lower()
        funcionario.cargo = request.form.get("cargo", funcionario.cargo).strip()
        funcionario.telefone = request.form.get("telefone", funcionario.telefone).strip()
        db.session.commit()
        flash("Funcionário atualizado com sucesso.", "success")
        return redirect(url_for("funcionario.detalhes", id=funcionario.id))

    return render_template("funcionarios/editar_funcionario.html", funcionario=funcionario)


def excluir_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    db.session.delete(funcionario)
    db.session.commit()
    flash("Funcionário excluído com sucesso.", "success")
    return redirect(url_for("funcionario.listar"))
