"""
GitHub 爬虫工具
支持从 GitHub Trending API 获取数据，以及手动添加项目
"""

import requests
from typing import List, Dict, Optional
from datetime import datetime
import re


class GitHubScraper:
    """GitHub 数据抓取器"""

    def __init__(self, github_token: Optional[str] = None):
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "github-chinese-trending"
        }
        if github_token:
            self.headers["Authorization"] = f"token {github_token}"

    def fetch_trending(self, language: str = "python", since: str = "daily") -> List[Dict]:
        """
        获取 GitHub Trending 数据

        Args:
            language: 编程语言
            since: 时间范围 (daily, weekly, monthly)

        Returns:
            项目列表
        """
        url = f"https://api.github.com/search/repositories?q=language:{language}+is:public"
        params = {
            "sort": "stars",
            "order": "desc",
            "per_page": 100
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            projects = []
            for item in data.get("items", [])[:50]:  # 限制 50 个项目
                projects.append({
                    "name": item["name"],
                    "description": item["description"] or "无描述",
                    "url": item["html_url"],
                    "language": item["language"],
                    "stars": item["stargazers_count"],
                    "forks": item["forks_count"],
                    "updated_at": item["updated_at"],
                    "created_at": item["created_at"],
                    "topics": item.get("topics", []),
                    "is_chinese": self._is_chinese_project(item)
                })

            return projects

        except Exception as e:
            print(f"Error fetching trending: {e}")
            return []

    def _is_chinese_project(self, repo: Dict) -> bool:
        """判断项目是否为中文项目"""
        # 检查 README 是否包含中文
        try:
            url = f"https://api.github.com/repos/{repo['full_name']}/readme"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                readme_data = response.json()
                readme_content = readme_data.get("content", "")
                import base64
                import textwrap
                decoded = base64.b64decode(readme_content).decode('utf-8', errors='ignore')
                # 检查是否有中文字符
                if re.search(r'[\u4e00-\u9fff]', decoded):
                    return True
        except:
            pass

        # 检查描述是否为中文
        description = repo.get("description", "")
        if re.search(r'[\u4e00-\u9fff]', description):
            return True

        return False

    def manual_add_project(self, project: Dict) -> List[Dict]:
        """
        手动添加项目

        Args:
            project: 项目信息字典

        Returns:
            更新后的项目列表
        """
        projects = self.fetch_trending()
        projects.append(project)
        return projects

    def search_projects(self, query: str, limit: int = 20) -> List[Dict]:
        """
        搜索 GitHub 项目

        Args:
            query: 搜索关键词
            limit: 返回数量

        Returns:
            项目列表
        """
        url = "https://api.github.com/search/repositories"
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": limit
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            projects = []
            for item in data.get("items", []):
                projects.append({
                    "name": item["name"],
                    "description": item["description"] or "无描述",
                    "url": item["html_url"],
                    "language": item["language"],
                    "stars": item["stargazers_count"],
                    "forks": item["forks_count"],
                    "updated_at": item["updated_at"],
                    "created_at": item["created_at"],
                    "topics": item.get("topics", []),
                    "is_chinese": self._is_chinese_project(item)
                })

            return projects

        except Exception as e:
            print(f"Error searching projects: {e}")
            return []


# 预定义的优质项目（手动精选）
MANUAL_PROJECTS = [
    {
        "name": "FastAPI",
        "description": "现代、快速（高性能）的 Web 框架，用于构建 API",
        "url": "https://github.com/tiangolo/fastapi",
        "language": "Python",
        "category": "Web",
        "stars": 70000,
        "forks": 5000,
        "updated_at": datetime.now().isoformat(),
        "created_at": "2018-11-01T00:00:00Z",
        "topics": ["api", "async", "python", "framework", "rest"],
        "is_chinese": False
    },
    {
        "name": "LangChain",
        "description": "用于构建由 LLM 驱动的应用程序的框架",
        "url": "https://github.com/langchain-ai/langchain",
        "language": "Python",
        "category": "AI/ML",
        "stars": 85000,
        "forks": 12000,
        "updated_at": datetime.now().isoformat(),
        "created_at": "2022-10-27T00:00:00Z",
        "topics": ["llm", "ai", "langchain", "chatgpt", "openai"],
        "is_chinese": False
    },
    {
        "name": "Vercel",
        "description": "前端开发者的部署平台",
        "url": "https://github.com/vercel/next.js",
        "language": "TypeScript",
        "category": "Web",
        "stars": 120000,
        "forks": 25000,
        "updated_at": datetime.now().isoformat(),
        "created_at": "2016-01-01T00:00:00Z",
        "topics": ["react", "next", "ssr", "javascript"],
        "is_chinese": False
    }
]
