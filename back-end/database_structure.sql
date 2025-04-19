CREATE TABLE Users
(
	user_id SERIAL PRIMARY key,
	username VARCHAR(100) NOT NULL,
	email VARCHAR(255) UNIQUE NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	confirmed BOOLEAN DEFAULT FALSE,
	access_token VARCHAR(255),
	refresh_token VARCHAR(255)
);

CREATE TABLE Profile (
    user_id INT PRIMARY KEY REFERENCES Users(user_id) ON DELETE CASCADE,
    phone_number VARCHAR(20),
    biography TEXT,
    img_url TEXT
);

CREATE TABLE Posts (
    post_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    description TEXT,
    img_url TEXT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Chats (
    conversation_id SERIAL PRIMARY KEY,
    user_1 INT REFERENCES Users(user_id) ON DELETE CASCADE,
    user_2 INT REFERENCES Users(user_id) ON DELETE CASCADE,
    conversation_started TIMESTAMP DEFAULT CURRENT_TIMESTAMP
--    UNIQUE(LEAST(user_1, user_2), GREATEST(user_1, user_2))
);

CREATE TABLE Messages (
    message_id SERIAL PRIMARY KEY,
    conversation_id INT REFERENCES Chats(conversation_id) ON DELETE cascade,
    sender_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,   -- Tracks if the message is read
    is_deleted BOOLEAN DEFAULT FALSE, -- For soft deleting messages
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE Contacts (
    contact_id SERIAL PRIMARY KEY,
    user_id_1 INT REFERENCES Users(user_id) ON DELETE CASCADE,
    user_id_2 INT REFERENCES Users(user_id) ON DELETE CASCADE,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
--    UNIQUE(LEAST(user_id_1, user_id_2), GREATEST(user_id_1, user_id_2))
);

CREATE TABLE BanList (
    ban_id SERIAL PRIMARY KEY,
    user_id INT UNIQUE REFERENCES Users(user_id) ON DELETE CASCADE,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



