# Assumptions

## 1. The data
1. I received only the PDF file with the assignment, without the CSV files. I generated the relevant data myself.

## 2. SQL
1. Unknown country data is imputed as 'XX', missing revenue is set to 0.0, and `is_test` = true records are excluded.

2. `table_daily_revenue` - is a temporary table containing unique app_id and date values. The `moving_avg_7d` calculation relies solely on available days; it considers the 7 preceding days present in the table rather than 7 calendar days. If there are fewer than 7 rows, the average is calculated from the first day up to the current day.

3. `event_raw.csv` and `campaing` - temporary tables that contain all the necessary data, combined by `date`, `app_id`, `media_source` та `campaing`. I use `COALESCE` in the `SELECT` statement to ensure the presence of all the data used to join the tables (`date`, `app_id`, `media_source` та `campaing`).
