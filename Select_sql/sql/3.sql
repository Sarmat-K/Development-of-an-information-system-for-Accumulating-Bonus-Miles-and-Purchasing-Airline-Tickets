SELECT  Surname, count(purchase_date)
from bonus_client as c
left join history_note as h
on c.C_id =h.C_id
left join ticket as t
on h.T_id=t.T_id
WHERE YEAR(purchase_date) ='$year'
GROUP BY Surname;