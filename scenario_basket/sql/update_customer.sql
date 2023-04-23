UPDATE bd_bonus.bonus_client
SET Total_bonus = Total_bonus + ($count * $bonus_accuted)
WHERE C_id = $client_id;