SELECT
    record_id,
    metadata_offset::int AS metadata_offset,
    metadata_partition::int AS metadata_partition,
    metadata_topic::varchar AS metadata_topic,
    archived::boolean AS archived,
    author::varchar AS author,
    can_gild::boolean AS can_gild,
    contest_mode::boolean AS contest_mode,
    created_utc::timestamp AS created_utc,
    domain::varchar AS domain,  -- noqa: L029
    gilded::int AS gilded,
    hidden::boolean AS hidden,
    hide_score::boolean AS hide_score,
    id::varchar AS id,
    is_self::boolean AS is_self,
    locked::boolean AS locked,
    name::varchar AS name,  -- noqa: L029
    num_comments::int AS num_comments,
    over_18::boolean AS over_18,
    permalink::varchar AS permalink,
    quarantine::boolean AS quarantine,
    removed::boolean AS removed,
    saved::boolean AS saved,
    score::int AS score,
    selftext::varchar AS selftext,
    spam::boolean AS spam,
    spoiler::boolean AS spoiler,
    stickied::boolean AS stickied,
    subreddit::varchar AS subreddit,
    subreddit_id::varchar AS subreddit_id,
    thumbnail::varchar AS thumbnail,
    title::varchar AS title,
    visited::boolean AS visited,
    (metadata_create_time::number / 1000)::timestamp AS metadata_create_time,
    parse_json(metadata_key) AS metadata_key,
    parse_url(url, 1) AS url  -- noqa: L029
FROM flattened_posts;
