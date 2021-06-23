create table user (
    id integer primary key autoincrement,
    user_name varchar(32) not null ,
    password varchar(64)
);

create table message (
    id integer primary key autoincrement,
    from_user_id int not null ,
    to_user_id int not null ,
    message text,
    status bit,
    recv_time time
);