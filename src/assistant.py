import os
import time
import pandas as pd
import streamlit as st
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

CHAVE_API = os.getenv('CHAVE_API')

# Configuração da API Gemini
genai.configure(api_key=os.environ["CHAVE_API"])

def convert_excel_to_csv(uploaded_file):
    """Converte um arquivo Excel para CSV usando o buffer de upload."""
    csv_path = "temp_converted_file.csv"  # Nome temporário para salvar o CSV
    df = pd.read_excel(uploaded_file)  # Lê o arquivo diretamente do buffer
    df.to_csv(csv_path, index=False)
    return csv_path

def upload_to_gemini(path, mime_type=None):
    """Faz upload do arquivo especificado para o Gemini."""
    try:
        file = genai.upload_file(path, mime_type=mime_type)
        return file
    except Exception as e:
        st.error(f"Erro no upload do arquivo: {e}")
        return None

def wait_for_files_active(files):
    """Aguarda até que os arquivos estejam ativos para uso."""
    try:
        for name in (file.name for file in files if file):
            file = genai.get_file(name)
            while file.state.name == "PROCESSING":
                time.sleep(10)
                file = genai.get_file(name)
            if file.state.name != "ACTIVE":
                st.error(f"Arquivo {file.name} falhou no processamento.")
                return False
        return True
    except Exception as e:
        st.error(f"Erro ao aguardar o processamento do arquivo: {e}")
        return False

# Configuração do modelo e da sessão de chat
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "Você é um assistente virtual especialista em processos de regularização fundiária de territórios quilombolas "
        "do Instituto Nacional de Colonização e Reforma Agrária. Responda conforme for perguntado. Mantenha-se no contexto "
        "da regularização quilombola. Se for perguntado fora desse contexto, informe que não pode ajudar. "
        "O tom da conversa deve ser amigável, utilize emojis nas respostas. "
        "Você tem acesso aos dados reais e atuais de todos os processos de regularização quilombola do INCRA no Maranhão."
    ),
)

# Inicializa as variáveis de estado para manter o status do upload e dos arquivos
if "upload_successful" not in st.session_state:
    st.session_state["upload_successful"] = False
if "files" not in st.session_state:
    st.session_state["files"] = None

# Interface com Streamlit
st.title("Assistente de Regularização de Territórios Quilombolas")

uploaded_file = st.file_uploader("Selecione o arquivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file and not st.session_state["upload_successful"]:
    csv_path = convert_excel_to_csv(uploaded_file)
    st.info("Arquivo carregado com sucesso. Iniciando upload...")

    gemini_file = upload_to_gemini(csv_path, mime_type="text/csv")
    
    if gemini_file:
        st.session_state["files"] = [gemini_file]
        if wait_for_files_active(st.session_state["files"]):
            st.session_state["upload_successful"] = True
            st.success("Arquivo processado e pronto para interação!")

# Exibe a caixa de input e a interação do chat somente após o upload e processamento bem-sucedidos
if st.session_state["upload_successful"]:
    # Inicia a sessão de chat
    chat_session = model.start_chat(history=[{"role": "user", "parts": [st.session_state["files"][0]]}])
    user_input = st.text_input("Digite sua pergunta:")
    
    if user_input:
        response = chat_session.send_message(user_input)
        st.write("Resposta:", response.text)

        # Botão para baixar a resposta
        st.download_button(
            label="Baixar resposta",
            data=response.text,
            file_name="resposta.txt",
            mime="text/plain"
        )
else:
    if not st.session_state["upload_successful"]:
        st.warning("Por favor, carregue um arquivo para começar.")
