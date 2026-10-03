import pandas as pd


def load_daily(path, day):
    df = pd.read_csv(path)
    df = df[df.event_time.str.startswith(day)]
    df["revenue_usd"] = df["revenue_usd"].astype(float)
    totals = {}
    for i, row in df.iterrows():
        key = row["app_id"] + "-" + row["media_source"]
        totals[key] = totals.get(key, 0) + row["revenue_usd"]
    return pd.DataFrame(
        [{"key": k, "revenue": v} for k, v in totals.items()]
    ).sort_values("revenue", ascending=False)




def load_daily(df_or_path: str, day: str) -> pd.DataFrame:
    df = pd.read_csv(df_or_path, dtype=str, keep_default_na=False)

    # is test
    if 'is_test' in df.columns:
        is_test_mask = df['is_test'].astype(str).str.strip().str.lower().isin(['true', '1'])
        df = df[~is_test_mask]

    # to the date format
    df['event_time'] = pd.to_datetime(df['event_time'], utc=True, errors='coerce')
    target_date = pd.to_datetime(day, utc=True).date()

    # filtering by date
    df = df[df['event_time'].dt.date == target_date]
    if df.empty:
        return pd.DataFrame(columns=['app_id', 'media_source', 'revenue'])

    # revenue_usd
    df['revenue_usd'] = (
        df['revenue_usd']
        .astype(str)
        .str.replace(',', '.', regex=False)
        .str.strip()
    )
    df['revenue_usd'] = pd.to_numeric(df['revenue_usd'], errors='coerce').fillna(0.0)

    # deduplication, like in task_2_1
    df['ingested_at'] = pd.to_datetime(df['ingested_at'], utc=True, errors='coerce')
    df = (
        df.sort_values(by=['ingested_at', 'revenue_usd'], ascending=[False, False])
        .drop_duplicates(subset=['event_id'], keep='first')
    )

    result = (
        df.groupby(['app_id', 'media_source'], as_index=False)['revenue_usd']
        .sum()
        .rename(columns={'revenue_usd': 'revenue'})
        .sort_values(by='revenue', ascending=False)
        .reset_index(drop=True)
    )

    return result



res = load_daily("events_raw.csv", "2026-03-01")
print(res)