WITH with_id AS (
    SELECT
        *,
        record_metadata['CreateTime'] || '-' || record_content['id'] AS record_id
    FROM
        snowflake_ml_reddit_posts_1911518057
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
    archived,
    author,
    can_gild,
    contest_mode,
    created_utc,
    domain,
    gilded,
    hidden,
    hide_score,
    id,
    is_self,
    locked,
    name,
    num_comments,
    over_18,
    permalink,
    quarantine,
    removed,
    saved,
    score,
    selftext,
    spam,
    spoiler,
    stickied,
    subreddit,
    subreddit_id,
    thumbnail,
    title,
    url,
    visited
FROM
    long_table PIVOT(
    max(_value) FOR _key IN (
        'CreateTime',
        'key',
        'offset',
        'partition',
        'topic',
        'archived',
        'author',
        'can_gild',
        'contest_mode',
        'created_utc',
        'domain',
        'gilded',
        'hidden',
        'hide_score',
        'id',
        'is_self',
        'locked',
        'name',
        'num_comments',
        'over_18',
        'permalink',
        'quarantine',
        'removed',
        'saved',
        'score',
        'selftext',
        'spam',
        'spoiler',
        'stickied',
        'subreddit',
        'subreddit_id',
        'thumbnail',
        'title',
        'url',
        'visited'
    )
) AS t (
    record_id,
    metadata_create_time,
    metadata_key,
    metadata_offset,
    metadata_partition,
    metadata_topic,
    archived,
    author,
    can_gild,
    contest_mode,
    created_utc,
    domain,
    gilded,
    hidden,
    hide_score,
    id,
    is_self,
    locked,
    name,
    num_comments,
    over_18,
    permalink,
    quarantine,
    removed,
    saved,
    score,
    selftext,
    spam,
    spoiler,
    stickied,
    subreddit,
    subreddit_id,
    thumbnail,
    title,
    url,
    visited
);
