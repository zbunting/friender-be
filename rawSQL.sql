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
        u.username != 'test_user' AND (
            (
            f.is_friending_username != 'test_user' AND
            f.is_friended_username != 'test_user' AND
            l.is_liking_username != 'test_user'
            ) OR (
                l.is_liking_username IS NULL
            ) OR (
                l.is_liking_username != 'test_user' AND
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
        f.is_friending_username = u.username OR
        f.is_friended_username = u.username