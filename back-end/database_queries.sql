select * 
from chat_app_structure_test.public.users u;

alter table chat_app_structure_test.public.users
add column password varchar(25) not null;


update chat_app_structure_test.public.users 
set confirmed = true 
where user_id = 3;


insert into chat_app_structure_test.public.users (username, email, password)
select 'Kostiantyn', 'koskosko0@gmal.com', 'password';

insert into chat_app_structure_test.public.users (username, email, password)
values 
	('User2', 'user2@gmal.com', 'user2password'),
	('User3', 'user3@gmal.com', 'user3password'),
	('User4', 'user4@gmal.com', 'user4password'),
	('User5', 'user5@gmal.com', 'user5password'),
	('User6', 'user6@gmal.com', 'user6password')
;


-- PROFILES
select * 
from chat_app_structure_test.public.profile p;

insert into chat_app_structure_test.public.profile (user_id, phone_number, biography, img_url)
select 3, '+(44) 074 241 570 42', 'I love big black cock', 'img url';

select 
	u.username,
	u.email,
	p.phone_number,
	p.biography,
	u.created_at,
	p.img_url
from chat_app_structure_test.public.profile p
join chat_app_structure_test.public.users u 
	on p.user_id = u.user_id;


-- POSTS
select * 
from chat_app_structure_test.public.posts p;

insert into chat_app_structure_test.public.posts (user_id, description, img_url)
select 3, 'I love big black cock', 'big black cock img';

select 
	u.username,
	u.email,
	p.description,
	p."date",
	p.img_url
from chat_app_structure_test.public.posts p 
join chat_app_structure_test.public.users u 
	on p.user_id = u.user_id;

-- CONTACTS	
select * 
from chat_app_structure_test.public.contacts c;

insert into chat_app_structure_test.public.contacts (user_id_1, user_id_2)
values 
	(3, 4),
	(5, 6),
	(7, 8)
;

select 
	(select u.username from chat_app_structure_test.public.users u where u.user_id = c.user_id_1) as username1,
	(select u.username from chat_app_structure_test.public.users u where u.user_id = c.user_id_2) as username2,
	c.date_created 
from chat_app_structure_test.public.contacts c;


select * 
from chat_app_structure_test.public.chats c;

insert into chat_app_structure_test.public.chats (user_1, user_2)
values 
	(3, 4),
	(5, 6),
	(7, 8)
;

select 
	(select u.username from chat_app_structure_test.public.users u where u.user_id = c.user_1) as username1,
	(select u.username from chat_app_structure_test.public.users u where u.user_id = c.user_2) as username2,
	c.conversation_started 
from chat_app_structure_test.public.chats c ;


-- 	MESSAGES
select * 
from chat_app_structure_test.public.messages m;

insert into chat_app_structure_test.public.messages (conversation_id, sender_id, message)
values 
	(1, 3, 'I love big black cocks'),
	(1, 4, 'ME TOO!'),
	(1, 3, 'Let''s suck one together!'),
	(1, 4, 'I WILL text YOU LATER!')
;

select 
	(select u.username from chat_app_structure_test.public.users u where u.user_id = m.sender_id) as username,
	m.message,
	m.sent_at
from chat_app_structure_test.public.messages m;


select * 
from chat_app_structure_test.public.banlist;

insert into chat_app_structure_test.public.banlist (user_id)
select 6


commit; 
rollback;

