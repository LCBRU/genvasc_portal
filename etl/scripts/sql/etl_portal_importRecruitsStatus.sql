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