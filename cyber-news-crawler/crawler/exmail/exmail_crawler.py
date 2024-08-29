import email
import imaplib
from email.header import decode_header

from bs4 import BeautifulSoup
from crawler.util.configer import config
from crawler.util.logger import logger


class ExmailCrawler:
    def __init__(self):
        self._mail = self.login()

    def login(self):
        logger.info(
            f'exmail server: {config["exmail_server"]}, user: {config["exmail_user"]}, {config["exmail_password"]}'
        )
        # 登录到邮箱
        mail = imaplib.IMAP4_SSL(config["exmail_server"])
        mail.login(config["exmail_user"], config["exmail_password"])
        logger.info("exmail logined")
        return mail

    def get_latest_mails(self, num: int):
        # 选择邮箱文件夹，默认为收件箱
        self._mail.select("inbox")

        # 搜索邮件，返回邮件编号列表
        status, messages = self._mail.search(None, "ALL")
        logger.info(f"status of searching all exmails: {status}")

        # 将邮件编号字符串转换为列表
        mail_ids = messages[0].split()

        # 遍历邮件编号，读取最新的几封邮件
        for i in mail_ids[-num:]:
            status, msg_data = self._mail.fetch(i, "(RFC822)")

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    # 获取邮件的各个部分
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    from_ = msg.get("From")
                    date_ = msg.get("Date")

                    logger.info(f"Subject: {subject}")
                    logger.info(f"From: {from_}")
                    logger.info(f"Date: {date_}")

                    # 遍历邮件的各个部分
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            try:
                                body = part.get_payload(decode=True).decode()
                            except Exception as e:
                                logger.warn(f"failed to get payload: {e}")
                                continue

                            if (
                                content_type == "text/plain"
                                and "attachment" not in content_disposition
                            ):
                                logger.info(f"Body: {body}")
                            elif (
                                content_type == "text/html"
                                and "attachment" not in content_disposition
                            ):
                                soup = BeautifulSoup(body, "html.parser")
                                logger.info(f"HTML Body: {soup.get_text()}")
                    else:
                        content_type = msg.get_content_type()
                        body = msg.get_payload(decode=True).decode()
                        if content_type == "text/plain":
                            logger.info(f"Body: {body}")
                        elif content_type == "text/html":
                            soup = BeautifulSoup(body, "html.parser")
                            logger.info(f"HTML Body: {soup.get_text()}")

                    logger.info("=" * 100)

    def logout(self):
        if self._mail is not None:
            self._mail.logout()


if __name__ == "__main__":
    exmail_crawler = ExmailCrawler()
    exmail_crawler.get_latest_mails(10)
