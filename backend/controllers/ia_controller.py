from flask import Blueprint, request, jsonify
import openai
from config import OPENAI_API_KEY

ia_controller = Blueprint('ia_controller', __name__)
openai.api_key = OPENAI_API_KEY

@ia_controller.route('/ia/sugestao', methods=['POST'])
def ia_sugestao():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'erro': 'Texto não informado'}), 400

    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é uma especialista em construção civil chamada Clarice. Responda de forma inteligente e prática."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        return jsonify({
            "resposta": resposta['choices'][0]['message']['content'].strip()
        })

    except Exception as e:
        return jsonify({'erro': str(e)}), 500