import time
import traceback
from abc import ABC
from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import Optional

from news.util.logger import logger
from news.util.mongodb import mongo


class FailureReason(Enum):
    """爬虫失败原因分类"""

    NETWORK_ERROR = "网络错误"
    PARSE_ERROR = "解析错误"
    API_RATE_LIMIT = "API 限流"
    ANTI_CRAWLER = "反爬虫"
    OTHER = "其他"


class RetryStrategy:
    """重试策略配置"""

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 5.0,
        use_exponential_backoff: bool = True,
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.use_exponential_backoff = use_exponential_backoff

    def get_delay(self, attempt: int) -> float:
        """获取重试延迟时间"""
        if self.use_exponential_backoff:
            return self.base_delay * (2 ** (attempt - 1))
        return self.base_delay


class BaseCrawlerWithRetry(ABC):
    """带重试和健康检查的爬虫基类"""

    def __init__(self, name: str, retry_strategy: Optional[RetryStrategy] = None):
        self.name = name
        self.retry_strategy = retry_strategy or RetryStrategy()

    @abstractmethod
    def _do_crawl(self) -> bool:
        """子类实现具体的爬取逻辑，返回是否成功"""

    def crawl(self) -> bool:
        """执行爬取，带重试和健康检查"""
        start_time = datetime.now()
        attempt = 0
        last_error = None
        failure_reason = None

        while attempt < self.retry_strategy.max_retries:
            attempt += 1
            try:
                logger.info(
                    f"[{self.name}] 开始爬取 (尝试 {attempt}/{self.retry_strategy.max_retries})"
                )
                success = self._do_crawl()

                if success:
                    elapsed = (datetime.now() - start_time).total_seconds()
                    self._record_health(True, None, None, elapsed, attempt)
                    logger.info(
                        f"[{self.name}] 爬取成功 (耗时 {elapsed:.2f}s, 重试 {attempt-1} 次)"
                    )
                    return True

            except Exception as e:
                last_error = e
                failure_reason = self._classify_error(e)
                logger.warning(f"[{self.name}] 爬取失败 (尝试 {attempt}): {e}")

                # 解析错误不重试
                if failure_reason == FailureReason.PARSE_ERROR:
                    logger.error(f"[{self.name}] 解析错误，不重试")
                    break

                # 如果还有重试机会，等待后重试
                if attempt < self.retry_strategy.max_retries:
                    delay = self._get_retry_delay(attempt, failure_reason)
                    logger.info(f"[{self.name}] 等待 {delay}s 后重试...")
                    time.sleep(delay)

        # 所有重试都失败
        elapsed = (datetime.now() - start_time).total_seconds()
        error_trace = traceback.format_exc() if last_error else None
        self._record_health(False, failure_reason, error_trace, elapsed, attempt)
        logger.error(f"[{self.name}] 爬取最终失败 (耗时 {elapsed:.2f}s, 重试 {attempt} 次)")
        return False

    def _classify_error(self, error: Exception) -> FailureReason:
        """分类错误原因"""
        error_str = str(error).lower()
        error_type = type(error).__name__.lower()

        # 网络错误
        if any(
            keyword in error_str or keyword in error_type
            for keyword in [
                "timeout",
                "connection",
                "network",
                "unreachable",
                "refused",
            ]
        ):
            return FailureReason.NETWORK_ERROR

        # API 限流
        if "429" in error_str or "rate limit" in error_str:
            return FailureReason.API_RATE_LIMIT

        # 解析错误
        if any(
            keyword in error_str or keyword in error_type
            for keyword in [
                "parse",
                "json",
                "xml",
                "html",
                "decode",
                "keyerror",
                "indexerror",
            ]
        ):
            return FailureReason.PARSE_ERROR

        # 反爬虫
        if any(
            keyword in error_str
            for keyword in ["403", "forbidden", "captcha", "blocked", "bot"]
        ):
            return FailureReason.ANTI_CRAWLER

        return FailureReason.OTHER

    def _get_retry_delay(self, attempt: int, failure_reason: FailureReason) -> float:
        """获取重试延迟，根据失败原因调整"""
        # API 限流使用更长的延迟
        if failure_reason == FailureReason.API_RATE_LIMIT:
            return 60 * attempt  # 60s, 120s, 180s

        # 其他错误使用配置的策略
        return self.retry_strategy.get_delay(attempt)

    def _record_health(
        self,
        success: bool,
        failure_reason: Optional[FailureReason],
        error_trace: Optional[str],
        elapsed: float,
        attempts: int,
    ):
        """记录健康状态到 MongoDB"""
        health_record = {
            "crawler_name": self.name,
            "success": success,
            "timestamp": datetime.now(),
            "elapsed_seconds": elapsed,
            "attempts": attempts,
        }

        if not success:
            health_record["failure_reason"] = (
                failure_reason.value if failure_reason else "未知"
            )
            health_record["error_trace"] = error_trace

        try:
            mongo.insert_one("crawler_health", health_record)
        except Exception as e:
            logger.error(f"[{self.name}] 记录健康状态失败: {e}")
