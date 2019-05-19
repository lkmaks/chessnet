
select real_player_id, prev_start_date, prev_end_date, start_date, end_date
from (
select real_player_id,
       lag(date_from) over (partition by t1.real_player_id order by t2.date_from) as prev_start_date,
       lag(date_to) over (partition by t1.real_player_id order by t2.date_from) as prev_end_date,
       t2.date_from as start_date,
       t2.date_to as end_date
from playerintournament t1 inner join tournament t2 on t1.tournament_id = t2.id
) x
where start_date <= prev_end_date;



select t1.id from
task t1 inner join realgame t2 on t1.real_game_from_id = t2.id
where t2.game_date >= current_date;



select distinct t2.game_date, sum(t1.rating_delta) over(order by t2.game_date) from
playerinrealgame t1 inner join realgame t2 on t1.real_game_id = t2.id
where t1.real_player_id = (select min(id) from realplayer) and t2.control_type='standard'
order by t2.game_date;


drop view if exists white_winrate_table;
create view white_winrate_table as
    select game_date,
    sum(1 - game_result / 2) over(order by game_date) as points,
    count(*) over(order by game_date) as poss_points
    from realplayer g1 inner join
         (playerinrealgame t1 inner join realgame t2 on t1.real_game_id = t2.id) g2
         on g1.id = g2.real_player_id
    where g1.id = 649 and color = 'white';


select game_date,
case
when poss_points = 0
then -1
else points * 100 / poss_points
end
from white_winrate_table;


