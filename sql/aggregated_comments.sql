WITH dims AS (
    SELECT
        record_id,
        author,
        link_title,
        body,
        subreddit_type,
        stickied,
        controversiality,
        CASE
            WHEN subreddit = 'AskReddit' THEN 'AskReddit'
            WHEN subreddit = 'nba' THEN 'nba'
            WHEN subreddit = 'newsbotbot' THEN 'newsbotbot'
            WHEN subreddit = 'NoStupidQuestions' THEN 'NoStupidQuestions'
            ELSE 'Other'
        END AS subreddit,
        date(created_utc) AS created_date
    FROM
        comments_typed
)

SELECT
    subreddit_type,
    stickied,
    controversiality,
    subreddit,
    created_date,
    count(record_id) AS number_of_records,
    count(DISTINCT author) AS number_of_authors,
    sum(len(link_title)) AS sum_title_length,
    sum(len(body)) AS sum_body_length
FROM
    dims
GROUP BY
    created_date,
    subreddit_type,
    stickied,
    controversiality,
    subreddit;
