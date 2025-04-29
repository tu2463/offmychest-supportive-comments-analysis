import pandas as pd

def clean_automod_comments(input_csv, output_csv):
    # 1. Load the original CSV
    df = pd.read_csv(input_csv)

    # 2. Drop comments containing 'AUTOMOD' (case-insensitive)
    df_cleaned = df[~df['comment_text'].str.contains('AUTOMOD', case=False, na=False)].reset_index(drop=True)
    df_cleaned = df_cleaned[~df_cleaned['comment_text'].str.contains('I am a bot', na=False)]
    df_cleaned = df_cleaned[~df_cleaned['comment_text'].str.contains(r'\[deleted\]', na=False)]
    df_cleaned = df_cleaned[~df_cleaned['comment_text'].str.contains(r'\[removed\]', na=False)]
    # df_cleaned = df_cleaned[df_cleaned['post_id'] <= 50].reset_index(drop=True)

    # 3. Save the cleaned comments to a new CSV
    df_cleaned.to_csv(output_csv, index=False)

    # 4. Print some information
    num_removed = len(df) - len(df_cleaned)
    print(f"✅ {num_removed} comments removed. Saved {len(df_cleaned)} cleaned comments to '{output_csv}'.")

if __name__ == "__main__":
    input_path = "offmychest/offmychest_comments.csv"  # or "./AITA_comments.csv" if needed
    output_path = "offmychest/offmychest_comments_cleaned.csv"
    clean_automod_comments(input_path, output_path)
