select 
    subsidiary_code,
    category_normalized,
    sum(theoretical_eur) as theoretical,
    sum(final_payout_eur) as paid,
    count(*) as recs
from '../../raw_data/remuneration.parquet'
group by 1, 2
union all
select 
    'All' as subsidiary_code,
    category_normalized,
    sum(theoretical_eur) as theoretical,
    sum(final_payout_eur) as paid,
    count(*) as recs
from '../../raw_data/remuneration.parquet'
group by 1, 2
