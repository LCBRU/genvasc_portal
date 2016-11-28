  SELECT
       UUID() AS id
     , 'CIVICRM' AS source_system
     , con.birth_date AS date_of_birth
     , cids.nhs_number_1 AS nhs_number
     , gpCustom.practice_code_7 AS practice_code
     , cas.start_date AS date_recruited
     , cas.id AS case_id
     , con.id AS contact_id
  FROM richdev_civicrm.civicrm_case cas
  JOIN richdev_civicrm.civicrm_case_contact cc ON cc.case_id = cas.id
  JOIN richdev_civicrm.civicrm_contact con ON con.id = cc.contact_id 
  JOIN richdev_civicrm.civicrm_value_contact_ids_1 cids ON cids.entity_id = con.id
  JOIN richdev_civicrm.civicrm_relationship practiceRel ON practiceRel.case_id = cas.id AND practiceRel.relationship_type_id = 24
  JOIN richdev_civicrm.civicrm_value_gp_surgery_data_3 gpCustom ON gpCustom.entity_id = practiceRel.contact_id_b
  WHERE cas.case_type_id = 5
      AND cas.id NOT IN (
        SELECT case_id
        FROM genvasc_portal_recruits
        WHERE case_id IS NOT NULL
        )
      AND LENGTH(TRIM(COALESCE(cids.nhs_number_1, ''))) > 0
      AND con.birth_date IS NOT NULL
;