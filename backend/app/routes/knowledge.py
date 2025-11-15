from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import KnowledgeBase

knowledge_bp = Blueprint('knowledge', __name__)


@knowledge_bp.route('/articles', methods=['GET'])
@jwt_required()
def get_knowledge_articles():
    """获取知识库文章"""
    category = request.args.get('category')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = KnowledgeBase.query

    if category:
        query = query.filter_by(category=category)

    articles = query.order_by(KnowledgeBase.created_at.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    article_list = []
    for article in articles.items:
        article_list.append({
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'category': article.category,
            'author': article.author,
            'created_at': article.created_at.isoformat()
        })

    return jsonify({
        'articles': article_list,
        'total': articles.total,
        'pages': articles.pages,
        'current_page': page
    }), 200