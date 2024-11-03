import os
import time
import pandas as pd
import google.generativeai as genai
from tkinter import Tk, filedialog

def setup_api_key():
    """Solicita ao usuário uma chave API e configura o Gemini."""
    api_key = input("Insira sua chave API do Gemini (ou pressione Enter para mais informações): ")
    if not api_key:
        print("A chave GEMINI não pode ser vazia. Para obter uma chave API Gemini, acesse: https://aistudio.google.com/app/apikey")
        api_key = input("Insira a chave API do Gemini aqui: ")
    genai.configure(api_key=api_key)
    print("Chave API GEMINI configurada com sucesso! 🎉\n")

def convert_excel_to_csv(excel_path):
    """Converte um arquivo Excel para CSV e retorna o caminho do CSV."""
    csv_path = excel_path.replace(".xlsx", ".csv")
    df = pd.read_excel(excel_path)
    df.to_csv(csv_path, index=False)
    return csv_path

def upload_to_gemini(path, mime_type=None):
    """Faz upload do arquivo especificado para o Gemini."""
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Arquivo '{file.display_name}' carregado com sucesso: {file.uri}\n")
    return file

def wait_for_files_active(files):
    """Aguarda até que os arquivos estejam ativos para uso."""
    print("Aguardando o processamento do arquivo...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"Arquivo {file.name} falhou no processamento")
    print("\nTodos os arquivos estão prontos.🎉")

def select_file():
    """Abre um diálogo para o usuário selecionar um arquivo local."""
    root = Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter
    file_path = filedialog.askopenfilename(
        title="Selecione o arquivo para carregar",
        filetypes=[("Excel Files", "*.xlsx"), ("Todos os arquivos", "*.*")]
    )
    return file_path

# Configuração da API Gemini
setup_api_key()

# Configuração do modelo e da sessão de chat
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

system_instruction = input(
    "Insira as instruções para o assistente (ou pressione Enter para usar o padrão):\n"
    "Exemplo de instrução padrão: 'Você é um assistente virtual especialista em...'\n"
)

if not system_instruction:
    system_instruction = (
        "Você é um assistente virtual"
        "Use os dados fornecidos no arquivo do usuário para responder às perguntas"
        "Responda conforme o contexto fornecido no arquivo."
    )

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=system_instruction,
)

# Interface de upload e preparação do arquivo
file_path = select_file()
if not file_path:
    print("Nenhum arquivo selecionado. Por favor, tente novamente.")
else:
    # Converte o arquivo Excel para CSV antes de enviá-lo
    csv_path = convert_excel_to_csv(file_path)
    files = [upload_to_gemini(csv_path, mime_type="text/csv")]

    # Aguarda o processamento do arquivo
    wait_for_files_active(files)

    # Inicia a sessão de chat
    chat_session = model.start_chat(history=[{"role": "user", "parts": [files[0]]}])

    # Loop de interação com o usuário
    print("Assistente iniciado e pronto para interação!")
    while True:
        user_input = input("Pergunta: ")
        if user_input.lower() in ["sair", "exit", "quit"]:
            print("Encerrando o assistente. Até mais!")
            break
        
        response = chat_session.send_message(user_input)
        print("Resposta:", response.text)
