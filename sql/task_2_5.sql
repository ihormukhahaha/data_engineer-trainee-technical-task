-- PostgreSQL

-- checking for duplicate event_ids in the target cleaned table
SELECT 
    event_id, 
    COUNT(*) AS duplicate_count
FROM clean_events
GROUP BY event_id
HAVING COUNT(*) > 1;


-- validation of incorrect data
SELECT 
    event_id, 
    revenue_usd
FROM clean_events
WHERE revenue_usd IS NULL 
   OR revenue_usd < 0;


-- check for incorrect timestamps
SELECT 
    event_id, 
    event_time, 
    ingested_at
FROM clean_events
WHERE event_time > ingested_at;