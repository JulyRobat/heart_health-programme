# backend/init_database.py
from app import create_app, db
from app.models import User, Dialog, EmergencyRecord, KnowledgeBase


def init_database():
    app = create_app()

    with app.app_context():
        # 删除所有表并重新创建
        db.drop_all()
        db.create_all()

        print("创建表结构...")

        # 创建默认管理员
        admin = User(
            student_id='admin',
            username='系统管理员',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # 创建测试学生
        test_student = User(
            student_id='20210001',
            username='测试学生',
            emergency_contact='13800138000',
            role='student'
        )
        test_student.set_password('123456')
        db.session.add(test_student)

        # 添加示例知识库文章
        articles = [
            {
                'title': '如何应对学习压力',
                'content': '学习压力是学生常见的问题，可以通过时间管理、适当休息、运动等方式缓解...',
                'category': '压力管理',
                'author': '心理咨询中心'
            },
            {
                'title': '改善睡眠质量的方法',
                'content': '良好的睡眠对心理健康至关重要，建议保持规律作息、创造舒适的睡眠环境...',
                'category': '睡眠健康',
                'author': '心理咨询中心'
            }
        ]

        for article_data in articles:
            article = KnowledgeBase(**article_data)
            db.session.add(article)

        try:
            db.session.commit()
            print("数据库初始化成功！")
            print("管理员账号: admin / admin123")
            print("测试学生账号: 20210001 / 123456")
        except Exception as e:
            db.session.rollback()
            print(f"数据库初始化失败: {e}")


if __name__ == '__main__':
    init_database()