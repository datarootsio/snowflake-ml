INSERT INTO
ml_posts_toxic(
    record_id,
    created_timestamp,
    subreddit,
    author,
    title,
    is_toxic,
    model_version
)
SELECT
    record_id,
    created_timestamp,
    subreddit,
    author,
    title,
    ML_PREDICT_PROD(title)['prediction'] AS is_toxic,
    ML_PREDICT_PROD(title)['model_version'] AS model_version
FROM
    new_ml_posts_clean
WHERE
    metadata$action = 'INSERT'  -- noqa: L057
