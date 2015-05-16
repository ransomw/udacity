-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

\c vagrant;
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
       id serial PRIMARY KEY,
       p_name text
);

CREATE TABLE matches (
       winner integer references players (id),
       loser integer references players (id)
);

CREATE VIEW standings AS
       SELECT players.id, p_name, wins, num_matches
       FROM (SELECT id, count(winner) as wins
             FROM players LEFT JOIN matches
             ON id = winner
             GROUP BY id) as wins_sel,
            (SELECT id, count(winner) as num_matches
             FROM players LEFT JOIN matches
             ON id = winner OR id = loser
             GROUP BY id) as matches_sel,
            players
       WHERE wins_sel.id = players.id AND matches_sel.id = players.id
       ORDER BY wins DESC;
