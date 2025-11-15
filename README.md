目录结构说明文档：
frontend/
├── src/
│   ├── pages/                    # 页面文件目录
│   │   ├── login/               # 登录页面 - 用户认证入口
│   │   ├── register/            # 注册页面 - 新用户注册
│   │   ├── index/               # 首页 - 功能导航和概览
│   │   ├── chat/                # 聊天页面 - AI心理对话
│   │   ├── emotion/             # 情感分析页面 - 情绪数据可视化
│   │   ├── knowledge/           # 知识库页面 - 心理健康文章
│   │   ├── emergency/           # 紧急求助页面 - 危机干预
│   │   └── admin/               # 管理后台 - 数据监控和管理
│   ├── stores/                  # 状态管理
│   │   ├── auth.js             # 认证状态 - 登录状态管理
│   │   └── chat.js             # 聊天状态 - 对话记录管理
│   ├── api/                     # API接口调用
│   │   ├── auth.js             # 认证接口 - 登录注册API
│   │   ├── chat.js             # 聊天接口 - 对话API
│   │   ├── emotion.js          # 情感接口 - 情绪数据API
│   │   ├── knowledge.js        # 知识库接口 - 文章API
│   │   └── admin.js            # 管理接口 - 后台API
│   ├── utils/                   # 工具函数
│   │   └── request.js          # 请求封装 - HTTP请求统一处理
│   ├── App.vue                 # 应用入口 - 全局配置
│   └── main.js                 # 主程序 - Vue应用初始化
├── static/                     # 静态资源
│   └── tabbar/                 # 底部导航图标
├── manifest.json               # 应用配置 - UniApp应用配置
├── pages.json                  # 页面配置 - 路由和页面设置
├── package.json               # 项目配置 - 依赖包管理
└── index.html                 # HTML模板 - 页面基础结构
backend/
├── app/
│   ├── routes/                 # 路由处理
│   │   ├── auth.py           # 认证路由 - 登录注册处理
│   │   ├── chat.py           # 聊天路由 - 对话消息处理
│   │   ├── emotion.py        # 情感路由 - 情绪数据分析
│   │   ├── admin.py          # 管理路由 - 后台功能处理
│   │   └── knowledge.py      # 知识库路由 - 文章管理
│   ├── utils/                 # 工具类
│   │   ├── ollama_client.py  # AI客户端 - Ollama模型调用
│   │   └── emotion_analyzer.py # 情感分析器 - 情绪识别算法
│   ├── __init__.py           # 应用初始化
│   └── models.py             # 数据模型 - 数据库表定义
├── config.py                 # 配置文件 - 系统参数设置
├── run.py                   # 启动文件 - 应用启动入口
├── requirements.txt         # 依赖列表 - Python包依赖
└── init_database.py        # 数据库初始化 - 初始数据创建
users/                        # 用户表 - 存储用户基本信息
├── id                      # 主键ID - 唯一标识
├── student_id              # 学号 - 登录账号
├── username                # 用户名 - 显示名称
├── password_hash           # 密码哈希 - 加密存储
├── emergency_contact       # 紧急联系人 - 危机通知
├── role                   # 用户角色 - 学生/管理员
├── created_at             # 创建时间 - 注册时间
└── last_login             # 最后登录 - 活跃时间
数据库表:
dialogs/                    # 对话记录表 - 存储聊天记录
├── id                     # 主键ID - 唯一标识
├── user_id                # 用户ID - 关联用户
├── role                   # 消息角色 - 用户/AI
├── content                # 消息内容 - 对话文本
├── emotion_score          # 情感分数 - 情绪分析结果
└── created_at             # 创建时间 - 消息时间

emergency_records/          # 紧急记录表 - 危机预警记录
├── id                     # 主键ID - 唯一标识
├── user_id                # 用户ID - 关联用户
├── triggered_at           # 触发时间 - 预警时间
├── status                 # 处理状态 - 待处理/已处理
├── handled_by             # 处理人 - 管理员名称
└── notes                  # 处理备注 - 处理说明

knowledge_base/            # 知识库表 - 心理健康文章
├── id                     # 主键ID - 唯一标识
├── title                  # 文章标题 - 文章名称
├── content                # 文章内容 - 详细内容
├── category               # 文章分类 - 类型标签
├── author                 # 作者 - 发布者
├── created_at             # 创建时间 - 发布时间
└── updated_at             # 更新时间 - 修改时间
