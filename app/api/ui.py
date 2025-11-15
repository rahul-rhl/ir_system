from flask import request, jsonify
from app.api import bp
from app.services.response_generator import generate_response


@bp.route('/ask-question', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get("question")

    answer = generate_response(question)

    return jsonify({"response": answer.get("answer"), "confidence":answer.get("confidence"), 
                    "sources":answer.get("sources")}), 200