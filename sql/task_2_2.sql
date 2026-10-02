-- PostgreSQL

-- temporary table with data grouped by calendar days and app_id
WITH table_daily_revenue AS (
    SELECT
        app_id,
        CAST(event_time AS DATE) AS event_date,
        SUM(revenue_usd) AS daily_revenue
    FROM events_cleaned
    GROUP BY app_id, CAST(event_time AS DATE)
)

-- from the de-duplicated events, for every app_id and every calendar day:
SELECT
    app_id,
    event_date,

    -- daily revenue
    daily_revenue,

    -- the running total of revenue since the app launched
    SUM(daily_revenue) OVER (
        -- for each app, all preceding days sorted are important
        PARTITION BY app_id 
        ORDER BY event_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_revenue,

    -- the 7-day moving average of daily revenue
    AVG(daily_revenue) OVER (
        PARTITION BY app_id 
        ORDER BY event_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_avg_7d,

    -- the day-over-day change in daily revenue, in percent
    ROUND(
        (daily_revenue - LAG(daily_revenue) OVER (
            PARTITION BY app_id
            ORDER BY event_date)
        ) / NULLIF(
            LAG(daily_revenue) OVER (
            PARTITION BY app_id
            ORDER BY event_date), 0) * 100, 
        2
    ) AS dod_change_pct
FROM table_daily_revenue
ORDER BY app_id, event_date;