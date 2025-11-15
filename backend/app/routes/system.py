from flask import Blueprint, request, jsonify
from app.utils.ollama_client import OllamaClient

system_bp = Blueprint('system', __name__)
ollama_client = OllamaClient()


@system_bp.route('/api/system/health', methods=['GET'])
def system_health():
    """系统健康检查"""
    ollama_health = ollama_client.check_health()
    available_models = ollama_client.get_available_models()

    return jsonify({
        'success': True,
        'ollama_available': ollama_health,
        'available_models': available_models,
        'current_model': ollama_client.model
    })


@system_bp.route('/api/system/models', methods=['GET'])
def get_models():
    """获取可用的模型列表"""
    models = ollama_client.get_available_models()

    return jsonify({
        'success': True,
        'models': models
    })


@system_bp.route('/api/system/switch-model', methods=['POST'])
def switch_model():
    """切换模型"""
    data = request.get_json()
    model_name = data.get('model_name')

    if not model_name:
        return jsonify({'success': False, 'message': '模型名称不能为空'}), 400

    # 检查模型是否可用
    available_models = ollama_client.get_available_models()
    model_exists = any(model['name'] == model_name for model in available_models)

    if not model_exists:
        return jsonify({
            'success': False,
            'message': f'模型 {model_name} 不可用'
        }), 400

    # 更新模型配置
    ollama_client.model = model_name

    return jsonify({
        'success': True,
        'message': f'已切换到模型: {model_name}',
        'current_model': model_name
    })