-- MySQL 初始化脚本
-- Docker 容器首次启动时自动执行

USE bkflow;

-- 设置字符集
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- 创建初始配置（如果需要）
-- 这里可以添加一些初始数据

SELECT 'BKFlow 数据库初始化完成' AS message;
