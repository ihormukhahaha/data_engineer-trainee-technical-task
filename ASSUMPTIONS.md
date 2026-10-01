# Assumptions

## 1. The data
1. I received only the PDF file with the assignment, without the CSV files. I generated the relevant data myself.

## 2. SQL
1. If two deliveries of the same event share the exact same `ingested_at`, standard ROW-based sorting can result
   in the selection of different (random) rows across different runs. This can occur due to multithreading and
   parallel scan, buffer cache, or changes to the execution plan. To ensure a deterministic result, an additional
   sorting criterion, `revenue_usd`, was defined. In the event of a timestamp tie, the record with the higher revenue
   figure is selected.

2.
