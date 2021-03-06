DROP DATABASE eat;

CREATE DATABASE IF NOT EXISTS eat DEFAULT charset=utf8;

USE eat;

CREATE TABLE `user` (
    id int(11) NOT NULL AUTO_INCREMENT,
    username varchar(30) NOT NULL,
    password varchar(20) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY (username)
);

INSERT INTO `user`(`username`, `password`) VALUES ('test', 'test');
UPDATE user SET id = 0 WHERE id = 1;
ALTER TABLE `user` AUTO_INCREMENT = 1;

CREATE TABLE `restaurant` (
    id int(11) NOT NULL,
    name varchar(30) NOT NULL,
    score int(11) NOT NULL,
    total int(11) NOT NULL,
    picture varchar(200) DEFAULT 'default.jpg',
    PRIMARY KEY (id)
);

CREATE TABLE `evaluate` (
    id int(11) NOT NULL AUTO_INCREMENT,
    user_id int(11) NOT NULL,
    restaurant_id int(11) NOT NULL,
    score int(8) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `recommend` (
    id int(11) NOT NULL AUTO_INCREMENT,
    restaurant_id int(11) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `user_recommend` (
    id int(11) NOT NULL AUTO_INCREMENT,
    user_id int(11) NOT NULL,
    recommend_id int(11) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (recommend_id) REFERENCES recommend(id) ON DELETE CASCADE ON UPDATE CASCADE
);
