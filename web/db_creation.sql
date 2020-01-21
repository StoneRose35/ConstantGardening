-- install mysql with root/horbermatt
CREATE DATABASE gardening;
CREATE USER 'mira'@'localhost' IDENTIFIED BY 'amelie';
GRANT ALL PRIVILEGES ON gardening.* TO 'mira'@'localhost';
FLUSH PRIVILEGES;
CREATE TABLE humidity (id INT(6) AUTO_INCREMENT PRIMARY KEY,value INTEGER,timestamp DATETIME);
