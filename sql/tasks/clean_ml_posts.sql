INSERT INTO
ml_posts_clean(
    record_id,
    created_timestamp,
    subreddit,
    author,
    title
)
SELECT
    record_id,
    created_timestamp,
    subreddit,
    author,
    regexp_replace(title, '[^[:ascii:]]') AS title
FROM
    new_ml_posts
WHERE
    metadata$action = 'INSERT'  -- noqa: L057
