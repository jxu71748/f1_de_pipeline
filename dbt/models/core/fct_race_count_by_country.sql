{{ config(materialized='table') }}

with races_with_country as (
    select 
        r.raceid,
        c.country
    from {{ ref('stg_races') }} r
    left join {{ ref('stg_circuits') }} c
        on r.circuitid = c.circuitid
),

race_counts as (
    select
        country,
        count(*) as race_count
    from races_with_country
    group by country
)

select * from race_counts
