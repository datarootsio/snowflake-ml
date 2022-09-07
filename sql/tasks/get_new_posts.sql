INSERT INTO
ml_posts(
    record_id,
    created_timestamp,
    subreddit,
    author,
    title
)
SELECT
    record_content['id']::VARCHAR AS record_id,
    (record_metadata['CreateTime']::NUMBER / 1000)::TIMESTAMP AS created_timestamp,
    record_content['subreddit']::VARCHAR AS subreddit,
    record_content['author']::VARCHAR AS author,
    record_content['title']::VARCHAR AS title
FROM
    new_posts
WHERE
    metadata$action = 'INSERT'  -- noqa: L057
