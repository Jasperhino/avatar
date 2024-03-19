# %%
import pandas as pd
import praw

reddit = praw.Reddit(
    client_id="ogawHHFV761eByjoV5A7KQ",
    client_secret="yPk0rB9m8bSY1BK7wI30Ti3RuHcIKw",
    user_agent="my praw app",
)

posts = []
all_comments = []  # Renamed for clarity
# keywords_ = ["awe"]
keywords = ["empathy", "empathize", "empathetic", "empath"]

# keywords = [
#     "identif",
#     "indentification",
#     "anthropomorph",
#     "anthropomorphism",
#     "behavior",
#     "behaviour change",
#     "humanlike",
#     "humanization",
#     "humanize",
# ]
avatar_subreddit = reddit.subreddit("Avatar")
for keyword in keywords:
    for post in avatar_subreddit.search(
        keyword,
        syntax="lucene",
        sort="top",
        time_filter="all",
    ):
        if post.selftext == "[deleted]" or post.id in [p[2] for p in posts]:
            continue

        posts.append(
            [
                post.title,
                post.score,
                post.id,
                post.subreddit,
                post.url,
                post.num_comments,
                post.selftext,
                post.created,
            ]
        )

        # Load all comments
        post.comments.replace_more(
            limit=None
        )  # Set limit=None to try to replace all MoreComments
        for comment in post.comments.list():
            if comment.body == "[deleted]" or comment.id in [
                c[2] for c in all_comments
            ]:
                continue
            all_comments.append(
                [
                    comment.body,
                    comment.score,
                    comment.id,
                    comment.subreddit,
                    comment.link_id,
                    comment.parent_id,
                    comment.created,
                ]
            )

posts_df = pd.DataFrame(
    posts,
    columns=[
        "title",
        "score",
        "id",
        "subreddit",
        "url",
        "num_comments",
        "body",
        "created",
    ],
)

comments_df = pd.DataFrame(
    all_comments,
    columns=[
        "body",
        "score",
        "id",
        "subreddit",
        "link_id",
        "parent_id",
        "created",
    ],
)

print(posts_df.head())  # Print just the head to keep the output manageable
# Specify a clear path where you want to save the CSV files
posts_df.to_csv(f"data_new/posts_empathy.csv", index=False)
comments_df.to_csv(f"data_new/comments_empathy.csv", index=False)
print(f"Number of posts: {len(posts_df)}")
print(f"Number of comments: {len(comments_df)}")

# %%
