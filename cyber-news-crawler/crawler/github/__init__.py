url_prefix = "https://github.com"
login_url = "https://github.com/login"
# 在开发者工具中看到 Github 主页的 Home 部分请求了 `/conduit/for_you_feed`，但我使用时会报 404 的错误
# feed_url = 'https://github.com/conduit/for_you_feed'
# 后来在 https://github.com/orgs/community/discussions/64982 看到可以使用 `/dashboard-feed`
feed_url = "https://github.com/dashboard-feed"
session_url = "https://github.com/session"

headers = {
    "Referer": "https://github.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Host": "github.com",
}
