from flask import render_template, request, redirect, url_for, flash
from models.funcionario_model import Funcionario
from extensions import db


def listar_funcionarios():
    funcionario = Funcionario.query.all()
    return render_template("funcionario/index_funcionario.html", funcionario=funcionario)


def detalhes_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    return render_template("funcionario/detalhe_funcionario.html", funcionario=funcionario)

def modificar_funcionario(id):

    funcionario = Funcionario.query.get_or_404(id)

    if not funcionario:
        return render_template("funcionario/editar_funcionario.html")
    
    if request.method == "POST":

        novo_nome = request.form.get("nome")
        nova_funcao = request.form.get("funcao")

        funcionario.nome  = novo_nome
        funcionario.funcao = nova_funcao
    
        db.session.commit()

        return redirect(url_for("funcionario.detalhes", id_funcionario=id))
       

    return render_template("funcionario/modificar_funcionario.html", funcionario=funcionario)


def deletar_funcionario(id):

    funcionario = Funcionario.query.get_or_404(id)

    if not funcionario:
        flash("Funcionário não encontrado.", "error")
        return redirect(url_for("funcionario.listar"))

    if request.method == "POST":
        
        id_funcionario = request.form.get("id_funcionario")
        
        db.session.delete(funcionario)
        db.session.commit()

        return redirect(url_for("funcionario.listar"))

    return render_template("funcionario/deletar_funcionario.html", funcionario=id_funcionario)


def criar_funcionario():

    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        funcao = request.form.get("funcao")

        if Funcionario.query.filter_by(email=email).first():
            flash("Email já cadastrado. Por favor, use outro email.", "error")

        funcionario = Funcionario(
            nome = nome,
            email = email,
            funcao = funcao,
        )

        try:
            db.session.add(funcionario)
            db.session.commit()
            return render_template("funcionario/detalhe_funcionario.html", funcionario=funcionario)
        except Exception as e:
            db.session.rollback()
            return render_template("funcionario/criar_funcionario.html")

    return render_template("funcionario/criar_funcionario.html")

