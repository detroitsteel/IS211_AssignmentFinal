--drop table usr;
CREATE TABLE usr(
u_id INTEGER PRIMARY KEY,
uid TEXT NOT NULL,
pww TEXT NOT NULL);

CREATE TABLE post(
p_id INTEGER PRIMARY KEY,
title TEXT,
pub_date DATE,
poot text);

CREATE TABLE usrPost(
id INTEGER PRIMARY KEY,
u_id INTEGER,
p_id INTEGER);

INSERT INTO usr VALUES (1, 'John', 'pw11@1'), (2, 'Jane', 'pw21$$$');
INSERT INTO post VALUES (1, 'Python Basics', '12/05/2018', 'This is a post that makes me exited...'), (2, 'JAVA Basics', '12/05/2015', 'I love this topic and want to discuss...') ;
INSERT INTO usrPost VALUES (1, 1, 1), (2, 2, 2);

select u.u_id, p.p_id, p.title, p.pub_date, p.poot
from usrPost up 
left join usr u 
	on u.u_id = up.u_id
left join post p 
	on p.p_id = up.p_id
order by p.pub_date desc;

