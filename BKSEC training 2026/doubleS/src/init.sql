CREATE DATABASE IF NOT EXISTS ${MYSQL_DB};
USE ${MYSQL_DB};

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS flags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flag VARCHAR(255) NOT NULL
);

INSERT INTO users (username, password) VALUES ('admin', 'this_is_a_super_super_vjp_pro_secure_password');

