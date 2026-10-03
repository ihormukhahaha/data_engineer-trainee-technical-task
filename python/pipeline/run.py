import argparse
import os
import shutil
import tempfile
from pathlib import Path
import pandas as pd

from cleaner import clean_events_data


def main():
    # command-line argument processing
    parser = argparse.ArgumentParser(description="Run ETL Pipeline")
    parser.add_argument("--input", required=True, help="Input directory containing CSV files or path to events_raw.csv")
    parser.add_argument("--output", required=True, help="Output directory for Parquet and Quarantine files")
    parser.add_argument("--since", required=False, help="Filter events starting from this date (YYYY-MM-DD)")

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)



    # path to the events_raw.csv
    if input_path.is_dir():
        raw_csv_file = input_path / "events_raw.csv"
    else:
        raw_csv_file = input_path

    if not raw_csv_file.exists():
        raise FileNotFoundError(f"Input file not found: {raw_csv_file}")



    # rows in
    raw_df_initial = pd.read_csv(raw_csv_file, dtype=str, keep_default_na=False)
    rows_in = len(raw_df_initial)

    # clean_events_data
    clean_df, quarantine_df, _ = clean_events_data(raw_csv_file)

    # filtering by --since
    if args.since and not clean_df.empty:
        since_dt = pd.to_datetime(args.since, utc=True)
        clean_df = clean_df[clean_df["event_time"] >= since_dt].copy()

    # rows out, rows quarantined
    rows_out = len(clean_df)
    rows_quarantined = len(quarantine_df)
    
    # duplicates removed
    duplicates_removed = (rows_in - rows_quarantined) - rows_out



    # event_date (YYYY-MM-DD)
    if not clean_df.empty:
        clean_df["event_date"] = clean_df["event_time"].dt.strftime("%Y-%m-%d")

    # atomic write to a temporary directory for crash safety
    output_path.mkdir(parents=True, exist_ok=True)
    clean_events_dir = output_path / "clean_events"
    quarantine_file = output_path / "quarantine.csv"

    # a temporary folder that is automatically deleted after exiting the with block
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        temp_clean_dir = temp_dir_path / "clean_events"

        # record of cleared events in Parquet format with partitioning by event date
        if not clean_df.empty:
            clean_df.to_parquet(
                temp_clean_dir,
                engine="pyarrow",
                partition_cols=["event_date"], # event_date=2026-10-03/xxxx.parquet
                index=False
            )

            # rewriting partitions without damaging old data
            for part in temp_clean_dir.rglob("*.parquet"):
                rel_path = part.relative_to(temp_clean_dir)
                dest_path = clean_events_dir / rel_path
                # creates the target partition subfolder if it did not exist
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(part), str(dest_path))

        # separately record the rows sent to quarantine
        if not quarantine_df.empty:
            quarantine_df.to_csv(quarantine_file, index=False)

    # print result
    print(f"rows in: {rows_in}, rows out: {rows_out}, duplicates removed: {duplicates_removed}, rows quarantined: {rows_quarantined}")



if __name__ == "__main__":
    main()