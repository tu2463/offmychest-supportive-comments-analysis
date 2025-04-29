import pandas as pd

# Load the files
comments_df = pd.read_csv('offmychest/offmychest_comments_labelled_5_2.csv')
# comments_df = pd.read_csv('offmychest/offmychest_comments_labelled_combined.csv')
posts_df = pd.read_csv('offmychest/offmychest_posts.csv')

# Group by post_id and calculate supportive_comments and all_comments
grouped = comments_df.groupby('post_id').agg(
    supportive_comments=('comment_type', lambda x: (x == 1).sum()),
    all_comments=('comment_type', 'count')
).reset_index()

# Calculate supportive_percentage
grouped['supportive_percentage'] = grouped['supportive_comments'] / grouped['all_comments']

# Merge with posts dataframe
posts_merged = posts_df.merge(grouped, on='post_id', how='left')

# Fill NaN values (in case some posts have no comments)
posts_merged['supportive_comments'] = posts_merged['supportive_comments'].fillna(0).astype(int)
posts_merged['all_comments'] = posts_merged['all_comments'].fillna(0).astype(int)
posts_merged['supportive_percentage'] = posts_merged['supportive_percentage'].fillna(0)

# Save to new file
output_path = 'offmychest/offmychest_posts_comments_5_2.csv'
posts_merged.to_csv(output_path, index=False)

print(f"Done. Output saved as '{output_path}'.")