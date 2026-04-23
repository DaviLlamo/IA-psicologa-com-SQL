from google import genai

# 🔑 COLOCA SUA CHAVE AQUI
client = genai.Client(api_key="coloca a chave api aki")


def gerar_resposta(mensagem, historico):

    contexto = ""

    for h in historico:
        contexto += f"[{h.criado_em}] Usuário: {h.mensagem_usuario}\nIA: {h.resposta_ia}\n"

    prompt = f"""
    Você é uma IA psicóloga empática e acolhedora.

    Regras:
    - Valide o sentimento do usuário
    - Demonstre compreensão emocional
    - Faça perguntas abertas
    - Seja natural (não robótica)
    - Se o usuário demonstrar emoções fortes (medo, ansiedade, tristeza), aprofunde mais
    - NÃO dê diagnósticos médicos
    IMPORTANTE:
    - Leve em consideração o TEMPO entre as mensagens
    - Mudanças rápidas = possível instabilidade emocional
    - Mudanças com horas/dias = algo natural

    Histórico da conversa:
    {contexto}

    Usuário: {mensagem}
    IA:
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text