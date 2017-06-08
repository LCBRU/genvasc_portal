SELECT DISTINCT
  SUBSTRING_INDEX(pc.value, '(', 1) AS practice_code,
  TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(d.value, ';', numbers.n), ';', -1)) email_address
FROM (
    select 1 n union all
   select 2 union all
    select 3 union all
   select 4 union all
    select 5
    ) numbers
INNER JOIN redcap6170_briccs.redcap_data d
    ON (CHAR_LENGTH(d.value) - CHAR_LENGTH(REPLACE(d.value, ';', ''))) >= (numbers.n - 1)
    AND d.project_id = 41
    AND d.field_name IN ('practice_manager_email', 'prim_contact_email_add', 'sec_contact_email_add', 'thrd_contact_email_add', 'frth_contact_email_add')
INNER JOIN redcap6170_briccs.redcap_data pc
    ON pc.project_id = d.project_id
    AND pc.field_name = 'practice_code'
    AND pc.record = d.record
WHERE LENGTH(TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(d.value, ';', numbers.n), ';', -1))) > 1

UNION

SELECT DISTINCT
  SUBSTRING_INDEX(pc.value, '(', 1) AS practice_code,
  TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(d.value, ';', numbers.n), ';', -1)) email_address
FROM (
    select 1 n union all
   select 2 union all
    select 3 union all
   select 4 union all
    select 5
    ) numbers
INNER JOIN redcap6170_briccsext.redcap_data d
    ON (CHAR_LENGTH(d.value) - CHAR_LENGTH(REPLACE(d.value, ';', ''))) >= (numbers.n - 1)
    AND d.project_id = 29
    AND d.field_name IN ('practice_manager_email', 'prim_contact_email_add', 'sec_contact_email_add', 'thrd_contact_email_add')
INNER JOIN redcap6170_briccsext.redcap_data pc
    ON pc.project_id = d.project_id
    AND pc.field_name = 'practice_code'
    AND pc.record = d.record
WHERE LENGTH(TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(d.value, ';', numbers.n), ';', -1))) > 1
