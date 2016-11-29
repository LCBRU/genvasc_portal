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
   , gen.genvasc_id_30 AS study_id
   , gr.case_id
   , gr.contact_id
   , rel_c.display_name AS processed_by
FROM genvasc_portal_recruits gr
LEFT JOIN daps_submission_participant dp ON dp.id = gr.daps_submission_participant_id
LEFT JOIN daps_submission ds ON ds.id = dp.daps_submission_id
LEFT JOIN richdev_civicrm.civicrm_case cas ON cas.id = gr.case_id
                                           AND cas.is_deleted = 0
LEFT JOIN richdev_civicrm.civicrm_option_value cs ON cs.value = cas.status_id
                                                  AND cs.option_group_id = 27
LEFT JOIN richdev_civicrm.civicrm_value_genvasc_recruitment_data_8 gen ON gen.entity_id = cas.id
LEFT JOIN richdev_civicrm.civicrm_relationship rel_r ON rel_r.case_id = cas.id
                                  AND rel_r.relationship_type_id = 19
LEFT JOIN richdev_civicrm.civicrm_contact rel_c ON rel_c.id = rel_r.contact_id_b
;