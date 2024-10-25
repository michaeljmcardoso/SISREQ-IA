import google.generativeai as genai
import PySimpleGUI as sg
import constantes
import config

def main():
    genai.configure(api_key=constantes.CHAVE_API)

    modelo = config.MODELO

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