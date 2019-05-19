
select id from realplayer where world_chess_standard_rating = (select max(world_chess_standard_rating) from realplayer);
select game_date from realgame where id in (select real_game_id from playerinrealgame where real_player_id = 305) order by game_date;
select name from tournament where id in (select tournament_id from playerintournament where real_player_id = 305)


select concat(t3.name, ' ', t3.surname), count(t4.id) as cnt from
((realplayer t1 inner join playerinrealgame t2 on t1.id = t2.real_player_id) t3
inner join
task t4
on t3.real_game_id = t4.real_game_from_id)
group by t3.name, t3.surname
order by cnt desc;

select real_player_id, count(*) from playerinrealgame group by real_player_id;

select distinct t2.game_date, sum(t1.rating_delta) over(order by t2.game_date) from
        playerinrealgame t1 inner join realgame t2 on t1.real_game_id = t2.id
        where t1.real_player_id = 351 and t2.control_type='standard'
        order by t2.game_date;

select * from realplayer;

select id, name, surname, world_chess_standard_rating from realplayer order by world_chess_standard_rating desc;