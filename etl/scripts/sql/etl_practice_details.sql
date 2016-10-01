SELECT
      gp_con.id AS id
    , gp.$COL_GP_CODE AS code
    , gp_con.organization_name AS name
    , gp.$COL_GP_STATUS AS status
    , gp_con.is_deleted AS is_deleted
    , COALESCE(ccg_con.organization_name, '') AS ccg_name
FROM $TAB_GP_CUSTOM gp
JOIN civicrm_contact gp_con ON gp_con.id = gp.entity_id
LEFT JOIN civicrm_relationship ccg_rel ON  ccg_rel.contact_id_a = gp_con.id
                                  AND ccg_rel.relationship_type_id = $ID_CCG_RELATIONSHIP_TYPE
LEFT JOIN civicrm_contact ccg_con ON ccg_con.id = ccg_rel.contact_id_b
                                  AND ccg_con.is_deleted = 0
;