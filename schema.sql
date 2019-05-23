CREATE TABLE usr(
u_id INTEGER PRIMARY KEY,
uid TEXT NOT NULL,
pww TEXT NOT NULL);
CREATE TABLE post(
p_id INTEGER PRIMARY KEY,
u_id INTEGER,
title TEXT,
pub_date DATE,
poot text);


INSERT INTO usr VALUES (1, 'John', 'pw11@1'), (2, 'Jane', 'pw21$$$');
INSERT INTO post VALUES (1, 1,  'Python Basics', '12/01/2018', 'This is a post that makes me exited...'), (2, 2, 'JAVA Basics', '12/05/2015', 'I love this topic and want to discuss...') ;
