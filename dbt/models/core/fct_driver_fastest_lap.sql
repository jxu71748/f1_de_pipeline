{{ config(materialized='table') }}

with lap_times as (
    select 
        lt.driverid,
        r.year,
        lt.milliseconds
    from {{ ref('stg_lap_times') }} lt
    inner join {{ ref('stg_races') }} r
        on lt.raceid = r.raceid
    where lt.milliseconds is not null
),

fastest_laps as (
    select
        driverid,
        year,
        min(milliseconds) as fastest_lap_time
    from lap_times
    group by driverid, year
),

final as (
    select
        fl.driverid,
        d.forename || ' ' || d.surname as driver_name,
        fl.year,
        fl.fastest_lap_time
    from fastest_laps fl
    left join {{ ref('stg_drivers') }} d
        on fl.driverid = d.driverid
)

select * from final
