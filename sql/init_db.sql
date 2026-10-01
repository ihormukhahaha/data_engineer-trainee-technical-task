-- 1. events_raw

DROP TABLE IF EXISTS events_raw;

CREATE TABLE events_raw (
    event_id     VARCHAR(64),
    user_id      VARCHAR(64),
    app_id       VARCHAR(64),
    event_name   VARCHAR(64),
    event_time   VARCHAR(64),
    ingested_at  VARCHAR(64),
    country      VARCHAR(64),
    media_source VARCHAR(64),
    campaign     VARCHAR(64),
    revenue_usd  VARCHAR(64),
    is_test      VARCHAR(10)
);

COPY events_raw
FROM '/Users/macbook/Desktop/work/trainee_junior_data_engineer/events_raw.csv'
WITH (FORMAT csv, HEADER true);




-- 2. apps

DROP TABLE IF EXISTS apps;

CREATE TABLE apps (
    app_id   VARCHAR(64),
    app_name VARCHAR(128),
    platform VARCHAR(32)
);

COPY apps
FROM '/Users/macbook/Desktop/work/trainee_junior_data_engineer/apps.csv'
WITH (FORMAT csv, HEADER true);




-- 3. campaign_costs

DROP TABLE IF EXISTS campaign_costs;

CREATE TABLE campaign_costs (
    date         VARCHAR(32),
    app_id       VARCHAR(64),
    country      VARCHAR(10),
    media_source VARCHAR(64),
    campaign     VARCHAR(64),
    cost_usd     VARCHAR(64)
);

COPY campaign_costs
FROM '/Users/macbook/Desktop/work/trainee_junior_data_engineer/campaign_costs.csv'
WITH (FORMAT csv, HEADER true);