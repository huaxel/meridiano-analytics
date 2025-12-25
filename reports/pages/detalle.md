---
title: Detalle Operativo
---

# Detalle Operativo


Consulta granular de registros procesados.

```sql detail
select
    employee_id,
    subsidiary_code,
    job_level,
    remuneration_concept,
    theoretical_eur,
    final_payout_eur,
    funding_ratio
from tia_elena.remuneration
order by final_payout_eur desc
limit 1000
```

<DataTable data={detail} search=true sortable=true downloadable=true rows=20>
  <Column id=employee_id title="ID Empleado" />
  <Column id=subsidiary_code title="Filial" />
  <Column id=job_level title="Nivel" />
  <Column id=remuneration_concept title="Concepto" />
  <Column id=theoretical_eur title="Teórico (€)" fmt=eur />
  <Column id=final_payout_eur title="Pago Final (€)" fmt=eur />
  <Column id=funding_ratio title="Ratio" fmt="0.00%" />
</DataTable>
