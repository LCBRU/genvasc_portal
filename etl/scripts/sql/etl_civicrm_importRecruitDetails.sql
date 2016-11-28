UPDATE etl_portal_recruits
SET civicrm_case_id = NULL
WHERE civicrm_case_id = 0
;

UPDATE etl_portal_recruits
SET civicrm_contact_id = NULL
WHERE civicrm_contact_id = 0
;

UPDATE genvasc_portal_recruits r
JOIN etl_portal_recruits e ON e.id = r.id
SET
      r.nhs_number = e.nhs_number
    , r.dob = e.dob
    , r.date_recruited = e.date_recruited
    , r.case_id = e.civicrm_case_id
    , r.contact_id = e.civicrm_contact_id
;

INSERT INTO genvasc_portal_recruits(id, source_system, practice_code, nhs_number, dob, date_recruited, case_id, contact_id)
SELECT
	  id
	, source_system
	, practice_code
	, nhs_number
	, dob
	, date_recruited
	, civicrm_case_id
	, civicrm_contact_id
FROM etl_portal_recruits
WHERE id NOT IN (
	SELECT id FROM genvasc_portal_recruits
)
;