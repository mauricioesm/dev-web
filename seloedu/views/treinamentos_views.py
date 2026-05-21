from flask import render_template, request, redirect, url_for, flash
from models.treinamento_model import Treinamento
from werkzeug.security import generate_password_hash
from extensions import db


def listar_treinamento():
    treinamento = Treinamento.query.all()
    return render_template("treinamento/index_treinamento.html", treinamento=treinamento)


def detalhes_treinamento(id):
    treinamento = Treinamento.query.get_or_404(id)
    return render_template("treinamento/detalhe_treinamento.html", treinamento=treinamento)

def modificar_treinamento(id):

    treinamento = Treinamento.query.get_or_404(id)

    if not treinamento:
        return render_template("treinamento/editar_treinamento.html")
    
    if request.method == "POST":

        nova_disciplina = request.form.get("disciplina")
        nova_carga_horaria = request.form.get("carga_horaria")
        nova_capacidade = request.form.get("capacidade")

        treinamento.disciplina  = nova_disciplina
        treinamento.carga_horaria = nova_carga_horaria
        treinamento.capacidade = nova_capacidade
    
        db.session.commit()

        return redirect(url_for("treinamento.detalhes", id_treinamento=id))
       

    return render_template("treinamento/modificar_treinamento.html", treinamento=treinamento)


def deletar_treinamento(id):

    treinamento = Treinamento.query.get_or_404(id)

    if not treinamento:
        flash("Treinamento não encontrado.", "error")
        return redirect(url_for("treinamento.listar"))

    if request.method == "POST":
        
        id_treinamento = request.form.get("id_treinamento")
        
        db.session.delete(treinamento)
        db.session.commit()

        return redirect(url_for("treinamento.listar"))

    return render_template("treinamento/deletar_treinamento.html", treinamento=treinamento)


def criar_treinamento():

    if request.method == "POST":
        disciplina = request.form.get("disciplina")
        carga_horaria = request.form.get("carga_horaria")
        capacidade = request.form.get("capacidade")

        if Treinamento.query.filter_by(disciplina=disciplina).first():
            flash("Treinamento já cadastrado. Por favor, use outro treinamento.", "error")

        treinamento = Treinamento(
            disciplina = disciplina,
            carga_horaria = carga_horaria,
            capacidade = capacidade
        )

        try:
            db.session.add(treinamento)
            db.session.commit()
            return render_template("treinamento/detalhe_treinamento.html", treinamento=treinamento)
        except Exception as e:
            db.session.rollback()
            return render_template("treinamento/criar_treinamento.html")

    return render_template("treinamento/criar_treinamento.html")

