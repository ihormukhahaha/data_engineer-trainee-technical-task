# Answers to Task Questions

## Task 2.1
If two deliveries of the same event share the exact same `ingested_at`, standard ROW-based sorting can result in the selection
of different (random) rows across different runs. This can occur due to multithreading and parallel scan, buffer cache, or
changes to the execution plan. To ensure a deterministic result, an additional sorting criterion, `revenue_usd`, was defined.
In the event of a timestamp tie, the record with the higher revenue figure is selected.

## Task 2.2
Yes, days without events are significant. The function operates on physical table rows rather than calendar days; consequently, it selects the current record and the seven preceding ones from the date-sorted table. This data can span a time interval of any length.

As for a solution, you could create a calendar grid and generate a complete sequence of calendar dates for each `app_id`, ranging from the launch date to the current date. Then, join this with your table while preserving all dates and filling in missing values ​​with zeros. With this dataset, the `7-day moving average` will calculate correctly.
