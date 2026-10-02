-- PostgreSQL

-- revenue by (date, app_id, media_source, campaign)
WITH daily_revenue AS (
    SELECT
        CAST(event_time AS DATE) AS date,
        app_id,
        media_source,
        campaign,
        SUM(revenue_usd) AS revenue_usd
    FROM events_cleaned
    GROUP BY CAST(event_time AS DATE), app_id, media_source, campaign
),

-- costs by (date, app_id, media_source, campaign)
daily_costs AS (
    SELECT
        CAST(date AS DATE) AS date,
        app_id,
        media_source,
        campaign,
        SUM(CAST(cost_usd AS NUMERIC(10, 4))) AS cost_usd,
        SUM(CAST(impressions AS BIGINT)) AS impressions,
        SUM(CAST(clicks AS BIGINT)) AS clicks
    FROM campaign_costs
    GROUP BY CAST(date AS DATE), app_id, media_source, campaign
)

-- combined revenue and costs data by (date, app_id, media_source, and campaign)
SELECT
    COALESCE(r.date, c.date) AS date,
    COALESCE(r.app_id, c.app_id) AS app_id,
    COALESCE(r.media_source, c.media_source) AS media_source,
    COALESCE(r.campaign, c.campaign) AS campaign,
    COALESCE(r.revenue_usd, 0.0) AS revenue_usd,
    COALESCE(c.cost_usd, 0.0) AS cost_usd,
    COALESCE(c.impressions, 0) AS impressions,
    COALESCE(c.clicks, 0) AS clicks,
    
    -- ROAS
    ROUND(
        COALESCE(r.revenue_usd, 0.0) / NULLIF(c.cost_usd, 0.0), 
        4
    ) AS roas
FROM daily_revenue r
FULL OUTER JOIN daily_costs c
    -- only if all 4 parameters match simultaneously
    ON r.date = c.date
   AND r.app_id = c.app_id
   AND r.media_source = c.media_source
   AND r.campaign = c.campaign
ORDER BY date, app_id, media_source, campaign;