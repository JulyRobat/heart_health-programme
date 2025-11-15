import requests
import json
import jieba
import re


class EmotionAnalyzer:
    def __init__(self):
        # 更详细的关键词库
        self.emotion_keywords = {
            'positive': ['开心', '高兴', '幸福', '满意', '放松', '平静', '希望', '自信', '乐观', '欣慰'],
            'negative': ['难过', '悲伤', '焦虑', '紧张', '愤怒', '失望', '孤独', '压力', '抑郁', '绝望'],
            'extreme': ['自杀', '自残', '不想活了', '绝望', '崩溃', '跳楼', '割腕', '安眠药', '上吊']
        }

        # 自杀风险评估模式
        self.suicide_patterns = [
            r'不想活|活不下去|不如死|死了算|离开这世界',
            r'自杀|自尽|自戕|自我了断',
            r'跳楼|跳河|上吊|割腕|吃药自杀',
            r'活着没意思|人生没意义',
            r'希望自己消失|希望从未存在'
        ]

    def analyze_emotion(self, text):
        """增强情感分析"""
        text_lower = text.lower()

        # 检测极端关键词和自杀风险
        suicide_risk = self.detect_suicide_risk(text)
        if suicide_risk:
            return 0.1, 'extreme', True  # 极低分，触发紧急预警

        # 计算情感分数
        positive_count = sum(1 for word in self.emotion_keywords['positive'] if word in text_lower)
        negative_count = sum(1 for word in self.emotion_keywords['negative'] if word in text_lower)

        total = positive_count + negative_count
        if total == 0:
            return 0.5, 'neutral', False

        score = positive_count / total

        if score > 0.6:
            emotion_type = 'positive'
        elif score < 0.4:
            emotion_type = 'negative'
        else:
            emotion_type = 'neutral'

        return score, emotion_type, False

    def detect_suicide_risk(self, text):
        """检测自杀风险"""
        text_lower = text.lower()

        # 检查极端关键词
        for word in self.emotion_keywords['extreme']:
            if word in text_lower:
                return True

        # 检查自杀相关模式
        for pattern in self.suicide_patterns:
            if re.search(pattern, text_lower):
                return True

        return False

    def get_emergency_level(self, text):
        """获取紧急级别"""
        score, emotion_type, is_extreme = self.analyze_emotion(text)

        if is_extreme:
            return 'high'
        elif emotion_type == 'negative' and score < 0.3:
            return 'medium'
        else:
            return 'low'