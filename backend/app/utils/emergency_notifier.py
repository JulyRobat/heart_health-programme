import requests
import json
from datetime import datetime
from app import db
from app.models import EmergencyRecord, User


class EmergencyNotifier:
    def __init__(self):
        # 这里可以集成短信服务API，如阿里云、腾讯云短信
        self.sms_enabled = False  # 暂时关闭真实短信，测试时改为True并配置API

    def send_emergency_sms(self, phone_number, student_name, message):
        """发送紧急短信通知"""
        if not self.sms_enabled:
            # 模拟发送，实际使用时替换为真实短信API
            print(f"【紧急通知】发送给 {phone_number}:")
            print(f"学生 {student_name} 出现心理危机: {message}")
            return True

        # 真实短信API调用示例（以阿里云为例）
        try:
            # 这里需要配置真实的短信服务
            # response = requests.post('短信API地址', data={
            #     'phone': phone_number,
            #     'template_code': 'SMS_XXXXXX',
            #     'sign_name': '心晴港湾',
            #     'template_param': json.dumps({
            #         'name': student_name,
            #         'message': message
            #     })
            # })
            return True
        except Exception as e:
            print(f"短信发送失败: {e}")
            return False

    def notify_emergency_contact(self, user_id, emergency_message):
        """通知紧急联系人"""
        try:
            user = User.query.get(user_id)
            if not user or not user.emergency_contact:
                return False

            # 创建紧急记录
            emergency_record = EmergencyRecord(
                user_id=user_id,
                triggered_at=datetime.utcnow(),
                status='pending'
            )
            db.session.add(emergency_record)
            db.session.commit()

            # 发送短信通知
            sms_message = f"【心晴港湾】您的联系人{user.username}（学号:{user.student_id}）出现心理危机，请立即关注。内容：{emergency_message[:50]}..."
            success = self.send_emergency_sms(
                user.emergency_contact,
                user.username,
                sms_message
            )

            if success:
                emergency_record.notes = f"已通知紧急联系人: {user.emergency_contact}"
                db.session.commit()

            return success

        except Exception as e:
            print(f"紧急通知处理失败: {e}")
            return False

    def notify_admin(self, user_id, emergency_message):
        """通知管理员"""
        try:
            # 这里可以发送邮件或系统内部通知
            user = User.query.get(user_id)
            print(f"【管理员通知】用户 {user.username}({user.student_id}) 触发紧急预警:")
            print(f"消息内容: {emergency_message}")
            return True
        except Exception as e:
            print(f"管理员通知失败: {e}")
            return False