# Answers to Task Questions

## Task 2.1
If two deliveries of the same event share the exact same `ingested_at`, standard ROW-based sorting can result in the selection
of different (random) rows across different runs. This can occur due to multithreading and parallel scan, buffer cache, or
changes to the execution plan. To ensure a deterministic result, an additional sorting criterion, `revenue_usd`, was defined.
In the event of a timestamp tie, the record with the higher revenue figure is selected.

## Task 2.2
Yes, days without events are significant. The function operates on physical table rows rather than calendar days; consequently, it selects the current record and the seven preceding ones from the date-sorted table. This data can span a time interval of any length.

As for a solution, you could create a calendar grid and generate a complete sequence of calendar dates for each `app_id`, ranging from the launch date to the current date. Then, join this with your table while preserving all dates and filling in missing values ​​with zeros. With this dataset, the `7-day moving average` will calculate correctly.

## Task 2.3
I used `FULL OUTER JOIN` for the join. This ensures that the final table retains both revenues without corresponding expenses and, conversely, expenses without corresponding revenues.
- If there are costs but zero revenue, this indicates low campaign efficiency or a problem at some stage of its implementation.
- If, however, there is revenue without costs, this may be due to organic activity from previous campaigns.

I applied the `NULLIF` function to the divisor to avoid a potential division-by-zero error. If `cost_usd` is zero, the expression will return `NULL` instead of an error.

## Task 2.4
We will filter the data based on column `ingested_at` rather than `even_time` to correctly capture new rows. Column `even_time` reflects the user-side execution time on the device; filtering by it would cause us to miss, for instance, events with adjusted revenue.

A minimum time interval of, say, 3–7 days can be selected; this should represent the maximum time it takes for delayed events or revenue corrections to arrive.
• If the window is too short, processing will be faster and cheaper, but delayed data will be missed.
• If it is too long, all data will be captured, but queries will become slower and more expensive due to the constant re-reading of duplicates.

## Task 3.2
If the script crashes while writing output, the standard process might result in incomplete or corrupted files. To prevent this, I implemented writing to a temporary, isolated directory using tempfile.TemporaryDirectory() first; if execution completes successfully, we move everything from there to the target directory.
