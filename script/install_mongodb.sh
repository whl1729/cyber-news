#!/bin/bash
# MongoDB 安装脚本 - Ubuntu 20.04

set -e

echo "=== 开始安装 MongoDB 5.0 ==="

# 1. 导入 MongoDB GPG 密钥
echo "1. 导入 MongoDB GPG 密钥..."
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -

# 2. 添加 MongoDB 源
echo "2. 添加 MongoDB 源..."
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list

# 3. 更新包列表
echo "3. 更新包列表..."
sudo apt-get update

# 4. 安装 MongoDB
echo "4. 安装 MongoDB..."
sudo apt-get install -y mongodb-org

# 5. 启动 MongoDB
echo "5. 启动 MongoDB..."
sudo systemctl start mongod
sudo systemctl enable mongod

# 6. 验证安装
echo "6. 验证安装..."
sleep 2
sudo systemctl status mongod --no-pager

echo ""
echo "=== MongoDB 安装完成 ==="
echo "MongoDB 正在运行在 127.0.0.1:27017"
