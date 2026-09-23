-- BKFlow 数据库初始化 SQL
-- 在 MySQL 中执行以下命令

-- 创建数据库
CREATE DATABASE IF NOT EXISTS bkflow DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户
CREATE USER IF NOT EXISTS 'bkflow'@'localhost' IDENTIFIED BY 'bkflow123';

-- 授权
GRANT ALL PRIVILEGES ON bkflow.* TO 'bkflow'@'localhost';

-- 刷新权限
FLUSH PRIVILEGES;

-- 查看数据库
SHOW DATABASES LIKE 'bkflow';

-- 查看用户
SELECT User, Host FROM mysql.user WHERE User = 'bkflow';

SELECT '✓ BKFlow 数据库和用户创建完成' AS status;
