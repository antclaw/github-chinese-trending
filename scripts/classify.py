"""
项目分类脚本
对抓取的项目进行分类
"""

import os
import sys
from datetime import datetime
from utils.classifier import classifier


def classify_projects(projects: list) -> dict:
    """
    分类项目

    Args:
        projects: 项目列表

    Returns:
        分类结果字典
    """
    print("\n" + "=" * 60)
    print("项目分类")
    print("=" * 60)

    # 分类项目
    classified = classifier.classify_projects(projects)

    # 保存分类结果
    json_path = "data/classified.json"
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump(classified, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Classification saved to: {json_path}")

    # 打印分类统计
    print("\n" + "-" * 60)
    print("分类统计:")
    print("-" * 60)

    for category, project_list in sorted(classified.items(), key=lambda x: len(x[1]), reverse=True):
        if project_list:
            print(f"{category}: {len(project_list)} 项目")

    return classified


def generate_stats(classified: dict) -> str:
    """
    生成统计信息

    Args:
        classified: 分类结果

    Returns:
        统计信息字符串
    """
    stats = []

    # 总项目数
    total = sum(len(p) for p in classified.values())
    stats.append(f"总项目数: {total}")

    # 按分类统计
    stats.append("\n按分类统计:")
    for category, project_list in sorted(classified.items(), key=lambda x: len(x[1]), reverse=True):
        if project_list:
            stats.append(f"  {category}: {len(project_list)}")

    # 按语言统计
    stats.append("\n按编程语言统计:")
    language_count = {}
    for project_list in classified.values():
        for project in project_list:
            lang = project.get("language", "Unknown")
            language_count[lang] = language_count.get(lang, 0) + 1

    for lang, count in sorted(language_count.items(), key=lambda x: x[1], reverse=True):
        stats.append(f"  {lang}: {count}")

    return "\n".join(stats)


def main():
    """主函数"""
    print("=" * 60)
    print("项目分类")
    print("=" * 60)

    # 获取当前日期
    today = datetime.now().strftime("%Y-%m-%d")

    # 读取项目数据
    json_path = f"data/{today}/projects.json"
    if not os.path.exists(json_path):
        print(f"\n❌ Error: {json_path} not found")
        print("Please run fetch_data.py first")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        import json
        projects = json.load(f)

    print(f"\nLoaded {len(projects)} projects from {json_path}")

    # 分类项目
    classified = classify_projects(projects)

    # 生成并保存统计信息
    stats = generate_stats(classified)
    stats_path = "data/stats.txt"
    with open(stats_path, "w", encoding="utf-8") as f:
        f.write(stats)

    print("\n" + "-" * 60)
    print("统计信息:")
    print("-" * 60)
    print(stats)

    print("\n✅ Classification completed!")


if __name__ == "__main__":
    main()
