SELECT c.C_id,Surname,Birthday
from bonus_client as c
left join history_note as h
on c.C_id =h.C_id
left join ticket as t
on h.T_id=t.T_id
Where  month(purchase_date) !='$month' and year(purchase_date) != '$year'
group by c.C_id