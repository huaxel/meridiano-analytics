---
title: Panel de Control
---

<div class="mb-4">
    <Dropdown 
        name=subsidiary 
        data={subsidiaries} 
        value=subsidiary_code 
        title="Filtrar por Filial"
        defaultValue="All"
    >
        <DropdownOption value="All" label="Todas las Filiales" />
    </Dropdown>
</div>

```sql subsidiaries
select distinct subsidiary_code from meridiano_analysis.remuneration_summary where subsidiary_code != 'All' order by 1
```

```sql kpis
select
    sum(theoretical) as total_demand,
    sum(paid) as total_paid,
    1 - (sum(paid) / sum(theoretical)) as haircut,
    sum(recs) as records
from meridiano_analysis.remuneration_summary
where (subsidiary_code = '${inputs.subsidiary.value}' or (subsidiary_code = 'All' and '${inputs.subsidiary.value}' = 'All'))
  and ('${inputs.subsidiary.value}' != 'All' OR subsidiary_code = 'All') 
  -- Logic: If Dropdown=Specific, match Specific. If Dropdown=All, match the 'All' row we created.
```

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


<Alert status=warning>
  <div class="flex items-center gap-2">
    <strong>Resumen Ejecutivo:</strong>
    <span>
      La filial con mayor desviación presupuestaria es 
      <strong><Value data={impact} column=subsidiary_code row=0 /></strong>, 
      con un déficit de 
      <strong><Value data={impact} column=gap fmt=eur row=0 /></strong>.
    </span>
  </div>
  <div class="mt-2 text-sm">
    <a href="./analisis-salarial" class="text-red-700 hover:underline font-bold">
       Ver Análisis Detallado por Nivel &rarr;
    </a>
  </div>
</Alert>

---

## Impacto por Filial

Top 10 filiales con mayor brecha entre retribución teórica y real.

```sql impact
select 
    subsidiary_code,
    sum(theoretical) as demand,
    sum(paid) as paid,
    sum(theoretical) - sum(paid) as gap
from meridiano_analysis.remuneration_summary
where subsidiary_code != 'All' 
  and (subsidiary_code = '${inputs.subsidiary.value}' or '${inputs.subsidiary.value}' = 'All')
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
    sum(paid) as paid
from meridiano_analysis.remuneration_summary
where category_normalized is not null
  and (subsidiary_code = '${inputs.subsidiary.value}' or (subsidiary_code = 'All' and '${inputs.subsidiary.value}' = 'All'))
  and ('${inputs.subsidiary.value}' != 'All' OR subsidiary_code = 'All')
group by category_normalized
order by paid desc
```

<script>
    let donutData = [];
    $: if (categories) {
        donutData = categories.map(d => ({
            value: d.paid,
            name: d.category_normalized
        }));
    }
</script>

<div class="card p-4 h-96">
    <h3 class="text-lg font-bold mb-2">Distribución de Masa Salarial</h3>
    <ECharts config={{
        tooltip: {
            trigger: 'item',
            formatter: '{b}: {c} ({d}%)'
        },
        legend: {
            bottom: 0,
            left: 'center',
            type: 'scroll' 
        },
        series: [
            {
                name: 'Masa Salarial',
                type: 'pie',
                radius: ['45%', '75%'],
                center: ['50%', '45%'], 
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2
                },
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: '20',
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: donutData,
                color: ['#ec0000', '#2b2b2b', '#444444', '#555555', '#666666', '#777777', '#888888', '#999999', '#aaaaaa', '#bbbbbb']
            }
        ]
    }} />
</div>

