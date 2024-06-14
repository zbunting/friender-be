SELECT u.username, f.is_friending_username, f.is_friended_username, l.is_liking_username, l.is_liked_username
    FROM users as u
    LEFT OUTER JOIN friends as f ON f.is_friending_username = u.username
    LEFT OUTER JOIN likes as l ON l.is_liking_username = u.username
    WHERE
        u.username != 'test_user' and (
            (
            f.is_friending_username != 'test_user' and
            f.is_friended_username != 'test_user' and
            l.is_liking_username != 'test_user'
            ) or (
                l.is_liking_username is NULL
            ) or (
                l.is_liking_username != 'test_user' and
                f.is_friending_username is NULL
            )
        )


SELECT u.username, f.is_friending_username, f.is_friended_username, l.is_liking_username, l.is_liked_username
    FROM users as u
    LEFT OUTER JOIN friends as f ON f.is_friending_username = u.username
    LEFT OUTER JOIN likes as l ON l.is_liking_username = u.username
    WHERE
        u.username != 'test_user' and (
            (
            f.is_friending_username != 'test_user' and
            f.is_friended_username != 'test_user' and
            l.is_liking_username != 'test_user'
            )
        )



f.is_friended_username != 'test_user' and




        SELECT u.username, f.is_friending_username, l.is_liking_username
    FROM users as u
    LEFT OUTER JOIN friends as f ON f.is_friending_username = u.username
    LEFT OUTER JOIN likes as l ON l.is_liking_username = u.username
    WHERE l.is_liking_username != 'test_user' and
        f.is_friended_username != 'test_user' and
        f.is_friending_username != 'test_user'