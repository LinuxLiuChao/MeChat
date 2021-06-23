/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2021/6/24 0:19:48                            */
/*==============================================================*/


drop table if exists message;

drop table if exists user;

/*==============================================================*/
/* Table: message                                               */
/*==============================================================*/
create table message
(
   id                   integer not null,
   from_user_id         integer,
   to_user_id           integer,
   message              text,
   status               bit,
   recve_time           timestamp default current_timestamp,
   send_time            datetime default null,
   primary key (id)
);

/*==============================================================*/
/* Table: user                                                  */
/*==============================================================*/
create table user
(
   id                   integer not null,
   user_nmae            varchar(32),
   password             varchar(64),
   primary key (id)
);

alter table user comment 'user info';

