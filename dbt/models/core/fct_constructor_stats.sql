
{{ config(materialized = 'table') }}

WITH constructor_points AS (
    SELECT
        r.constructorid,
        c.name AS constructor_name,
        EXTRACT(YEAR FROM ra.race_timestamp) AS year,
        SUM(CAST(r.points AS FLOAT64)) AS total_points
    FROM {{ ref('stg_results') }} r
    LEFT JOIN {{ ref('stg_races') }} ra ON r.raceid = ra.raceid
    LEFT JOIN {{ ref('stg_constructors') }} c ON r.constructorid = c.constructorid
    GROUP BY constructorid, constructor_name, year
),

constructor_wins AS (
    SELECT
        r.constructorid,
        c.name AS constructor_name,
        EXTRACT(YEAR FROM ra.race_timestamp) AS year,
        COUNT(*) AS wins
    FROM {{ ref('stg_results') }} r
    LEFT JOIN {{ ref('stg_races') }} ra ON r.raceid = ra.raceid
    LEFT JOIN {{ ref('stg_constructors') }} c ON r.constructorid = c.constructorid
    WHERE r.position = '1'
    GROUP BY constructorid, constructor_name, year
)

SELECT
    p.constructorid,
    p.constructor_name,
    p.year,
    p.total_points,
    COALESCE(w.wins, 0) AS wins
FROM constructor_points p
LEFT JOIN constructor_wins w
  ON p.constructorid = w.constructorid AND p.year = w.year
