from dataclasses import dataclass


@dataclass
class GithubUserEvent:
    """Github 用户事件"""

    # 事件标识
    id: str
    # 事件类型，比如：ForkEvent、MemberEvent、PublicEvent、WatchEvent
    type: str
    # 行动者的名字
    actor_name: str
    # 行动者的 URL 地址
    actor_url: str
    # 仓库名字
    repo_name: str
    # 仓库的 URL 地址
    repo_url: str
    # 创建时间
    created_at: str

    def to_json(self):
        return {
            "id": self.id,
            "type": self.type,
            "actor_name": self.actor_name,
            "actor_url": self.actor_url,
            "repo_name": self.repo_name,
            "repo_url": self.repo_url,
            "created_at": self.created_at,
        }
