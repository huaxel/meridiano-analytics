---
title: Análisis Salarial
---

# Análisis de Distribución Salarial


Análisis estadístico (Histogramas y Box Plots) de los paquetes retributivos por nivel jerárquico.

## Distribución Salarial por Nivel

Visualización de la distribución de retribución total por nivel jerárquico.

```sql employee_data
select
    employee_id,
    job_level,
    sum(final_payout_eur) as total_comp
from meridiano_analysis.remuneration_lean
group by employee_id, job_level
```

```sql boxplot_data
select
    job_level as name,
    quantile(total_comp, 0.01) as min,
    quantile(total_comp, 0.25) as q1,
    quantile(total_comp, 0.50) as median,
    quantile(total_comp, 0.75) as q3,
    quantile(total_comp, 0.99) as max
from ${employee_data}
where job_level is not null
  and total_comp > 0
group by job_level
order by median desc
```

```sql cumulative_dist
select
    total_comp as salary,
    round(percent_rank() over (order by total_comp) * 100, 1) as percentile
from ${employee_data}
where total_comp > 0 
  and total_comp < 500000
  and job_level is not null
qualify row_number() over (partition by floor(total_comp / 2500) order by total_comp) = 1
order by salary
```

<div class="grid grid-cols-1 gap-4">

<div class="card p-4">
    <h3 class="text-lg font-bold mb-2">Box Plot: Distribución por Nivel Jerárquico</h3>
    <p class="text-sm text-gray-500 mb-4">Muestra mediana, quartiles (Q1-Q3), y valores extremos por cada nivel.</p>
    <BoxPlot
        data={boxplot_data}
        name=name
        min=min
        q1=q1
        median=median
        q3=q3
        max=max
        title="Retribución Total por Nivel"
        yAxisTitle="Retribución (€)"
        yFmt=eur0k
        colorPalette={['#ec0000']}
    />
</div>

<div class="card p-4">
    <h3 class="text-lg font-bold mb-2">Distribución Acumulada</h3>
    <p class="text-sm text-gray-500 mb-4">Muestra qué porcentaje de empleados gana menos de cada umbral salarial.</p>
    <LineChart
        data={cumulative_dist}
        x=salary
        y=percentile
        title="Curva de Distribución Acumulada (hasta €500k)"
        xAxisTitle="Retribución Total (€)"
        yAxisTitle="Percentil (%)"
        xFmt=eur0k
        xMax=500000
        colorPalette={['#ec0000']}
    />
</div>

</div>


## Correlación: Nivel vs Retribución

Análisis de la progresión salarial según nivel jerárquico. Permite identificar anomalías (puntos fuera de la tendencia).

```sql scatter_data
select
    job_level,
    CASE 
        WHEN job_level LIKE 'L9%' THEN 9
        WHEN job_level LIKE 'L8%' THEN 8
        WHEN job_level LIKE 'L7%' THEN 7
        WHEN job_level LIKE 'L6%' THEN 6
        WHEN job_level LIKE 'L5%' THEN 5
        WHEN job_level LIKE 'L4%' THEN 4
        WHEN job_level LIKE 'L3%' THEN 3
        WHEN job_level LIKE 'L2%' THEN 2
        WHEN job_level LIKE 'L1%' THEN 1
        ELSE 0 
    END as level_code,
    sum(final_payout_eur) as total_comp,
    first(subsidiary_code) as subsidiary
from meridiano_analysis.remuneration_lean
where job_level is not null
group by employee_id, job_level
having sum(final_payout_eur) > 0
order by level_code
```

<ScatterPlot
    data={scatter_data}
    x=level_code
    y=total_comp
    series=subsidiary
    title="Correlación Nivel / Pago"
    subtitle="Escala Numérica: L1=1 ... L9=9"
    xAxisTitle="Nivel Jerárquico"
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
from meridiano_analysis.remuneration_lean
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
from meridiano_analysis.remuneration_lean
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
  <Column id=max_val title="Máximo" fmt=eur />
</DataTable>

## Explorador de Datos (Auditoría)

Herramienta de búsqueda para identificar casos específicos (Outliers).

<DataTable data={scatter_data} search=true sortable=true rows=10 download=true>
  <Column id=employee_id title="ID Empleado" />
  <Column id=subsidiary title="Filial" />
  <Column id=job_level title="Nivel" />
  <Column id=total_comp title="Retribución Total" fmt=eur />
</DataTable>
