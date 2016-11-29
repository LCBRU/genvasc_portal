CREATE TABLE etl_recruit_status (
        id CHAR(16) NOT NULL PRIMARY KEY
    ,	source_system VARCHAR(50) NOT NULL
    ,   status VARCHAR(100) NOT NULL
    ,   study_id VARCHAR(100) NOT NULL
    ,	civicrm_contact_id INT NULL
    ,	civicrm_case_id INT NULL
    ,   processed_by VARCHAR(500)
    )
;
