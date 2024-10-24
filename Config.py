import google.generativeai as genai

# Configurações do modelo de geração

CONFIG_GERACAO = {
        'candidate_count': 1,
        'temperature': 0.9,
    }

CONFIG_SEGURANCA = {
        'HARASSMENT': 'BLOCK_NONE',
        'HATE': 'BLOCK_NONE',
        'SEXUAL': 'BLOCK_NONE',
        'DANGEROUS': 'BLOCK_NONE',
    }

MODELO = genai.GenerativeModel('gemini-1.5-flash', generation_config=CONFIG_GERACAO, safety_settings=CONFIG_SEGURANCA)

""" 
Use `genai.list_models` para conferir os modelos do Gemini disponíveis:

gemini-1.5-flash: modelo multimodal mais rápido

gemini-1.5-pro: modelo multimodal mais eficiente e inteligente

"""