DROP TABLE IF EXISTS users;
CREATE TABLE users (
	chat_id varchar(15) not null,
    username varchar(255) not null,
    user_id varchar(15) not null,
    primary key (chat_id),
    foreign key (user_id) references employees(user_id)
);

DROP TABLE IF EXISTS employees;
CREATE TABLE employees (
	user_id varchar(15) not null,
    fullname varchar(255) not null,
    primary key (user_id)
);

DROP TABLE IF EXISTS employee_answers;
CREATE TABLE employee_answers (
	user_id varchar(15) not null,
    question varchar(100) not null,
    answer varchar(255) not null,
    constraint PK_employee_answers primary key (user_id, question)
);



