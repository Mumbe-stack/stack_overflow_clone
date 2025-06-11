from flask import Blueprint, request, jsonify
from models import db, Answer, User, Question

answer_bp = Blueprint("answer_bp", __name__)

# Create an answer
@answer_bp.route("/answers", methods=["POST"])
def create_answer():
    data = request.get_json()

    user_id = data.get("user_id")
    question_id = data.get("question_id")
    body = data.get("body")

    if not user_id or not question_id or not body:
        return jsonify({"error": "user_id, question_id, and body are required"}), 400

    if not User.query.get(user_id):
        return jsonify({"error": "User not found"}), 404

    if not Question.query.get(question_id):
        return jsonify({"error": "Question not found"}), 404

    answer = Answer(user_id=user_id, question_id=question_id, body=body)
    db.session.add(answer)
    db.session.commit()

    return jsonify({"success": "Answer created"}), 201

# Get all answers
@answer_bp.route("/answers", methods=["GET"])
def get_all_answers():
    answers = Answer.query.all()
    results = []
    for a in answers:
        results.append({
            "id": a.id,
            "user_id": a.user_id,
            "question_id": a.question_id,
            "body": a.body,
            "is_hidden": a.is_hidden,
            "created_at": a.created_at
        })
    return jsonify(results), 200

# Get answers for a question
@answer_bp.route("/questions/<int:question_id>/answers", methods=["GET"])
def get_answers_for_question(question_id):
    answers = Answer.query.filter_by(question_id=question_id).all()
    results = []
    for a in answers:
        results.append({
            "id": a.id,
            "user_id": a.user_id,
            "question_id": a.question_id,
            "body": a.body,
            "is_hidden": a.is_hidden,
            "created_at": a.created_at
        })
    return jsonify(results), 200

# Delete an answer
@answer_bp.route("/answers/<int:answer_id>", methods=["DELETE"])
def delete_answer(answer_id):
    answer = Answer.query.get(answer_id)
    if not answer:
        return jsonify({"error": "Answer not found"}), 404
    db.session.delete(answer)
    db.session.commit()
    return jsonify({"success": "Answer deleted"}), 200
