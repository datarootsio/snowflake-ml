WITH dims AS (
    SELECT
        record_id,
        author,
        title,
        selftext,
        num_comments,
        score,
        spoiler,
        stickied,
        CASE
            WHEN subreddit = 'AskReddit' THEN 'AskReddit'
            WHEN subreddit = 'nba' THEN 'nba'
            WHEN subreddit = 'newsbotbot' THEN 'newsbotbot'
            WHEN subreddit = 'NoStupidQuestions' THEN 'NoStupidQuestions'
            ELSE 'Other'
        END AS subreddit,
        CASE
            WHEN domain IN ('i.redd.it', 'v.redd.it', 'reddit.com') THEN 'reddit.com'
            WHEN domain IN ('youtu.be', 'youtube.com') THEN 'youtube.com'
            WHEN startswith(domain, 'self.') THEN 'self.*'
            WHEN domain = 'twitter.com' THEN 'twitter.com'
            WHEN domain = 'instagram.com' THEN 'instagram.com'
            ELSE 'other'
        END AS domain, -- noqa: L029
        CASE
            WHEN thumbnail = 'self' THEN 'self'
            WHEN thumbnail = 'default' THEN 'default'
            WHEN thumbnail = 'nsfw' THEN 'nsfw'
            WHEN thumbnail = 'image' THEN 'image'
            WHEN thumbnail = 'spoiler' THEN 'spoiler'
            ELSE 'other'
        END AS thumbnail,
        date(created_utc) AS created_date
    FROM
        posts_typed
    WHERE
        NOT over_18
)

SELECT
    subreddit,
    domain,
    thumbnail,
    created_date,
    stickied,
    count(record_id) AS number_of_records,
    count(DISTINCT author) AS number_of_authors,
    avg(len(title)) AS average_title_length,
    avg(len(selftext)) AS average_body_length,
    sum(num_comments) AS number_of_comments,
    sum(score) AS total_score
FROM
    dims
GROUP BY
    created_date,
    subreddit,
    domain,
    thumbnail,
    stickied;
