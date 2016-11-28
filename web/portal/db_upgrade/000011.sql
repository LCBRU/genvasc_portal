CREATE TABLE etl_missing_recruits (
        id CHAR(16) NOT NULL PRIMARY KEY
    ,	source_system VARCHAR(50) NOT NULL
    ,	date_of_birth DATE NULL
    ,	nhs_number VARCHAR(100) NULL
    ,	practice_code VARCHAR(100) NOT NULL
    ,   date_recruited DATE NOT NULL
    ,	civicrm_case_id INTEGER NOT NULL
    ,	civicrm_contact_id INTEGER NOT NULL
    )
;

CREATE UNIQUE INDEX idx_etl_missing_recruits_nhs_number_practice_code
ON etl_missing_recruits (nhs_number, practice_code)
;
