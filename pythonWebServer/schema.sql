drop table if exists entries;

create table entries(
    id integer primary key autoincrement ,
    QQ integer not null,    
    'text' text not null,
    isCar integer ,
);