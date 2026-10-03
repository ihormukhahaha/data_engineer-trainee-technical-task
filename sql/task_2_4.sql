-- PostgreSQL

-- create a physical table for ON CONFLICT.
CREATE TABLE IF NOT EXISTS clean_events (
    event_id     VARCHAR(64) PRIMARY KEY,
    user_id      VARCHAR(64),
    app_id       VARCHAR(64),
    event_name   VARCHAR(64),
    event_time   TIMESTAMPTZ,
    ingested_at  TIMESTAMPTZ,
    country      VARCHAR(10),
    media_source VARCHAR(64),
    campaign     VARCHAR(64),
    revenue_usd  NUMERIC(10, 4)
);

-- incremental loading of new and updated events from events_staging
WITH staged_cleaned AS (
    SELECT
        event_id,
        user_id,
        app_id,
        event_name,
        CAST(event_time AS TIMESTAMPTZ) AS event_time,
        CAST(ingested_at AS TIMESTAMPTZ) AS ingested_at,
        CASE 
            WHEN country IS NULL OR country IN ('', '--') THEN 'XX'
            ELSE UPPER(country)
        END AS country,
        media_source,
        campaign,
        CASE 
            WHEN revenue_usd IS NULL OR revenue_usd IN ('', 'NULL') THEN 0.0
            ELSE CAST(REPLACE(revenue_usd, ',', '.') AS NUMERIC(10, 4))
        END AS revenue_usd
    -- the raw data
    FROM events_staging
    -- select data for the last 7 days
    WHERE CAST(ingested_at AS TIMESTAMPTZ) >= (SELECT MAX(CAST(ingested_at AS TIMESTAMPTZ)) FROM events_staging) - INTERVAL '7 days'
      AND LOWER(COALESCE(is_test, 'false')) NOT IN ('true', '1')
),
ranked_by_ingest AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY event_id
            ORDER BY ingested_at DESC, revenue_usd DESC
        ) AS rn
    FROM staged_cleaned
)
INSERT INTO clean_events (
    event_id, user_id, app_id, event_name, event_time,
    ingested_at, country, media_source, campaign, revenue_usd
)
SELECT
    event_id, user_id, app_id, event_name, event_time,
    ingested_at, country, media_source, campaign, revenue_usd
FROM ranked_by_ingest
-- keep only the first (newest and most accurate) row for each event_id
WHERE rn = 1

-- data update
ON CONFLICT (event_id) DO UPDATE SET
    user_id      = EXCLUDED.user_id,
    app_id       = EXCLUDED.app_id,
    event_name   = EXCLUDED.event_name,
    event_time   = EXCLUDED.event_time,
    ingested_at  = EXCLUDED.ingested_at,
    country      = EXCLUDED.country,
    media_source = EXCLUDED.media_source,
    campaign     = EXCLUDED.campaign,
    revenue_usd  = EXCLUDED.revenue_usd
-- update if the incoming record is newer or contains corrected income data
WHERE EXCLUDED.ingested_at > clean_events.ingested_at
   OR (EXCLUDED.ingested_at = clean_events.ingested_at AND EXCLUDED.revenue_usd > clean_events.revenue_usd);