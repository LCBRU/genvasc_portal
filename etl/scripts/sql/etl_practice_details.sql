SELECT
      con.id AS id
    , gp.$COL_GP_CODE AS code
    , con.organization_name AS name
    , gp.$COL_GP_STATUS AS status
    , con.is_deleted AS is_deleted
FROM $TAB_GP_CUSTOM gp
JOIN civicrm_contact con ON con.id = gp.entity_id
;