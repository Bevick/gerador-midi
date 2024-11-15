import openai
import requests


openai.api_key = "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"

# URL do backend no Render
BACKEND_URL = "https://gerador-midi.onrender.com"  # Substitua pela URL do Render

def interpretar_comando(prompt):
    """
    Usa o GPT para interpretar o comando do usuário e gerar os dados musicais.
    Args:
        prompt (str): Comando textual do usuário.
    Returns:
        dict: Dados estruturados (BPM, notas, etc.).
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um especialista em criar músicas MIDI."},
            {"role": "user", "content": prompt}
        ]
    )
    return eval(response["choices"][0]["message"]["content"])

def gerar_midi(dados):
    """
    Envia os dados musicais para o backend e recebe o arquivo MIDI gerado.
    Args:
        dados (dict): Dados musicais (BPM, notas, etc.).
    Returns:
        bytes: Arquivo MIDI gerado.
    """
    resposta = requests.post(BACKEND_URL, json=dados)
    if resposta.status_code == 200:
        return resposta.content
    else:
        raise Exception(f"Erro no backend: {resposta.text}")

if __name__ == "__main__":
    prompt = input("Digite o comando para criar a música (ex: 'Crie uma música com BPM 120 e notas C, D, E, G'): ")

    try:
        dados_musicais = interpretar_comando(prompt)
        print("Dados gerados:", dados_musicais)

        arquivo_midi = gerar_midi(dados_musicais)

        with open("musica.mid", "wb") as f:
            f.write(arquivo_midi)
        print("Arquivo MIDI gerado com sucesso! Salvo como 'musica.mid'")

    except Exception as e:
        print("Erro:", e)
