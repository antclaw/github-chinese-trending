"""
数据抓取脚本
从 GitHub Trending API 和手动精选获取项目数据
"""

import os
import sys
from datetime import datetime
from utils.scraper import GitHubScraper, MANUAL_PROJECTS


def fetch_all_projects() -> list:
    """
    获取所有项目数据

    Returns:
        项目列表
    """
    scraper = GitHubScraper()

    # 从不同编程语言获取项目
    languages = ["python", "javascript", "go", "rust", "java", "typescript"]
    all_projects = []

    for lang in languages:
        print(f"Fetching {lang} projects...")
        projects = scraper.fetch_trending(language=lang)
        all_projects.extend(projects)

    # 添加手动精选项目
    print("Adding manually curated projects...")
    all_projects.extend(MANUAL_PROJECTS)

    # 去重
    unique_projects = []
    seen_urls = set()

    for project in all_projects:
        url = project.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_projects.append(project)

    # 按星标数排序
    unique_projects.sort(key=lambda x: x.get("stars", 0), reverse=True)

    return unique_projects


def save_projects(projects: list) -> str:
    """
    保存项目数据到 JSON 文件

    Args:
        projects: 项目列表

    Returns:
        JSON 文件路径
    """
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

    json_path = os.path.join(data_dir, "projects.json")
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump(projects, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(projects)} projects to {json_path}")
    return json_path


def main():
    """主函数"""
    print("=" * 60)
    print("GitHub 中文热门项目数据抓取")
    print("=" * 60)

    # 获取当前日期
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\nDate: {today}")

    # 获取项目数据
    projects = fetch_all_projects()
    print(f"\nTotal projects fetched: {len(projects)}")

    # 保存数据
    json_path = save_projects(projects)

    print("\n✅ Data fetching completed!")
    print(f"📁 Saved to: {json_path}")

    return projects


if __name__ == "__main__":
    main()
