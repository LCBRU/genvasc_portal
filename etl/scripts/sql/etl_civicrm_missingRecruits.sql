  SELECT
       UUID() AS id
     , 'CIVICRM' AS source_system
     , con.birth_date AS date_of_birth
     , cids.${CIVICRMDB_NHS_NUMBER_NAME} AS nhs_number
     , gpCustom.${CIVICRMDB_PRACTICE_CODE_NAME} AS practice_code
     , cas.start_date AS date_recruited
     , cas.id AS case_id
     , con.id AS contact_id
  FROM ${CIVICRMDB_CIVICRM_DATABASE}.civicrm_case cas
  JOIN ${CIVICRMDB_CIVICRM_DATABASE}.civicrm_case_contact cc ON cc.case_id = cas.id
  JOIN ${CIVICRMDB_CIVICRM_DATABASE}.civicrm_contact con ON con.id = cc.contact_id 
  JOIN ${CIVICRMDB_CIVICRM_DATABASE}.${CIVICRMDB_CONTACT_IDS_TABLE} cids ON cids.entity_id = con.id
  JOIN ${CIVICRMDB_CIVICRM_DATABASE}.civicrm_relationship practiceRel ON practiceRel.case_id = cas.id AND practiceRel.relationship_type_id = ${CIVICRMDB_PRACTICE_RELATIONSHIP_TYPE}
  JOIN ${CIVICRMDB_CIVICRM_DATABASE}.${CIVICRMDB_SURGERY_DATA_TABLE} gpCustom ON gpCustom.entity_id = practiceRel.contact_id_b
  WHERE cas.case_type_id = $CIVICRMDB_GENVASC_CASE_TYPE
      AND cas.id NOT IN (
        SELECT case_id
        FROM genvasc_portal_recruits
        WHERE case_id IS NOT NULL
        )
      AND LENGTH(TRIM(COALESCE(cids.${CIVICRMDB_NHS_NUMBER_NAME}, ''))) > 0
      AND con.birth_date IS NOT NULL
;