SELECT * FROM
RealGame t1 INNER JOIN Tournament t2
ON t1.tournament_id = t2.id
WHERE t1.game_date >= to_date('01.01.2019', 'dd.mm.yyyy');
