CREATE DATABASE IF NOT EXISTS eat;

USE eat;

CREATE TABLE `user` (
	id int(11) NOT NULL AUTO_INCREMENT,
	username varchar(30) DEFAULT NULL,
	password varchar(20) DEFAULT NULL,
	PRIMARY KEY (id)
);
