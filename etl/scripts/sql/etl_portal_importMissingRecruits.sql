SELECT id FROM user WHERE username = 'system' INTO @system_user_id
;

INSERT INTO recruit (id, source_system, practice_registration_id, user_id, nhs_number, date_of_birth, date_recruited, date_created, civicrm_contact_id, civicrm_case_id)
SELECT
	  e.id
	, e.source_system
	, pr.id
	, @system_user_id
	, e.nhs_number
	, e.date_of_birth
	, e.date_recruited
	, CURDATE()
	, e.civicrm_contact_id
	, e.civicrm_case_id
FROM 	etl_missing_recruits e
JOIN	practice_registration pr ON pr.code = e.practice_code
WHERE	e.civicrm_case_id NOT IN (
	SELECT 	civicrm_case_id
	FROM recruit
	WHERE	civicrm_case_id IS NOT NULL
)
;