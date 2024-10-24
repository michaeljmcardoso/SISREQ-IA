import google.generativeai as genai
import PySimpleGUI as sg
import Constantes
import Config

def main():
    genai.configure(api_key=Constantes.CHAVE_API)

    modelo = Config.MODELO

    chat = modelo.start_chat(history=[])

    def chat_loop():
        treinamento = Constantes.TREINAMENTO

        sg.theme(Constantes.TEMA_JANELA)

        layout = Constantes.LAYOUT_JANELA

        janela = sg.Window('SISREQ_IA - Assistante Virtual', layout, resizable=True, size=(550, 425))

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