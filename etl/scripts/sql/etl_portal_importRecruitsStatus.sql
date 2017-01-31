UPDATE etl_recruit_status
SET
      civicrm_case_id = CASE WHEN civicrm_case_id = 0 THEN NULL ELSE civicrm_case_id END
    , civicrm_contact_id = CASE WHEN civicrm_contact_id = 0 THEN NULL ELSE civicrm_contact_id END
    , status = CASE WHEN status = 'NULL' THEN NULL ELSE status END
    , study_id = CASE WHEN study_id = 'NULL' THEN NULL ELSE study_id END
    , processed_by = CASE WHEN processed_by = 'NULL' THEN NULL ELSE processed_by END
;

UPDATE 	recruit r
JOIN	etl_recruit_status e ON e.id = r.id
SET
	  r.civicrm_contact_id = e.civicrm_case_id
	, r.civicrm_case_id = e.civicrm_case_id
;

DELTE FROM recruit WHERE source_system <> 'PORTAL'
;

SELECT id FROM user WHERE email = 'lcbruit@uhl-tr.nhs.uk' INTO @system_user_id
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
FROM 	etl_recruit_status e
JOIN	practice_registration pr ON pr.code = e.practice_code
WHERE	e.civicrm_case_id NOT IN (
	SELECT 	civicrm_case_id
	FROM recruit
	WHERE	civicrm_case_id IS NOT NULL
)
;