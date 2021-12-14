DROP TABLE IF EXISTS users;
CREATE TABLE users (
    username varchar(100) not null,
    fullname varchar(100) not null,
    contact_no varchar(25),
    email varchar(100),
    primary key (username),
    foreign key (username) references user_answers(username),
    foreign key(username) references user_links(username)
);

DROP TABLE IF EXISTS user_answers;
CREATE TABLE user_answers (
	username varchar(100) not null,
    question varchar(100) not null,
    answer varchar(255) not null,
    constraint PK_user_answers primary key (username, question)
);

DROP TABLE IF EXISTS user_links;
CREATE TABLE user_links(
    username varchar(100) not null,
    link varchar(100) not null,
    link_description varchar(25) not null,
    constraint PK_user_links primary key (username, link_description)
)


