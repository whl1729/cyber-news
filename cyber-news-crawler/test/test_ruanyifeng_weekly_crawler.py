from crawler.blog import ruanyifeng_weekly_crawler
from crawler.util import fs


def test_ruanyifeng_blog_parser():
    parser = ruanyifeng_weekly_crawler.RuanyifengBlogParser()
    html_path = fs.log_dir / "ruanyifeng_blog_0.html"
    with open(html_path, encoding="utf-8") as f:
        content = f.read()
    title, url = parser.parse(content)
    assert title == "科技爱好者周刊（第 315 期）：一份谷歌离职报告"
    assert url == "https://www.ruanyifeng.com/blog/2024/08/weekly-issue-315.html"


def test_find_latest_blog():
    title, url = ruanyifeng_weekly_crawler.find_latest_blog()
    assert "科技爱好者周刊" in title
    assert "weekly-issue-" in url


def test_ruanyifeng_weekly_parser():
    title = "科技爱好者周刊（第 315 期）：一份谷歌离职报告"
    url = "https://www.ruanyifeng.com/blog/2024/08/weekly-issue-315.html"
    parser = ruanyifeng_weekly_crawler.RuanyifengWeeklyParser(title, url)
    html_path = fs.log_dir / "ruanyifeng_weekly_0.html"
    with open(html_path, encoding="utf-8") as f:
        content = f.read()
    [result] = parser.parse(content)

    expected_sections = {
        "热点": [
            "一份谷歌离职报告",
            "微软工程师的薪资",
            "[活动通知] 动手练习 AI 编程",
        ],
        "科技动态": [
            "1. 载人飞艇",
            "2. 新形状意大利面",
            "3. 折叠屏笔记本",
            "4. 其他",
        ],
        "文章": [
            "1. SAML 身份验证的可视化解释（英文）",
            "2. 现代 CSS 方式设置 table 样式（英文）",
            "3. 如何制作 SVG 加载器（英文）",
            "4. 小写可以减少压缩文件体积（英文）",
            "5. .git 子目录内部（英文）",
            "6. 方形复选框的记忆（英文）",
        ],
        "工具": [
            "1. Coolify",
            "2. Ente Auth",
            "3. Marsview",
            "4. Notion Exporter",
            "5. 电池的电量显示",
            "6. tsimp",
            "7. xpano",
            "8. concrete.css",
            "9. Person Diagram",
        ],
        "AI 相关": [
            "1. 现代文转古文大模型",
            "2. Linly-Dubbing",
            "3. kotaemon",
            "4. Watson AI",
            "5. Fluximg.com",
        ],
        "资源": [
            "1. 妖怪平生录",
            "2. Emoji Spark",
            "3. 使用 Julia 语言学习微积分（Calculus With Julia）（英文）",
            "4. Documentaries",
        ],
        "图片": ["1. 还原致命的原子弹实验事故"],
        "文摘": ["1. 73亿人，一栋小楼"],
    }

    for name, content in result["sections"].items():
        assert content == expected_sections[name]


if __name__ == "__main__":
    test_ruanyifeng_weekly_parser()
