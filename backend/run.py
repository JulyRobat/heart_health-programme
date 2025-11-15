from app import create_app

app = create_app()

if __name__ == '__main__':
    print("🚀 启动心理健康支持系统...")
    print("📡 服务地址: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)