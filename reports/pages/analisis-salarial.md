---
title: Análisis Salarial
---

# Análisis de Distribución Salarial


Análisis estadístico (Histogramas y Box Plots) de los paquetes retributivos por nivel jerárquico.

## Histograma Global

Distribución de la retribución total (fija + variable procesada).

```sql employee_data
select
    employee_id,
    job_level,
    sum(final_payout_eur) as total_comp
from tia_elena.remuneration_lean
group by employee_id, job_level
```

```sql histogram_main
select
    job_level,
    floor(total_comp / 5000) * 5000 as bin_start,
    count(*) as frequency
from ${employee_data}
where total_comp < 300000
  and total_comp > 0
group by all
order by bin_start
```

```sql histogram_top
select
    job_level,
    floor(total_comp / 50000) * 50000 as bin_start,
    count(*) as frequency
from ${employee_data}
where total_comp >= 300000
group by all
order by bin_start
```

<div class="grid grid-cols-1 gap-4">

<div class="card p-4">
    <h3 class="text-lg font-bold mb-2">Distribución General (Plantilla Base)</h3>
    <p class="text-sm text-gray-500 mb-4">Salarios hasta €300k (99% de empleados). Bins de €5k.</p>
    <BarChart
        data={histogram_main}
        x=bin_start
        y=frequency
        series=job_level
        stacked=true
        title="Frecuencia por Nivel"
        colorPalette={['#ec0000', '#2b2b2b', '#444444', '#555555', '#666666', '#777777', '#888888', '#999999', '#aaaaaa', '#bbbbbb', '#cccccc']}
    />
</div>

<div class="card p-4">
    <h3 class="text-lg font-bold mb-2">Alta Dirección (Top Management)</h3>
    <p class="text-sm text-gray-500 mb-4">Salarios > €300k. Bins de €50k.</p>
    <BarChart
        data={histogram_top}
        x=bin_start
        y=frequency
        series=job_level
        stacked=true
        title="Frecuencia Alta Dirección"
        colorPalette={['#ec0000', '#2b2b2b', '#444444', '#555555', '#666666', '#777777', '#888888', '#999999', '#aaaaaa', '#bbbbbb', '#cccccc']}
    />
</div>

</div>


## Correlación: Nivel vs Retribución

Análisis de la progresión salarial según nivel jerárquico. Permite identificar anomalías (puntos fuera de la tendencia).

```sql scatter_data
select
    job_level,
    CASE 
        WHEN job_level = 'VP' THEN 6
        WHEN job_level = 'D' THEN 5
        WHEN job_level = 'M' THEN 4
        WHEN job_level = 'S' THEN 3
        WHEN job_level = 'A' THEN 2
        WHEN job_level = 'J' THEN 1
        ELSE 0 
    END as level_code,
    sum(final_payout_eur) as total_comp,
    first(subsidiary_code) as subsidiary
from tia_elena.remuneration
where total_comp > 0
group by employee_id, job_level
order by level_code
```

<ScatterPlot
    data={scatter_data}
    x=level_code
    y=total_comp
    series=subsidiary
    title="Correlación Nivel / Pago"
    subtitle="Escala Numérica: J=1 ... VP=6"
    xAxisTitle="Nivel Jerárquico (Calculado)"
    yAxisTitle="Retribución Total (€)"
    yLog=true
    opacity=0.6
/>

## Debug: Top Salarios
```sql debug_salaries
select
    employee_id,
    job_level,
    sum(final_payout_eur) as total_comp
from tia_elena.remuneration
group by employee_id, job_level
order by total_comp desc
limit 20
```

<DataTable data={debug_salaries} />


## Dispersión por Nivel (Quartiles)

Análisis de consistencia interna y equidad.

```sql boxplot
select
    job_level,
    quantile(final_payout_eur, 0.25) as q1,
    quantile(final_payout_eur, 0.50) as median,
    quantile(final_payout_eur, 0.75) as q3,
    min(final_payout_eur) as min_val,
    max(final_payout_eur) as max_val -- Note: Evidence BoxPlot might need specific format, using table for detail
from tia_elena.remuneration
group by job_level
order by median desc
```

<DataTable data={boxplot} title="Estadísticas por Nivel">
  <Column id=job_level title="Nivel" />
  <Column id=min_val title="Mínimo" fmt=eur />
  <Column id=q1 title="Q1 (25%)" fmt=eur />
  <Column id=median title="Mediana" fmt=eur />
  <Column id=q3 title="Q3 (75%)" fmt=eur />
  <Column id=max_val title="Máximo" fmt=eur />
</DataTable>
