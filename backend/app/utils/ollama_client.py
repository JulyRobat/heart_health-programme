import requests
import json
from config import Config


class OllamaClient:
    def __init__(self):
        self.base_url = Config.OLLAMA_BASE_URL
        self.model = Config.OLLAMA_MODEL

    def generate_response(self, prompt, context=None):
        """生成AI回复 - 增强版本"""
        try:
            messages = []

            # 心理咨询师系统角色设定
            system_prompt = """你是一名专业的心理咨询师，具有丰富的心理健康支持经验。
            请遵循以下原则：
            1. 以温暖、支持、共情的态度回应
            2. 避免给出医学诊断
            3. 鼓励用户寻求专业帮助
            4. 对于危机情况，提供紧急帮助资源
            5. 保持对话的自然和流畅

            重要：如果用户表达自杀、自残等极端想法，请：
            - 表达关心和理解
            - 提供紧急求助电话（如心理危机干预热线）
            - 鼓励联系信任的人
            - 建议寻求专业心理咨询"""

            messages.append({"role": "system", "content": system_prompt})

            # 添加上下文对话
            if context:
                for msg in context[-6:]:  # 最近6条消息作为上下文
                    role = "user" if msg['role'] == 'user' else "assistant"
                    messages.append({"role": role, "content": msg['content']})

            # 添加当前消息
            messages.append({"role": "user", "content": prompt})

            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 40
                }
            }

            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=60  # 增加超时时间
            )

            if response.status_code == 200:
                result = response.json()
                return result['message']['content']
            else:
                print(f"Ollama API错误: {response.status_code}")
                return "抱歉，我现在有些忙碌。请稍后再试，或者联系我们的心理支持团队。"

        except requests.exceptions.Timeout:
            return "响应超时，请稍后再试。如果您需要紧急帮助，请拨打心理危机干预热线：400-161-9995"
        except Exception as e:
            print(f"Ollama API连接错误: {e}")
            return "网络连接出现问题。请检查您的网络设置，如需紧急帮助请联系：400-161-9995"