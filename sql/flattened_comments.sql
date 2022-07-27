WITH with_id AS (
    SELECT
        *,
        record_metadata[
            'CreateTime'
        ] || '-' || record_content['id'] AS record_id
    FROM
        snowflake_ml.reddit.snowflake_ml_reddit_comments_423303504
),

long_table AS (
    SELECT
        with_id.record_id,
        f.path AS _key,
        f.value AS _value
    FROM
        with_id,
        LATERAL flatten(input => with_id.record_metadata) AS f
    UNION ALL
    SELECT
        with_id.record_id,
        f.path AS _key,
        f.value AS _value
    FROM
        with_id,
        LATERAL flatten(input => with_id.record_content) AS f
)

SELECT
    record_id,
    metadata_create_time,
    metadata_key,
    metadata_offset,
    metadata_partition,
    metadata_topic,
    author,
    id,
    saved,
    subreddit_type,
    gilded,
    name,
    score_hidden,
    subreddit_id,
    can_gild,
    link_url,
    stickied,
    body,
    replies,
    created_utc,
    link_title,
    controversiality,
    parent_id,
    subreddit,
    archived,
    link_id,
    score
FROM
    long_table PIVOT(
    max(_value) FOR _key IN (
        'CreateTime',
        'key',
        'offset',
        'partition',
        'topic',
        'author',
        'id',
        'saved',
        'subreddit_type',
        'gilded',
        'name',
        'score_hidden',
        'subreddit_id',
        'can_gild',
        'link_url',
        'stickied',
        'body',
        'replies',
        'created_utc',
        'link_title',
        'controversiality',
        'parent_id',
        'subreddit',
        'archived',
        'link_id',
        'score'
    )
) AS t (
    record_id,
    metadata_create_time,
    metadata_key,
    metadata_offset,
    metadata_partition,
    metadata_topic,
    author,
    id,
    saved,
    subreddit_type,
    gilded,
    name,
    score_hidden,
    subreddit_id,
    can_gild,
    link_url,
    stickied,
    body,
    replies,
    created_utc,
    link_title,
    controversiality,
    parent_id,
    subreddit,
    archived,
    link_id,
    score
);
