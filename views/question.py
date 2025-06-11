from flask import Blueprint, request, jsonify
from models import db, Question, User

question_bp = Blueprint("question_bp", __name__)

# Create a new question
@question_bp.route("/questions", methods=["POST"])
def create_question():
    data = request.get_json()

    title = data.get("title")
    body = data.get("body")
    tags = data.get("tags")
    user_id = data.get("user_id")

    if not title or not body or not tags or not user_id:
        return jsonify({"error": "Title, body, tags, and user_id are required"}), 400

    if Question.query.filter_by(title=title).first():
        return jsonify({"error": "Question with this title already exists"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    question = Question(title=title, body=body, tags=tags, user_id=user_id)
    db.session.add(question)
    db.session.commit()

    return jsonify({"success": "Question created successfully"}), 201

# Get a specific question by ID
@question_bp.route("/questions/<int:question_id>", methods=["GET"])
def get_question(question_id):
    question = Question.query.get(question_id)

    if not question:
        return jsonify({"error": "Question not found"}), 404

    question_data = {
        "id": question.id,
        "title": question.title,
        "body": question.body,
        "tags": question.tags,
        "is_approved": question.is_approved,
        "user_id": question.user_id,
        "created_at": question.created_at
    }

    return jsonify(question_data), 200

# Get all questions
@question_bp.route("/questions", methods=["GET"])
def get_all_questions():
    questions = Question.query.all()
    all_data = []
    for q in questions:
        all_data.append({
            "id": q.id,
            "title": q.title,
            "body": q.body,
            "tags": q.tags,
            "is_approved": q.is_approved,
            "user_id": q.user_id,
            "created_at": q.created_at
        })
    return jsonify(all_data), 200

# Delete a question by ID
@question_bp.route("/questions/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    question = Question.query.get(question_id)

    if not question:
        return jsonify({"error": "Question not found"}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({"success": "Question deleted successfully"}), 200

# Approve a question (admin action)
@question_bp.route("/questions/<int:question_id>/approve", methods=["PATCH"])
def approve_question(question_id):
    question = Question.query.get(question_id)

    if not question:
        return jsonify({"error": "Question not found"}), 404

    question.is_approved = True
    db.session.commit()
    return jsonify({"success": "Question approved"}), 200
