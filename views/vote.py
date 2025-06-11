from flask import Blueprint, request, jsonify
from models import db, Vote, User, Question, Answer

vote_bp = Blueprint("vote_bp", __name__)

# Create a vote
@vote_bp.route("/votes", methods=["POST"])
def create_vote():
    data = request.get_json()

    user_id = data.get("user_id")
    value = data.get("value")
    question_id = data.get("question_id")
    answer_id = data.get("answer_id")

    if not user_id or value not in [1, -1]:
        return jsonify({"error": "user_id and valid vote value (1 or -1) are required"}), 400

    if question_id and answer_id:
        return jsonify({"error": "Vote must target either a question or an answer, not both"}), 400

    if not User.query.get(user_id):
        return jsonify({"error": "User not found"}), 404

    if question_id:
        if not Question.query.get(question_id):
            return jsonify({"error": "Question not found"}), 404
        vote = Vote(user_id=user_id, value=value, question_id=question_id)
    elif answer_id:
        if not Answer.query.get(answer_id):
            return jsonify({"error": "Answer not found"}), 404
        vote = Vote(user_id=user_id, value=value, answer_id=answer_id)
    else:
        return jsonify({"error": "question_id or answer_id is required"}), 400

    db.session.add(vote)
    db.session.commit()
    return jsonify({"success": "Vote recorded"}), 201

# Get all votes
@vote_bp.route("/votes", methods=["GET"])
def get_all_votes():
    votes = Vote.query.all()
    data = []
    for v in votes:
        data.append({
            "id": v.id,
            "user_id": v.user_id,
            "question_id": v.question_id,
            "answer_id": v.answer_id,
            "value": v.value,
            "created_at": v.created_at
        })
    return jsonify(data), 200
