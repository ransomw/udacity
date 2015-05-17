-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- \c vagrant;
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
       id serial PRIMARY KEY,
       p_name text
);

CREATE TABLE matches (
       id serial PRIMARY KEY,
       winner integer references players (id),
       loser integer references players (id)
);

CREATE VIEW standings AS
       SELECT players.id, p_name, wins, num_matches
       FROM (SELECT players.id, count(winner) as wins
             FROM players LEFT JOIN matches
             ON players.id = winner
             GROUP BY players.id) as wins_sel,
            (SELECT players.id, count(winner) as num_matches
             FROM players LEFT JOIN matches
             ON players.id = winner OR players.id = loser
             GROUP BY players.id) as matches_sel,
            players
       WHERE wins_sel.id = players.id AND matches_sel.id = players.id
       ORDER BY wins DESC;
