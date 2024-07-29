from lxml import etree
import requests
import socks
import socket

from crawler.util.configer import config
from crawler.util.logger import logger
from crawler.util import fs

class GithubLogin(object):
    def __init__(self):
        socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 7078)
        socket.socket = socks.socksocket
        self._email=config["github_username"]
        self._password=config['github_password']
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'github.com'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/settings/profile'
        self.session = requests.Session()
    
    def token(self):
        response = self.session.get(self.login_url, headers=self.headers)
        selector = etree.HTML(response.text)
        # 崔庆才的源代码中获取 token 的 xpath 已不适用，此处做了修改
        token = selector.xpath('//*[@id="login"]/div[4]/form/input[1]/@value')
        return token
    
    def login(self):
        self.dynamics()

        response = self.session.get(self.logined_url, headers=self.headers)
        if response.status_code == 200:
            self.profile(response.text)
        else:
            logger.error(f'failed to get profile: {response}')

        response = requests.get("https://api.github.com/notifications", headers=headers)
        notifications = response.json()

        for notification in notifications:
            print(notification)
            
    def dynamics(self):
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token()[0],
            'login': self._email,
            'password': self._password
        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            logger.error(f'failed to post session: {response}')
            return
        
        html = response.text
        self.save(html, "dynamics.html")
        selector = etree.HTML(html)
        dynamics = selector.xpath('//div[contains(@class, "news")]//div[contains(@class, "alert")]')
        for item in dynamics:
            dynamic = ' '.join(item.xpath('.//div[@class="title"]//text()')).strip()
            logger.info(f'dynamic: {dynamic}')
    
    def profile(self, html):
        selector = etree.HTML(html)
        name = selector.xpath('//input[@id="user_profile_name"]/@value')[0]
        email = selector.xpath('//select[@id="user_profile_email"]/option[@value!=""]/text()')[0]
        logger.info(f'name: {name}, email: {email}')
    
    def save(self, html: str, dest_path: str):
        with open(fs.log_dir / dest_path, "w", encoding="utf-8") as f:
            f.write(html)


if __name__ == "__main__":
    github = GithubLogin()
    github.login()
