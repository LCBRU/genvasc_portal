SELECT
      r.id AS recruit_id
    , r.nhs_number
    , r.date_of_birth
    , pr.code AS practice_code
FROM recruit r
JOIN practice_registration pr ON pr.id = r.practice_registration_id
;