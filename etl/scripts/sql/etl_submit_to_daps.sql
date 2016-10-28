INSERT INTO daps_submission (date_submitted)
VALUES (NOW())
;

SET @daps_submission_id = LAST_INSERT_ID();

UPDATE recruit
SET daps_submission_id = @daps_submission_id
WHERE daps_submission_id IS NULL
;

SELECT
      r.id AS recruit_id
    , r.nhs_number
    , r.date_of_birth
    , pr.code AS practice_code
FROM recruit r
JOIN practice_registration pr ON pr.id = r.practice_registration_id
WHERE daps_submission_id = @daps_submission_id
;