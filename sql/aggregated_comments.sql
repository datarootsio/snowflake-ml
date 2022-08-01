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
            WHEN subreddit = 'interestingasfuck' THEN 'interestingasfuck'
            WHEN subreddit = 'Unexpected' THEN 'Unexpected'
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
    count(record_id) AS number_or_records,
    count(DISTINCT author) AS number_of_authors,
    avg(len(link_title)) AS average_title_length,
    avg(len(body)) AS average_body_length
FROM
    dims
GROUP BY
    CUBE(
        subreddit_type,
        stickied,
        controversiality,
        subreddit,
        created_date
    );
