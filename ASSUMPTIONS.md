# Assumptions

## 1. The data
1. I received only the PDF file with the assignment, without the CSV files. I generated the relevant data myself.

## 2. SQL
1. Unknown country data is imputed as 'XX', missing revenue is set to 0.0, and `is_test` = true records are excluded.

2. `table_daily_revenue` - is a temporary table containing unique app_id and date values. The `moving_avg_7d` calculation relies solely on available days; it considers the 7 preceding days present in the table rather than 7 calendar days. If there are fewer than 7 rows, the average is calculated from the first day up to the current day.

3. `event_raw.csv` and `campaing` - temporary tables that contain all the necessary data, combined by `date`, `app_id`, `media_source` та `campaing`. I use `COALESCE` in the `SELECT` statement to ensure the presence of all the data used to join the tables.

4. A physical table was created for `clean_events`, similar to how the temporary one was created. This enables operations such as `ON CONFLICT`. Additionally, the `event_id` column was set as the `PRIMARY KEY`. We also added the `events_staging.csv` table, which stores nights or corrected events.

5. Added the three described checks, which should return 0 rows if all three checks pass.
