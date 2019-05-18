DROP TABLE IF EXISTS RealPlayer CASCADE;
DROP TABLE IF EXISTS OnlineUser CASCADE;
DROP TABLE IF EXISTS Article CASCADE;
DROP TABLE IF EXISTS Comment CASCADE;
DROP TABLE IF EXISTS OnlineGame CASCADE;
DROP TABLE IF EXISTS UserInOnlineGame CASCADE;
DROP TABLE IF EXISTS Tournament CASCADE;
DROP TABLE IF EXISTS PlayerInTournament CASCADE;
DROP TABLE IF EXISTS RealGame CASCADE;
DROP TABLE IF EXISTS PlayerInRealGame CASCADE;
DROP TABLE IF EXISTS Task CASCADE;

CREATE TABLE RealPlayer (
    id SERIAL,
    name VARCHAR(20),
    surname VARCHAR(20),
    country VARCHAR(50),
    country_chess_blitz_rating INTEGER,
    country_chess_rapid_rating INTEGER,
    country_chess_standard_rating INTEGER,
    world_chess_blitz_rating INTEGER,
    world_chess_rapid_rating INTEGER,
    world_chess_standard_rating INTEGER,
    wins_as_white INTEGER,
    draws_as_white INTEGER,
    losses_as_white INTEGER,
    wins_as_black INTEGER,
    draws_as_black INTEGER,
    losses_as_black INTEGER,
    PRIMARY KEY (id)
);

CREATE TABLE OnlineUser (
    username VARCHAR(20),
    real_player_id INTEGER,
    email VARCHAR(30),
    password VARCHAR(20),
    decency_rating INTEGER,
    chess_standard_rating INTEGER,
    chess_rapid_rating INTEGER,
    chess_blitz_rating INTEGER,
    task_rating INTEGER,
    wins_as_white INTEGER,
    draws_as_white INTEGER,
    losses_as_white INTEGER,
    wins_as_black INTEGER,
    draws_as_black INTEGER,
    losses_as_black INTEGER,
    PRIMARY KEY (username),
    FOREIGN KEY (real_player_id) REFERENCES RealPlayer(id)
);

CREATE TABLE Article (
    id SERIAL,
    author_username VARCHAR(20),
    article_body text,
    date_published date,
    PRIMARY KEY (id),
    FOREIGN KEY (author_username) REFERENCES OnlineUser(username)
);

CREATE TABLE Comment (
    id SERIAL,
    article_id INTEGER,
    author_username VARCHAR(20),
    post_time TIMESTAMP,
    comment_body text,
    PRIMARY KEY (id),
    FOREIGN KEY (article_id) REFERENCES Article(id),
    FOREIGN KEY (author_username) REFERENCES OnlineUser(username)
);

CREATE TABLE OnlineGame (
    id SERIAL,
    finish_time TIMESTAMP,
    duration INTEGER,
    time_control VARCHAR(40),
    PRIMARY KEY (id)
);

CREATE TABLE UserInOnlineGame (
    id SERIAL,
    online_game_id INTEGER,
    username VARCHAR(20),
    color VARCHAR(10),
    time_left VARCHAR(20),
    game_result INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (online_game_id) REFERENCES OnlineGame(id),
    FOREIGN KEY (username) REFERENCES OnlineUser(username)
);

CREATE TABLE Tournament (
    id SERIAL,
    name VARCHAR(40),
    date_from date,
    date_to date,
    rule VARCHAR(20),
    country VARCHAR(50),
    tournament_info text,
    PRIMARY KEY (id)
);

CREATE TABLE PlayerInTournament (
    id SERIAL,
    tournament_id INTEGER,
    real_player_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (tournament_id) REFERENCES Tournament(id),
    FOREIGN KEY (real_player_id) REFERENCES RealPlayer(id)
);

CREATE TABLE RealGame (
    id SERIAL,
    tournament_id INTEGER,
    game_date date,
    time_control VARCHAR(40),
    game_result INTEGER,
    control_type VARCHAR(10),
    PRIMARY KEY (id),
    FOREIGN KEY (tournament_id) REFERENCES Tournament(id)
);

CREATE TABLE PlayerInRealGame (
    id SERIAL,
    real_player_id INTEGER,
    real_game_id INTEGER,
    color VARCHAR(10),
    time_left VARCHAR(20),
    PRIMARY KEY (id),
    FOREIGN KEY (real_player_id) REFERENCES RealPlayer(id),
    FOREIGN KEY (real_game_id) REFERENCES RealGame(id)
);

CREATE TABLE Task (
    id SERIAL,
    author_username VARCHAR(20),
    online_game_from_id INTEGER,
    real_game_from_id INTEGER,
    task_body text,
    difficulty INTEGER,
    goal VARCHAR(20),
    task_type VARCHAR(20),
    PRIMARY KEY (id),
    FOREIGN KEY (author_username) REFERENCES OnlineUser(username),
    FOREIGN KEY (online_game_from_id) REFERENCES OnlineGame(id),
    FOREIGN KEY (real_game_from_id) REFERENCES RealGame(id)
);
