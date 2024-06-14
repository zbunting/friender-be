SELECT
  u.username,
  f.is_friending_username,
  f.is_friended_username,
  l.is_liking_username,
  l.is_liked_username
    FROM users AS u
    LEFT OUTER JOIN friends AS f ON f.is_friending_username = u.username
    LEFT OUTER JOIN likes AS l ON l.is_liking_username = u.username
    WHERE
    -- don't want yourself
        u.username != 'test_user' AND (
            (
            -- any time there isn't a friend connection and you're not
            f.is_friending_username != 'test_user' AND
            f.is_friended_username != 'test_user' AND
            l.is_liking_username != 'test_user' AND
            l.is_liked_username != 'test_user'
            ) OR (
                -- anyone you haven't liked
                l.is_liking_username IS NULL
            ) OR (
                -- anyone you haven't liked
                l.is_liking_username != 'test_user' AND
                -- anyone you're not friends with
                f.is_friending_username IS NULL
            )
        )

SELECT
  u.username,
  f.is_friending_username,
  f.is_friended_username,
  l.is_liking_username,
  l.is_liked_username
    FROM users AS u
    LEFT OUTER JOIN friends AS f ON f.is_friending_username = u.username
    LEFT OUTER JOIN likes AS l ON l.is_liking_username = u.username
    WHERE
    -- don't want yourself
        u.username != 'test_user3' AND (
            (
            -- any time there isn't a friend connection
            f.is_friending_username != 'test_user3' AND
            f.is_friended_username != 'test_user3' AND
            l.is_liking_username != 'test_user3' AND
            l.is_liked_username != 'test_user3'
            ) OR (
                -- anyone you haven't liked
                l.is_liking_username IS NULL
            ) OR (
                -- anyone you haven't liked
                l.is_liking_username != 'test_user3' AND
                -- anyone you're not friends with
                f.is_friending_username IS NULL
            )
        )



SELECT
  u.username,
  f.is_friending_username,
  f.is_friended_username
    FROM users AS u
    JOIN friends AS f ON f.is_friending_username = u.username
    WHERE
        u.username != 'test_user' AND (
        f.is_friending_username = 'test_user' OR
        f.is_friended_username = 'test_user'
        )


SELECT u.username, l.is_liked_username, l.is_liking_username
FROM users as u
JOIN likes as l ON l.is_liked_username = u.username


CREATE VIEW not_friends as
SELECT
  u.username
  FROM users as u
  WHERE u.username NOT IN (
    SELECT
      f.is_friended_username
      FROM friends as f
      WHERE f.is_friending_username = 'test_user'
    ) AND u.username != 'test_user';

CREATE VIEW not_likes as
SELECT
  u.username
  FROM users as u
  WHERE u.username NOT IN (
    SELECT
      l.is_liked_username
      FROM likes as l
      WHERE l.is_liking_username = 'test_user'
    ) AND u.username != 'test_user';


WITH dont_show as (
SELECT
    f.is_friended_username as username
    FROM friends as f
    WHERE
    f.is_friending_username = 'test_user'

    UNION

SELECT
    l.is_liked_username
    FROM likes as l
    WHERE
    l.is_liking_username = 'test_user'
)

SELECT
    *
    FROM users as u
    LEFT OUTER JOIN dont_show as n ON u.username = n.username
    WHERE n.username IS NULL AND u.username != 'test_user'

SELECT
    *
    FROM users as u
    WHERE u.username NOT IN (
        SELECT
        n.username FROM dont_show as n
    )