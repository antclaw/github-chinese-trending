# GitHub 中文热门项目排行榜

> 🌟 每天上午 8 点自动更新，收录优质中文开源项目

## 📊 数据范围

- **语言**：中文项目（主要使用中文，或中文文档）
- **来源**：GitHub Trending API + 手动精选优质项目
- **频率**：每天上午 8 点自动更新

## 🏷️ 分类方式

### 1. 编程语言分类
- Python
- JavaScript/TypeScript
- Go
- Rust
- Java
- 其他

### 2. 项目维度分类
- 🔥 AI/ML - 人工智能与机器学习
- 🌐 Web - 前端/后端/全栈
- 📱 Mobile - 移动应用
- 🗄️ Database - 数据库与数据工程
- 🔧 DevOps - 运维与工具
- 📚 Documentation - 文档与教程
- 🎨 Design - 设计与 UI/UX
- 🎮 Game - 游戏
- 📊 Analytics - 数据分析
- 🔐 Security - 安全
- 🤖 Automation - 自动化
- 📦 Other - 其他

## 🚀 使用方式

### 手动更新

```bash
# 安装依赖
pip install -r requirements.txt

# 运行更新脚本
python scripts/fetch_data.py
python scripts/classify.py
python scripts/generate_readme.py
```

### 自动更新

项目已配置 GitHub Actions，每天上午 8 点自动运行更新。

## 📈 数据来源

1. **GitHub Trending API** - 自动抓取趋势项目
2. **手动精选** - 根据项目活跃度、质量、创新性手动添加

## 📝 添加手动精选项目

在 `scripts/` 目录下的 `scraper.py` 中添加：

```python
MANUAL_PROJECTS = [
    {
        "name": "项目名称",
        "description": "项目描述",
        "url": "https://github.com/...",
        "language": "Python",
        "category": "AI/ML",
        "stars": 1000,
        "forks": 100,
        "updated_at": datetime.now().isoformat(),
        "created_at": "2026-03-15T00:00:00Z",
        "topics": ["ai", "ml"],
        "is_chinese": False
    }
]
```

## 📄 许可证

MIT License
