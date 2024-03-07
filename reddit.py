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
# keyword = "awe"
keyword = "empathy OR empathize OR empathetic OR empath"
# keyword = "identif OR indentification OR anthropomorph OR anthropomorphism OR behavior OR behaviour change"
avatar_subreddit = reddit.subreddit("Avatar")
for post in avatar_subreddit.search(keyword, sort="top", time_filter="all"):
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
