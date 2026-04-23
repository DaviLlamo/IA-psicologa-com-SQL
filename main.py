from fastapi import FastAPI
from database import SessionLocal
from models import Usuario, Conversa
from auth import hash_senha, verificar_senha
from ia import gerar_resposta

app = FastAPI()


# 🔹 Cadastro
@app.post("/cadastro")
def cadastro(nome: str, idade: int, senha: str):
    db = SessionLocal()

    try:
        usuario = Usuario(
            nome=nome,
            idade=idade,
            senha=hash_senha(senha)
        )

        db.add(usuario)
        db.commit()

        return {"msg": "Usuário criado"}

    finally:
        db.close()


# 🔹 Login
@app.post("/login")
def login(nome: str, senha: str):
    db = SessionLocal()

    try:
        usuario = db.query(Usuario).filter(Usuario.nome == nome).first()

        if not usuario:
            return {"erro": "Usuário não encontrado"}

        if not verificar_senha(senha, usuario.senha):
            return {"erro": "Senha incorreta"}

        return {
            "msg": "Login OK",
            "usuario_id": usuario.id
        }

    finally:
        db.close()


# 🔹 Mensagem com IA + memória
@app.post("/mensagem")
def mensagem(usuario_id: int, mensagem: str):
    db = SessionLocal()

    try:
        # 🔎 Buscar últimas 5 mensagens do usuário
        historico = db.query(Conversa)\
            .filter(Conversa.usuario_id == usuario_id)\
            .order_by(Conversa.id.desc())\
            .limit(5)\
            .all()

        # inverter ordem (mais antigo → mais novo)
        historico = list(reversed(historico))

        # 🤖 Gerar resposta com IA (Gemini)
        resposta = gerar_resposta(mensagem, historico)

        # 💾 Salvar no banco
        conversa = Conversa(
            usuario_id=usuario_id,
            mensagem_usuario=mensagem,
            resposta_ia=resposta
        )

        db.add(conversa)
        db.commit()

        return {"resposta": resposta}

    finally:
        db.close()