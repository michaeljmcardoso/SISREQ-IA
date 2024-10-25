import google.generativeai as genai
import PySimpleGUI as sg
import constantes
import os
from config import MODELO
from dotenv import load_dotenv

load_dotenv()

CHAVE_API = os.getenv('CHAVE_API')

def main():
    genai.configure(api_key=CHAVE_API)

    modelo = MODELO

    chat = modelo.start_chat(history=[])

    def chat_loop():
        treinamento = constantes.TREINAMENTO

        sg.theme(constantes.TEMA_JANELA)

        layout = constantes.LAYOUT_JANELA

        janela = sg.Window('SISREQ_IA', layout, resizable=True, size=(700, 510))

        while True:
            event, values = janela.read()

            if event == sg.WIN_CLOSED or event == '-SAIR-':
                break

            if event == '-ENVIAR-':
                prompt = values['-ENTRADA-']
                response = chat.send_message(f'{treinamento} {prompt}')
                janela['-SAIDA-'](f'SISREQ_IA: {response.text}\n')
                janela['-ENTRADA-'].update('')

        janela.close()

    chat_loop()

if __name__ == "__main__":
    main()