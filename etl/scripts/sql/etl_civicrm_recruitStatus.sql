  SELECT
       gr.id AS genvasc_port_recruits_id
     , gr.source_system
     , CASE
      WHEN cs.name IS NOT NULL THEN cs.name
      ELSE 'Awaiting processing'
      END AS status
     , gr.nhs_number
     , gen.${CIVI_CUSCOL_GENVASC_ID} AS study_id
     , gr.practice_code
     , con.first_name AS first_name
     , con.last_name AS last_name
     , con.birth_date AS date_of_birth
     , gr.case_id
     , gr.contact_id
     , rel_c.display_name AS processed_by
     , rel_r.start_date AS processed_date
     , gr.date_recruited
  FROM genvasc_portal_recruits gr
  LEFT JOIN daps_submission_participant dp ON dp.id = gr.daps_submission_participant_id
  LEFT JOIN daps_submission ds ON ds.id = dp.daps_submission_id
  LEFT JOIN ${CIVI_CIVIDB_NAME}.civicrm_case cas ON cas.id = gr.case_id
                                             AND cas.is_deleted = 0
  LEFT JOIN ${CIVI_CIVIDB_NAME}.civicrm_case_contact cas_con ON cas_con.case_id = cas.id
  LEFT JOIN ${CIVI_CIVIDB_NAME}.civicrm_contact con ON con.id = cas_con.contact_id
  LEFT JOIN ${CIVI_CIVIDB_NAME}.civicrm_option_value cs ON cs.value = cas.status_id
                                                    AND cs.option_group_id = ${CIVI_CUSID_CASE_STATUS_GROUP}
  LEFT JOIN ${CIVI_CIVIDB_NAME}.${CIVI_CUSTAB_GENVASC_DATA} gen ON gen.entity_id = cas.id
  LEFT JOIN ${CIVI_CIVIDB_NAME}.civicrm_relationship rel_r ON rel_r.case_id = cas.id
                                    AND rel_r.relationship_type_id = ${CIVI_CUSID_RECRUITER_RELATIONSHIP_TYPE}
  LEFT JOIN ${CIVI_CIVIDB_NAME}.civicrm_contact rel_c ON rel_c.id = rel_r.contact_id_b


UNION


  SELECT
       UUID() AS id
     , 'CIVICRM' AS source_system
     , CASE
      WHEN cs.name IS NOT NULL THEN cs.name
      ELSE 'Awaiting processing'
      END AS status
     , cids.${CIVI_CUSCOL_NHS_NUMBER} AS nhs_number
     , gen.${CIVI_CUSCOL_GENVASC_ID} AS study_id
     , gpCustom.${CIVI_CUSCOL_PRACTICE_CODE} AS practice_code
     , con.first_name AS first_name
     , con.last_name AS last_name
     , con.birth_date AS date_of_birth
     , cas.id AS case_id
     , con.id AS contact_id
     , rel_c.display_name AS processed_by
     , rel_r.start_date AS processed_date
     , cas.start_date AS date_recruited
  FROM ${CIVI_CIVIDB_NAME}.civicrm_case cas
  LEFT JOIN ${CIVI_CIVIDB_NAME}.civicrm_option_value cs ON cs.value = cas.status_id
                                                      AND cs.option_group_id = ${CIVI_CUSID_CASE_STATUS_GROUP}
  JOIN ${CIVI_CIVIDB_NAME}.civicrm_case_contact cc ON cc.case_id = cas.id
  JOIN ${CIVI_CIVIDB_NAME}.civicrm_contact con ON con.id = cc.contact_id 
  JOIN ${CIVI_CIVIDB_NAME}.${CIVI_CUSTAB_CONTACT} cids ON cids.entity_id = con.id
  JOIN ${CIVI_CIVIDB_NAME}.civicrm_relationship practiceRel ON practiceRel.case_id = cas.id AND practiceRel.relationship_type_id = ${CIVI_CUSID_PRACTICE_RELATIONSHIP_TYPE}
  JOIN ${CIVI_CIVIDB_NAME}.${CIVI_CUSTAB_SURGERY} gpCustom ON gpCustom.entity_id = practiceRel.contact_id_b
  LEFT JOIN ${CIVI_CIVIDB_NAME}.${CIVI_CUSTAB_GENVASC_DATA} gen ON gen.entity_id = cas.id
  LEFT JOIN genvasc_portal_recruits gpr ON gpr.case_id = cas.id
  LEFT JOIN ${CIVI_CIVIDB_NAME}.civicrm_relationship rel_r ON rel_r.case_id = cas.id
                                    AND rel_r.relationship_type_id = ${CIVI_CUSID_RECRUITER_RELATIONSHIP_TYPE}
  LEFT JOIN ${CIVI_CIVIDB_NAME}.civicrm_contact rel_c ON rel_c.id = rel_r.contact_id_b
  WHERE cas.case_type_id = ${CIVI_CUSID_GENVASC_CASE_TYPE}
      AND LENGTH(TRIM(COALESCE(cids.${CIVI_CUSCOL_NHS_NUMBER}, ''))) > 0
      AND con.birth_date IS NOT NULL
      AND gpr.case_id IS NULL
;