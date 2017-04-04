use ebookdata
go
if exists(select name from sys.tables where name='Student_test')
drop table Student_test
go
create table Student_test
(sname nchar(10) primary key,
 sex nchar(2) not null,
)