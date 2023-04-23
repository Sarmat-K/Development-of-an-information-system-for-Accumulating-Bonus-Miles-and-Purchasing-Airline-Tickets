SELECT Surname,Birthday
FROM bonus_client
LEFT JOIN history_note hn on bonus_client.C_id = hn.C_id
left join ticket t on bonus_client.C_id = t.C_id
WHERE Total_bonus is NULL;