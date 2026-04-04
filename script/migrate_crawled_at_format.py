"""
一次性迁移脚本：将 MongoDB 中所有 collection 的 crawled_at 字段
从旧格式 "YYYYMMDDHHmmSS"（如 "20260404103000"）
转换为新格式 "%Y-%m-%d %H:%M:%S"（如 "2026-04-04 10:30:00"）

用法：
  python script/migrate_crawled_at_format.py --dry-run   # 预览
  python script/migrate_crawled_at_format.py             # 执行
"""

import os
import sys

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


def get_db():
    host = os.getenv("MONGODB_HOST", "127.0.0.1")
    port = os.getenv("MONGODB_PORT", 27017)
    database = os.getenv("MONGODB_DATABASE", "newsDB")
    client = MongoClient(f"mongodb://{host}:{port}/")
    return client[database]


def convert_format(old_value: str) -> str:
    """20260404103000 -> 2026-04-04 10:30:00"""
    return (
        f"{old_value[:4]}-{old_value[4:6]}-{old_value[6:8]} "
        f"{old_value[8:10]}:{old_value[10:12]}:{old_value[12:14]}"
    )


REGEX_FILTER = {"crawled_at": {"$regex": r"^\d{14}$"}}


def dry_run(db):
    for coll_name in sorted(db.list_collection_names()):
        coll = db[coll_name]
        count = coll.count_documents(REGEX_FILTER)
        if count > 0:
            sample = coll.find_one(REGEX_FILTER)
            print(
                f"  {coll_name}: {count} records"
                f" (e.g. {sample['crawled_at']} -> {convert_format(sample['crawled_at'])})"
            )
    print("\nDry run complete. Run without --dry-run to apply changes.")


def migrate(db):
    total_updated = 0
    for coll_name in sorted(db.list_collection_names()):
        coll = db[coll_name]
        count = 0
        for doc in coll.find(REGEX_FILTER):
            new_value = convert_format(doc["crawled_at"])
            coll.update_one(
                {"_id": doc["_id"]},
                {"$set": {"crawled_at": new_value}},
            )
            count += 1
        if count > 0:
            print(f"  {coll_name}: {count} records updated")
            total_updated += count
    print(f"\nTotal: {total_updated} records updated")


if __name__ == "__main__":
    print("Migrating crawled_at format: YYYYMMDDHHmmSS -> YYYY-MM-DD HH:MM:SS\n")
    db = get_db()

    if "--dry-run" in sys.argv:
        dry_run(db)
    else:
        migrate(db)
