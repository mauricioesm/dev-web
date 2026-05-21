from flask import render_template, request, redirect, url_for, flash
from extensions import db
from models.treinamento_models import Treinamento
from datetime import datetime

def listar_treinamentos():
    if request.method == "POST":
        action = request.form.get("action")
        
        # Ação de Criar
        if action == "create":
            titulo = request.form.get("titulo")
            d_inicio = request.form.get("data_inicio")
            d_fim = request.form.get("data_fim")
            
            # Converte as strings de data do HTML para o formato Date do Python
            data_inicio = datetime.strptime(d_inicio, '%Y-%m-%d').date() if d_inicio else None
            data_fim = datetime.strptime(d_fim, '%Y-%m-%d').date() if d_fim else None
            
            novo_treinamento = Treinamento(titulo=titulo, data_inicio=data_inicio, data_fim=data_fim)
            db.session.add(novo_treinamento)
            db.session.commit()
            flash("Treinamento criado com sucesso!", "success")
            
        # Ação de Excluir
        elif action == "delete":
            treinamento_id = request.form.get("treinamento_id")
            treinamento = db.session.get(Treinamento, treinamento_id)
            if treinamento:
                db.session.delete(treinamento)
                db.session.commit()
                flash("Treinamento excluído com sucesso!", "success")
                
        return redirect(url_for("treinamentos.listar"))

    # Busca todos os treinamentos e manda para a tela
    treinamentos = Treinamento.query.all()
    return render_template("treinamentos/index.html", treinamentos=treinamentos)