UPDATE etl_recruit_status
SET civicrm_case_id = NULL
WHERE civicrm_case_id = 0
;

UPDATE etl_recruit_status
SET civicrm_contact_id = NULL
WHERE civicrm_contact_id = 0
;

UPDATE 	recruit r
JOIN	etl_recruit_status e ON e.id = r.id
SET
	  r.civicrm_contact_id = e.civicrm_case_id
	, r.civicrm_case_id = e.civicrm_case_id
;