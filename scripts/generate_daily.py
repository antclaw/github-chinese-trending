"""
生成每日排行榜文档
创建按天的 markdown 文件
"""

import os
import sys
from datetime import datetime
from utils.classifier import classifier


def generate_markdown(classified: dict, date_str: str) -> str:
    """
    生成 markdown 文档

    Args:
        classified: 分类结果
        date_str: 日期字符串

    Returns:
        Markdown 内容
    """
    lines = []

    # 标题
    lines.append("# GitHub 中文热门项目排行榜")
    lines.append(f"\n> 📅 更新时间: {date_str}")
    lines.append(f"> ⏰ 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    # 项目总数
    total = sum(len(p) for p in classified.values())
    lines.append(f"📊 **总项目数**: {total}")
    lines.append("")

    # 分类列表
    lines.append("## 📁 按分类浏览")
    lines.append("")

    for category, projects in sorted(classified.items(), key=lambda x: len(x[1]), reverse=True):
        if not projects:
            continue

        lines.append(f"### {category} ({len(projects)})")
        lines.append("")

        for project in projects[:20]:  # 每个分类最多显示 20 个
            name = project.get("name", "Unknown")
            description = project.get("description", "无描述")
            url = project.get("url", "")
            stars = project.get("stars", 0)
            language = project.get("language", "Unknown")

            lines.append(f"- [{name}]({url})")
            lines.append(f"  - 🌟 {stars} stars | 💻 {language}")
            lines.append(f"  - {description}")
            lines.append("")

    # 顶级项目（按星标数）
    lines.append("## 🏆 顶级项目 (Top 10)")
    lines.append("")

    top_projects = []
    for project_list in classified.values():
        top_projects.extend(project_list)

    top_projects = sorted(top_projects, key=lambda x: x.get("stars", 0), reverse=True)[:10]

    for idx, project in enumerate(top_projects, 1):
        name = project.get("name", "Unknown")
        url = project.get("url", "")
        stars = project.get("stars", 0)
        forks = project.get("forks", 0)
        description = project.get("description", "")
        language = project.get("language", "Unknown")
        category = project.get("category", "Other")

        lines.append(f"{idx}. [{name}]({url})")
        lines.append(f"   - 🌟 {stars} stars | 🍴 {forks} forks | 💻 {language} | 📂 {category}")
        if description:
            lines.append(f"   - {description}")
        lines.append("")

    return "\n".join(lines)


def save_markdown(content: str, date_str: str) -> str:
    """
    保存 markdown 文件

    Args:
        content: Markdown 内容
        date_str: 日期字符串

    Returns:
        文件路径
    """
    data_dir = os.path.join("data", date_str)
    os.makedirs(data_dir, exist_ok=True)

    md_path = os.path.join(data_dir, f"{date_str}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Saved markdown to: {md_path}")
    return md_path


def main():
    """主函数"""
    print("=" * 60)
    print("生成每日排行榜文档")
    print("=" * 60)

    # 获取当前日期
    today = datetime.now().strftime("%Y-%m-%d")

    # 读取分类数据
    json_path = os.path.join("data", today, "classified.json")
    if not os.path.exists(json_path):
        print(f"\n❌ Error: {json_path} not found")
        print("Please run classify.py first")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        import json
        classified = json.load(f)

    print(f"\nLoaded classification from {json_path}")

    # 生成 markdown
    print("\nGenerating markdown...")
    content = generate_markdown(classified, today)

    # 保存 markdown
    md_path = save_markdown(content, today)

    print("\n" + "=" * 60)
    print("✅ Markdown generation completed!")
    print(f"📁 Output: {md_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
