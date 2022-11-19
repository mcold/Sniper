drop table snip;
drop table category;
drop table task;

create table if not exists task
(id 	  integer primary key autoincrement,
num       integer,
name      text,
descript  text);

create table if not exists category
(id 	  integer primary key autoincrement,
id_task   integer references task(id) on delete cascade,
name      text,
tag       text,
descript  text);

create table if not exists snip
(id 	  integer primary key autoincrement,
id_cat    integer references category(id) on delete cascade,
name      text,
install	  integer default 0,
seq_order integer,
code      blob,
roll_back blob,
descript  text);