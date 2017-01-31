SELECT
	  r.id
	, r.source_system
	, pr.code AS practice_code
	, r.nhs_number
	, r.date_of_birth AS dob
	, r.date_recruited
	, r.civicrm_contact_id
	, r.civicrm_case_id
FROM recruit r
JOIN practice_registration pr ON pr.id = r.practice_registration_id
WHERE r.source_system = 'PORTAL'
;