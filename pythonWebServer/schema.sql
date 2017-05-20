drop table if exists entries;

create table entries(
    id integer primary key autoincrement ,
    QQ integer not null,    
    'text' text not null,
    isCar integer 
);

drop table if exists QQMSG;
CREATE TABLE [QQMSG] (
[id] INTEGER  PRIMARY KEY NOT NULL,
[qq] INTEGER  NOT NULL,
[QQGROUP] INTEGER  NOT NULL,
[msg] TEXT  NOT NULL,
[isCar] BOOLEAN  NULL,
[time] TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
)