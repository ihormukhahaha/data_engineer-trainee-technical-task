import pandas as pd
import numpy as np

# events_raw.csv
events_data = {
    'event_id': ['0', '1', '2', '2', '3', '3', '4', '5'],
    'user_id': ['0', '1', '1', '1', '2', '2', '1', '1'],
    'app_id': ['104', '101', '101', '101', '102', '102', '104', '103'],
    'event_name': ['install', 'purchase', 'purchase', 'purchase', 'install', 'install', 'purchase', 'purchase'],
    'event_time': [
        '2026-10-01 10:00:00', '2026-10-01 11:00:00', '2026-10-01 12:00:00', 
        '2026-10-01 12:00:00', '2026-10-02 08:00:00', '2026-10-02 09:00:00',
        '2026-10-02 10:00:00', '2026-10-02 11:00:00'
    ],
    'ingested_at': [
        '2026-10-01 10:05:00', '2026-10-01 11:05:00', '2026-10-01 12:05:00', 
        '2026-10-01 12:10:00', '2026-10-02 08:05:00', '2026-10-02 09:05:00',
        '2026-10-02 10:05:00', '2026-10-02 11:05:00'
    ],
    'country': ['US', '', '--', '--', 'UA', 'UA', 'us', 'FR'],
    'media_source': ['facebook', 'google', 'facebook', 'facebook', 'google', 'google', 'facebook', 'facebook'],
    'campaign': ['cmp_fb_1', 'cmp_gg', 'cmp_fb_2', 'cmp_fb_2', 'cmp_gg', 'cmp_gg', 'cmp_fb_3', 'cmp_fb_01'],
    'revenue_usd': ['3.0', '9.99', '4,99', '5.99', 'NULL', '', '19.99', '2.99'],
    'is_test': [False, False, False, False, False, False, False, True]
}
pd.DataFrame(events_data).to_csv('events_raw.csv', index=False)

# apps.csv
apps_data = {
    'app_id': ['101', '102 ', '103', '104'],
    'app_name': ['Super Game', 'Puzzle Master', 'Fitness Tracker', '2048'],
    'platform': ['ios', 'android', 'ios', 'ios'],
    'store_id': ['com.supergame.ios', 'com.puzzlemaster.android', 'com.fitnesstracker.ios', 'com.2048.ios'],
    'launched_on': ['2026-01-01', '2026-01-15', '2026-02-01', '2026-02-14']
}
pd.DataFrame(apps_data).to_csv('apps.csv', index=False)

# campaign_costs.csv
costs_data = {
    'date': ['2026-03-01', '2026-03-01', '2026-03-02', '2026-03-02', '2026-03-02'],
    'app_id': ['101', '101', '102', '104', '103'],
    'media_source': ['google', 'facebook', 'google', 'facebook', 'tiktok'],
    'campaign': ['cmp_gg', 'cmp_fb_2', 'cmp_gg', 'cmp_fb_3', 'cmp_tt_01'],
    'cost_usd': [150.0, 100.0, 200.0, 120.0, 80.0],
    'impressions': [15000, 10000, 18000, 12000, 5000],
    'clicks': [700, 500, 900, 600, 250]
}
pd.DataFrame(costs_data).to_csv('campaign_costs.csv', index=False)

# events_staging.csv
events_staging = {
    'event_id': ['4', '6'],
    'user_id': ['1', '2'],
    'app_id': ['104', '101'],
    'event_name': ['purchase', 'purchase'],
    'event_time': [
        '2026-10-02 17:15:00', '2026-10-03 11:00:00'
    ],
    'ingested_at': [
        '2026-10-01 17:20:00', '2026-10-03 11:05:00'
    ],
    'country': ['US', 'FR'],
    'media_source': ['facebook', 'facebook'],
    'campaign': ['cmp_fb_3', 'cmp_fb_2'],
    'revenue_usd': ['21.99', '7.99'],
    'is_test': [False, False]
}
pd.DataFrame(events_staging).to_csv('events_staging.csv', index=False)


print("csv-files generated")