INSERT INTO bd_bonus.purchased_tickets ( id_t, id_c, Airport_in, Airport_out,
                                        class, flight, purchase_date,Price ,
                                        number, bonus )
VALUES ( $T_id, $client_id ,'$Airport_in','$Airport_out',
        '$T_class', '$Flight_num', CURRENT_DATE(), $T_price * $count,
        $count ,$bonus_accuted * $count)