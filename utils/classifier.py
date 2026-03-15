"""
项目分类器
支持编程语言分类和维度分类（AI、Web、Mobile 等）
"""

from typing import Dict, List
from utils.scraper import MANUAL_PROJECTS


class ProjectClassifier:
    """项目分类器"""

    # 维度分类映射
    CATEGORY_MAP = {
        "AI/ML": [
            "ai", "machine learning", "deep learning", "nlp", "computer vision",
            "gpt", "llm", "transformer", "neural network", "tensorflow",
            "pytorch", "keras", "scikit-learn", "data science", "ml"
        ],
        "Web": [
            "web", "frontend", "backend", "fullstack", "api", "rest",
            "graphql", "django", "flask", "fastapi", "express", "nextjs",
            "react", "vue", "angular", "svelte", "node", "javascript",
            "typescript", "html", "css", "sass", "tailwind"
        ],
        "Mobile": [
            "mobile", "android", "ios", "flutter", "react native", "swift",
            "kotlin", "xamarin", "capacitor", "ionic", "app"
        ],
        "Database": [
            "database", "sql", "nosql", "mongodb", "postgresql", "mysql",
            "redis", "elasticsearch", "influxdb", "timescaledb", "clickhouse",
            "cassandra", "dynamodb", "sqlite", "db"
        ],
        "DevOps": [
            "devops", "docker", "kubernetes", "ci/cd", "jenkins", "gitlab",
            "github actions", "terraform", "ansible", "aws", "azure",
            "gcp", "cloud", "linux", "shell", "bash", "python script",
            "automation", "monitoring", "logging"
        ],
        "Documentation": [
            "docs", "documentation", "tutorial", "guide", "book", "manual",
            "readme", "wiki", "help"
        ],
        "Design": [
            "design", "ui", "ux", "figma", "sketch", "adobe xd", "design-system",
            "css", "sass", "tailwind", "styled-components", "emotion",
            "animation", "graphic design"
        ],
        "Game": [
            "game", "gamedev", "unity", "unreal", "godot", "pygame", "cocos",
            "game engine", "3d", "2d", "rpg", "strategy", "puzzle"
        ],
        "Analytics": [
            "analytics", "data analysis", "visualization", "dashboard",
            "chart", "plot", "graph", "statistics", "data"
        ],
        "Security": [
            "security", "encryption", "auth", "authentication", "oauth",
            "jwt", "ssl", "tls", "penetration testing", "hacking"
        ],
        "Automation": [
            "automation", "bot", "script", "rpa", "workflow", "automation",
            "scheduler", "cron"
        ],
        "Other": []
    }

    # 编程语言映射
    LANGUAGE_MAP = {
        "Python": ["python"],
        "JavaScript": ["javascript", "js"],
        "TypeScript": ["typescript", "ts"],
        "Go": ["go", "golang"],
        "Rust": ["rust"],
        "Java": ["java"],
        "C++": ["c++", "cpp"],
        "C": ["c"],
        "Shell": ["shell", "bash", "sh"],
        "Ruby": ["ruby"],
        "PHP": ["php"],
        "Swift": ["swift"],
        "Kotlin": ["kotlin"],
        "HTML": ["html"],
        "CSS": ["css"],
        "SQL": ["sql"],
        "Other": []
    }

    def __init__(self):
        self.categories = self.CATEGORY_MAP
        self.languages = self.LANGUAGE_MAP

    def classify_by_category(self, project: Dict) -> str:
        """
        根据项目特征分类

        Args:
            project: 项目信息

        Returns:
            分类名称
        """
        name = project.get("name", "").lower()
        description = project.get("description", "").lower()
        topics = project.get("topics", [])

        # 检查 topics
        all_keywords = " ".join(topics + [name, description])
        for category, keywords in self.categories.items():
            if category == "Other":
                continue
            for keyword in keywords:
                if keyword in all_keywords:
                    return category

        # 默认分类
        return "Other"

    def classify_by_language(self, project: Dict) -> str:
        """
        根据编程语言分类

        Args:
            project: 项目信息

        Returns:
            编程语言名称
        """
        language = project.get("language", "Other")
        language = language.strip() if language else "Other"

        # 映射到标准名称
        for std_name, keywords in self.languages.items():
            if std_name == "Other":
                continue
            for keyword in keywords:
                if keyword in language.lower():
                    return std_name

        return "Other"

    def classify_projects(self, projects: List[Dict]) -> Dict[str, List[Dict]]:
        """
        批量分类项目

        Args:
            projects: 项目列表

        Returns:
            分类后的项目字典 {分类: [项目列表]}
        """
        classified = {}

        for category in self.categories.keys():
            classified[category] = []

        # 包含手动精选项目
        all_projects = projects + MANUAL_PROJECTS

        for project in all_projects:
            category = self.classify_by_category(project)
            language = self.classify_by_language(project)

            project["category"] = category
            project["language"] = language

            if category in classified:
                classified[category].append(project)

        return classified

    def get_top_projects(self, projects: List[Dict], limit: int = 10) -> List[Dict]:
        """
        获取排名前 N 的项目（按星标数）

        Args:
            projects: 项目列表
            limit: 返回数量

        Returns:
            排名前 N 的项目
        """
        return sorted(projects, key=lambda x: x.get("stars", 0), reverse=True)[:limit]

    def get_projects_by_category(self, projects: List[Dict], category: str) -> List[Dict]:
        """
        按分类获取项目

        Args:
            projects: 项目列表
            category: 分类名称

        Returns:
            该分类下的项目列表
        """
        return [p for p in projects if p.get("category") == category]


# 创建分类器实例
classifier = ProjectClassifier()
