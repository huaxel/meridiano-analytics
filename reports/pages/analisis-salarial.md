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

```sql salary_ranges
select
    job_level,
    'Q1 (25%)' as metric,
    quantile(total_comp, 0.25) as value
from ${employee_data}
where job_level is not null and total_comp > 0
group by job_level
union all
select
    job_level,
    'Mediana (50%)' as metric,
    quantile(total_comp, 0.50) as value
from ${employee_data}
where job_level is not null and total_comp > 0
group by job_level
union all
select
    job_level,
    'Q3 (75%)' as metric,
    quantile(total_comp, 0.75) as value
from ${employee_data}
where job_level is not null and total_comp > 0
group by job_level
order by job_level, metric
```

<div class="grid grid-cols-1 gap-4">

<div class="card p-4">
    <h3 class="text-lg font-bold mb-2">Distribución Salarial por Nivel</h3>
    <p class="text-sm text-gray-500 mb-4">Q1, Mediana y Q3 de retribución total por nivel jerárquico.</p>
    <BarChart
        data={salary_ranges}
        x=job_level
        y=value
        series=metric
        type=grouped
        title="Quartiles de Retribución por Nivel"
        xAxisTitle="Nivel Jerárquico"
        yAxisTitle="Retribución (€)"
        yFmt=eur0k
        colorPalette={['#ec0000', '#666666', '#cccccc']}
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
    max(final_payout_eur) as max_val
from meridiano_analysis.remuneration_lean
group by job_level
order by median desc
```

<DataTable data={boxplot} title="Estadísticas Detalladas por Nivel">
  <Column id=job_level title="Nivel" />
  <Column id=min_val title="Mínimo" fmt=eur />
  <Column id=q1 title="Q1 (25%)" fmt=eur />
  <Column id=median title="Mediana" fmt=eur />
  <Column id=q3 title="Q3 (75%)" fmt=eur />
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
