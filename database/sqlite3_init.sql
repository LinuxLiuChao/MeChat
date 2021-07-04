create table user (
    id integer primary key autoincrement,
    user_name varchar(32) not null ,
    password varchar(64)
);

create table message (
    id integer primary key autoincrement,
    from_user_name varchar(32) not null ,
    to_user_name varchar(32) not null ,
    message text,
    status bit,
    recv_time time,
    send_time datetime
);