---
title: Panel de Control
---

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10 mt-2">
  <div class="bg-red-50 p-6 rounded-xl border border-red-100 shadow-sm flex items-center justify-between group hover:border-red-200 transition-all">
    <div>
        <h3 class="text-red-600 text-xs font-bold uppercase tracking-widest mb-1">Área Corporativa</h3>
        <p class="text-3xl font-bold text-red-950 tracking-tight">Personas & Cultura</p>
    </div>
    <div class="text-red-200 group-hover:text-red-300 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
    </div>
  </div>

  <div class="bg-white p-6 rounded-xl border border-gray-100 shadow-sm flex items-center justify-between group hover:border-gray-300 transition-all">
    <div>
        <h3 class="text-gray-400 text-xs font-bold uppercase tracking-widest mb-1">Analista Senior</h3>
        <p class="text-3xl font-bold text-gray-900 tracking-tight">Doña Submarino</p>
    </div>
    <div class="h-10 w-10 rounded-full bg-gray-100 flex items-center justify-center text-gray-400 font-bold border border-gray-200">
        DS
    </div>
  </div>
</div>

```sql kpis
select
    sum(theoretical_eur) as total_demand,
    sum(final_payout_eur) as total_paid,
    1 - (sum(final_payout_eur) / sum(theoretical_eur)) as haircut,
    count(*) as records
from tia_elena.remuneration
```

<BigValue 
  data={kpis} 
  value=total_demand 
  fmt=eur 
  title="Demanda Total" 
/>
<BigValue 
  data={kpis} 
  value=total_paid 
  fmt=eur 
  title="Pago Real" 
/>
<BigValue 
  data={kpis} 
  value=haircut 
  fmt=pct 
  title="Recorte Global"
/>
<BigValue 
  data={kpis} 
  value=records 
  fmt="#,##0" 
  title="Registros Procesados" 
/>

---

## Impacto por Filial

Top 10 filiales con mayor brecha entre retribución teórica y real.

```sql impact
select 
    subsidiary_code,
    sum(theoretical_eur) as demand,
    sum(final_payout_eur) as paid,
    demand - paid as gap
from tia_elena.remuneration
group by subsidiary_code
order by gap desc
limit 10
```

<BarChart 
    data={impact}
    x=subsidiary_code
    y={["demand", "paid"]}
    title="Demanda vs Pago Real (Top 10 Déficit)"
/>

## Distribución por Categoría

```sql categories
select
    category_normalized,
    sum(final_payout_eur) as paid
from tia_elena.remuneration
where category_normalized is not null
group by category_normalized
order by paid desc
```

<DataTable
    data={categories}
    title="Masa Salarial por Concepto"
    rows=10
/>

