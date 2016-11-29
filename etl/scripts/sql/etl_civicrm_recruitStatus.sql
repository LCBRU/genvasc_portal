SELECT
     gr.id AS genvasc_port_recruits_id
   , gr.source_system
   , CASE
    WHEN cs.name IS NOT NULL THEN cs.name
    WHEN ds.date_returned IS NOT NULL THEN 'Demographics Returned'
    WHEN ds.date_abandoned IS NOT NULL THEN 'Demographics Abandoned'
    WHEN ds.date_submitted IS NULL THEN 'Received'
    ELSE 'Awaiting Demographics'
    END AS status
   , gen.${CIVICRMDB_GENVASC_ID_NAME} AS study_id
   , gr.case_id
   , gr.contact_id
   , rel_c.display_name AS processed_by
FROM genvasc_portal_recruits gr
LEFT JOIN daps_submission_participant dp ON dp.id = gr.daps_submission_participant_id
LEFT JOIN daps_submission ds ON ds.id = dp.daps_submission_id
LEFT JOIN ${CIVICRMDB_CIVICRM_DATABASE}.civicrm_case cas ON cas.id = gr.case_id
                                           AND cas.is_deleted = 0
LEFT JOIN ${CIVICRMDB_CIVICRM_DATABASE}.civicrm_option_value cs ON cs.value = cas.status_id
                                                  AND cs.option_group_id = ${CIVICRMDB_CASE_STATUS_GROUP}
LEFT JOIN ${CIVICRMDB_CIVICRM_DATABASE}.${CIVICRMDB_GENVASC_DATA_TABLE} gen ON gen.entity_id = cas.id
LEFT JOIN ${CIVICRMDB_CIVICRM_DATABASE}.civicrm_relationship rel_r ON rel_r.case_id = cas.id
                                  AND rel_r.relationship_type_id = ${CIVICRMDB_RECRUITER_RELATIONSHIP_TYPE}
LEFT JOIN ${CIVICRMDB_CIVICRM_DATABASE}.civicrm_contact rel_c ON rel_c.id = rel_r.contact_id_b
;