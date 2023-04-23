SELECT Surname,Birthday,Total_bonus,Flight_num,T_price
from bonus_client as c
left join history_note as h
on c.C_id =h.C_id
left join ticket as t
on h.T_id=t.T_id
Where  T_price = (select max(T_price)
				from ticket as t
				left join history_note as h
				on h.T_id =t.T_id
                left join bonus_client as c
                on c.C_id =h.C_id
                Where (Flight_num)='$number' );
