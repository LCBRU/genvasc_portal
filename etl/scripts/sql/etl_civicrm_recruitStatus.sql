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
   , gen.${CIVI_CUSCOL_GENVASC_ID} AS study_id
   , con.firat_name AS first_name
   , con.last_name AS last_name
   , gr.case_id
   , gr.contact_id
   , rel_c.display_name AS processed_by
   , rel_r.start_date AS processed_date
FROM genvasc_portal_recruits gr
LEFT JOIN daps_submission_participant dp ON dp.id = gr.daps_submission_participant_id
LEFT JOIN daps_submission ds ON ds.id = dp.daps_submission_id
LEFT JOIN ${CIVI_CIVIDB_NAME}.civicrm_case cas ON cas.id = gr.case_id
                                           AND cas.is_deleted = 0
LEFT JOIN ${CIVI_CIVIDB_NAME}.civicrm_case_contact cas_con ON cas_con.case_id = cas.case_id
LEFT JOIN ${CIVI_CIVIDB_NAME}.civicrm_contact con ON con.id = cas_con.contact_id
LEFT JOIN ${CIVI_CIVIDB_NAME}.civicrm_option_value cs ON cs.value = cas.status_id
                                                  AND cs.option_group_id = ${CIVI_CUSID_CASE_STATUS_GROUP}
LEFT JOIN ${CIVI_CIVIDB_NAME}.${CIVI_CUSTAB_GENVASC_DATA} gen ON gen.entity_id = cas.id
LEFT JOIN ${CIVI_CIVIDB_NAME}.civicrm_relationship rel_r ON rel_r.case_id = cas.id
                                  AND rel_r.relationship_type_id = ${CIVI_CUSID_RECRUITER_RELATIONSHIP_TYPE}
LEFT JOIN ${CIVI_CIVIDB_NAME}.civicrm_contact rel_c ON rel_c.id = rel_r.contact_id_b
;