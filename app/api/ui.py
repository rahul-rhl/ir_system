from flask import render_template, request, jsonify
from app.api import bp
from app.services.response_generator import generate_response


@bp.route('/ask', methods=['GET', 'POST'])
def ask():
    answer_data = None

    if request.method == 'POST':
        question = request.form.get("question")

        result = generate_response(question)
        answer_data = {
            "answer": result.get("answer"),
            "confidence": result.get("confidence"),
            "sources": result.get("sources"),
        }

    return render_template("ask.html", result=answer_data)
