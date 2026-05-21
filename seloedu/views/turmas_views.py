from flask import render_template, request, redirect, url_for, flash
from models.turma_model import Turma
from werkzeug.security import generate_password_hash
from extensions import db


def listar_turma():
    turma = Turma.query.all()
    return render_template("turma/index_turma.html", turma=turma)


def detalhes_turma(id):
    turma = Turma.query.get_or_404(id)
    return render_template("turma/detalhe_turma.html", turma=turma)

def modificar_turma(id):

    turma = Turma.query.get_or_404(id)

    if not turma:
        return render_template("turma/editar_turma.html")
    
    if request.method == "POST":

        nova_qtd_funcionarios = request.form.get("qtd_funcionarios")
        
        turma.qtd_funcionarios = nova_qtd_funcionarios
    
        db.session.commit()

        return redirect(url_for("turma.detalhes", id_turma=id))
       

    return render_template("turma/modificar_turma.html", turma=turma)


def deletar_turma(id):

    turma = Turma.query.get_or_404(id)

    if not turma:
        flash("Turma não encontrada.", "error")
        return redirect(url_for("turma.listar"))

    if request.method == "POST":
        
        id_turma = request.form.get("id_turma")
        
        db.session.delete(turma)
        db.session.commit()

        return redirect(url_for("turma.listar"))

    return render_template("turma/deletar_turma.html", turma=turma)


def criar_turma():

    if request.method == "POST":
        qtd_funcionarios = request.form.get("qtd_funcionarios")

        if Turma.query.first():
            flash("Turma já cadastrada. Por favor, use outra turma.", "error")

        turma = Turma(
            qtd_funcionarios = qtd_funcionarios
        )

        try:
            db.session.add(turma)
            db.session.commit()
            return render_template("turma/detalhe_turma.html", turma=turma)
        except Exception as e:
            db.session.rollback()
            return render_template("turma/criar_turma.html")

    return render_template("turma/criar_turma.html")

