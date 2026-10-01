WITH cleaned_data AS (
    SELECT
        event_id,
        user_id,
        app_id,
        event_name,
        -- timestamps to TIMESTAMPTZ for time zone consistency
        CAST(event_time AS TIMESTAMPTZ) AS event_time,
        CAST(ingested_at AS TIMESTAMPTZ) AS ingested_at,

        -- unknown country data -> 'XX', known -> uppercase
        CASE 
            WHEN country IS NULL OR country IN ('', '--') THEN 'XX'
            ELSE UPPER(country)
        END AS country,

        media_source,
        campaign,

        -- unknown income data -> 0.0, known -> with separator ','
        CASE 
            WHEN revenue_usd IS NULL OR revenue_usd IN ('', 'NULL') THEN 0.0
            ELSE CAST(REPLACE(revenue_usd, ',', '.') AS NUMERIC(10, 4))
        END AS revenue_usd
    FROM events_raw
    WHERE LOWER(COALESCE(is_test, 'false')) NOT IN ('true', '1')
),

-- one row for event_id with adjusted revenue
ranked_by_ingest AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY event_id
            -- newer data first by time, then by revenue
            ORDER BY ingested_at DESC, revenue_usd DESC
        ) AS rn
    FROM cleaned_data
)

-- return the deduplicated clean data directly
SELECT 
    event_id,
    user_id,
    app_id,
    event_name,
    event_time,
    ingested_at,
    country,
    media_source,
    campaign,
    revenue_usd
FROM ranked_by_ingest
-- the latest record with the highest revenue for event_id
WHERE rn = 1;