INSERT INTO user (email, password, first_name, last_name, active)
SELECT
	  e.email_address AS email
    , MD5(RAND()) AS password
    , '' AS first_name
    , '' AS last_name
    , 1 AS active

FROM	(
    SELECT DISTINCT email_address
    FROM etl_user
) e
WHERE	e.email_address NOT IN (
	SELECT 	email
	FROM	user
)
;

INSERT INTO practice_registrations_users (user_id, practice_registration_id)
SELECT
    u.id,
    pr.id
FROM    etl_user e
JOIN    user u ON u.email = e.email_address
JOIN    practice_registration pr ON pr.code = e.practice_code
LEFT JOIN practice_registrations_users pru
    ON pru.user_id = u.id
    AND pru.practice_registration_id = pr.id
WHERE pru.user_id IS NULL
    AND pru.practice_registration_id IS NULL
;