import pandas as pd

# Load the two CSV files
file1 = 'offmychest/offmychest_comments_labelled_5_1.csv'
file2 = 'offmychest/offmychest_comments_labelled_5_2.csv'  # <- Change to your second filename

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Check that they have the same number of rows
assert len(df1) == len(df2), "Files have different number of rows!"

# Create a new DataFrame starting from df1
combined = df1.copy()

# Compare the 'comment_type' columns
for idx in range(len(df1)):
    if df1.loc[idx, 'comment_type'] != df2.loc[idx, 'comment_type']:
        combined.loc[idx, 'comment_type'] = -1  # Set to -1 if different

# Save the combined DataFrame
combined.to_csv('offmychest_comments_labelled_combined.csv', index=False)

print("Comparison done. Saved to 'offmychest_comments_labelled_combined.csv'.")
