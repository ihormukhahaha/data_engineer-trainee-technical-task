import pandas as pd


def clean_events_data(file_path_or_buffer):

    # the function will not crash due to an invalid string
    try:
        # keep_default_na=False - we will work specifically with 'NULL' or ''
        df = pd.read_csv(file_path_or_buffer, dtype=str, keep_default_na=False)
    except Exception as e:
        return pd.DataFrame(), pd.DataFrame([{"error": str(e)}]), 0



    # rows containing errors are isolated so that they can be returned separately later
    quarantined_list = []
    clean_rows = []
    # to count and report the number of incorrect ones
    unparseable_revenue_count = 0

    required_cols = {
        'event_id', 'user_id', 'app_id', 'event_name', 'event_time', 
        'ingested_at', 'country', 'media_source', 'campaign', 'revenue_usd', 'is_test'
    }

    if not required_cols.issubset(set(df.columns)):
        return pd.DataFrame(), df, 0



    # event_id check
    for _, row in df.iterrows():
        row_dict = row.to_dict()
        if not row_dict.get('event_id'):
            row_dict['quarantine_reason'] = 'missing event_id'
            quarantined_list.append(row_dict)
        else:
            clean_rows.append(row_dict)

    # if all rows have been added to quarantine
    if not clean_rows:
        return pd.DataFrame(), pd.DataFrame(quarantined_list), 0

    clean_df = pd.DataFrame(clean_rows)



    # removed test rows
    is_test_mask = clean_df['is_test'].astype(str).str.strip().str.lower().isin(['true', '1'])
    # dataset containing non-test data
    clean_df = clean_df[~is_test_mask].copy()

    # revenue_usd in float format, other values ​​are replaced with 0.0
    def parse_revenue(val):
        nonlocal unparseable_revenue_count
        if val is None:
            unparseable_revenue_count += 1
            return 0.0
        
        val_str = str(val).strip().upper()
        if val_str in ['', 'NULL']:
            unparseable_revenue_count += 1
            return 0.0
        
        val_str = val_str.replace(',', '.')
        
        try:
            return float(val_str)
        except ValueError:
            # some unexpected data error
            unparseable_revenue_count += 1
            return 0.0

    clean_df['revenue_usd'] = clean_df['revenue_usd'].apply(parse_revenue)



    # normalization of 'country' to a two-letter uppercase code
    def normalize_country(country):
        if country is None:
            # values ​​that cannot be matched are replaced with 'XX'
            return 'XX'
        c_str = str(country).strip().upper()
        if len(c_str) == 2 and c_str.isalpha():
            return c_str
        return 'XX'

    clean_df['country'] = clean_df['country'].apply(normalize_country)



    # recognition of timestamps taking into account the UTC time zone
    for col in ['event_time', 'ingested_at']:
        # errors='coerce' -> incorrect date to NaT
        clean_df[col] = pd.to_datetime(clean_df[col], utc=True, errors='coerce')

    # invalid rows - move to quarantine
    bad_time_mask = clean_df['event_time'].isna() | clean_df['ingested_at'].isna()
    # if there are any
    if bad_time_mask.any():
        bad_time_rows = clean_df[bad_time_mask].to_dict('records')
        for r in bad_time_rows:
            r['quarantine_reason'] = 'invalid timestamp format'
            quarantined_list.append(r)
        # remove incorrect rows from the main table
        clean_df = clean_df[~bad_time_mask].copy()



    # duplicates are processed according to the same rule as in task 2.1
    clean_df = clean_df.sort_values(
        by=['ingested_at', 'revenue_usd'], 
        ascending=[False, False]
    )
    clean_df = clean_df.drop_duplicates(subset=['event_id'], keep='first').reset_index(drop=True)



    quarantine_df = pd.DataFrame(quarantined_list)
    return clean_df, quarantine_df, unparseable_revenue_count