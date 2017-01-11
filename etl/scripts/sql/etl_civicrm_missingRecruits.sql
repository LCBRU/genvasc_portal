  SELECT
       UUID() AS id
     , 'CIVICRM' AS source_system
     , con.birth_date AS date_of_birth
     , cids.${CIVI_CUSCOL_NHS_NUMBER} AS nhs_number
     , gpCustom.${CIVI_CUSCOL_PRACTICE_CODE} AS practice_code
     , cas.start_date AS date_recruited
     , cas.id AS case_id
     , con.id AS contact_id
  FROM ${CIVI_CIVIDB_NAME}.civicrm_case cas
  JOIN ${CIVI_CIVIDB_NAME}.civicrm_case_contact cc ON cc.case_id = cas.id
  JOIN ${CIVI_CIVIDB_NAME}.civicrm_contact con ON con.id = cc.contact_id 
  JOIN ${CIVI_CIVIDB_NAME}.${CIVI_CUSTAB_CONTACT} cids ON cids.entity_id = con.id
  JOIN ${CIVI_CIVIDB_NAME}.civicrm_relationship practiceRel ON practiceRel.case_id = cas.id AND practiceRel.relationship_type_id = ${CIVI_CUSID_PRACTICE_RELATIONSHIP_TYPE}
  JOIN ${CIVI_CIVIDB_NAME}.${CIVI_CUSTAB_SURGERY} gpCustom ON gpCustom.entity_id = practiceRel.contact_id_b
  LEFT JOIN genvasc_portal_recruits gpr ON gpr.case_id = cas.id
  WHERE cas.case_type_id = ${CIVI_CUSID_GENVASC_CASE_TYPE}
      AND LENGTH(TRIM(COALESCE(cids.${CIVI_CUSCOL_NHS_NUMBER}, ''))) > 0
      AND con.birth_date IS NOT NULL
      AND gpr.case_id IS NULL
;