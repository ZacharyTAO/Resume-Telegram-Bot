DROP SCHEMA IF EXISTS telebot;
CREATE SCHEMA telebot;
USE telebot;


DROP TABLE IF EXISTS users;
CREATE TABLE users (
    username varchar(100) not null,
    fullname varchar(100) not null,
    contact_no varchar(25),
    email varchar(100),
    primary key (username)
);

DROP TABLE IF EXISTS user_answers;
CREATE TABLE user_answers (
	username varchar(100) not null,
    question varchar(100) not null,
    answer longtext not null,
    constraint PK_user_answers primary key (username, question),
    foreign key(username) references users(username)
);

DROP TABLE IF EXISTS user_links;
CREATE TABLE user_links(
    username varchar(100) not null,
    link varchar(100) not null,
    link_description longtext not null,
    constraint PK_user_links primary key (username, link_description), 
    foreign key(username) references users(username)
);


