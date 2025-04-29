import praw
import csv

reddit = praw.Reddit(
    client_id="ubSMCk9wff5ihGusNNl0UQ",
    client_secret="8wkTOKCNTZziL4M9423s2pnX7KmP_w",
    user_agent="AggressionStudyScript by /u/Sherrrie",
)

# === Output files ===
subrreddit_name = "AITA"
posts_file = f"{subrreddit_name}_posts.csv"
comments_file = f"{subrreddit_name}_comments.csv"

# === Open both files ===
with open(posts_file, mode='w', encoding='utf-8', newline='') as posts_csv, \
     open(comments_file, mode='w', encoding='utf-8', newline='') as comments_csv:

    posts_writer = csv.writer(posts_csv)
    comments_writer = csv.writer(comments_csv)

    posts_writer.writerow(['post_id', 'post_text'])
    comments_writer.writerow(['post_id', 'comment_id', 'comment_text'])

    for post_id, submission in enumerate(reddit.subreddit(subrreddit_name).hot(limit=50), 1):
        submission.comments.replace_more(limit=None)

        # === Save post ===
        post_text = (submission.title + "\n\n" + submission.selftext).strip()
        posts_writer.writerow([post_id, post_text])

        # === Save each comment ===
        for comment_id, comment in enumerate(submission.comments.list(), 1):
            if hasattr(comment, "body"):
                comment_text = comment.body.strip()
                comments_writer.writerow([post_id, comment_id, comment_text])

print("✅ Done! Posts saved to posts.csv and comments saved to comments.csv")