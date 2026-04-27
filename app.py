from fastapi import FastAPI

app = FastAPI()


@app.get("/ListarTodosOsAlunos")
def listar_alunos():
    return alunos 


@app.get("/alunos")
def remover_alunos(aluno_id: int):
    for aluno in alunos:
        if aluno["Sexo"] == "M":
            alunos.remove(aluno)
            return {"message": f"Aluno com id {aluno_id} removido com sucesso."}
    return {"message": f"Aluno com id {aluno_id} não encontrado."}

@app.post("/alunos")
def adicionar_aluno(id: int, nome: str, idade: int, Sexo: str):
    novo_aluno = {"id": id, "nome": nome, "idade": idade, "Sexo": Sexo}
    alunos.append(novo_aluno)
    return {"message": f"Aluno {nome} adicionado com sucesso."}

#Alunos
alunos = [
    {"id": 1, "nome": "Pedro", "idade": 99, "Sexo": "F"},
    {"id": 2, "nome": "Ana", "idade": 22, "Sexo": "M"}
]