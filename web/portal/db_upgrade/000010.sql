CREATE TABLE etl_recruit_status (
        id VARCHAR(50) NOT NULL PRIMARY KEY
    ,	source_system VARCHAR(50) NOT NULL
    ,   status VARCHAR(100) NULL
    ,   study_id VARCHAR(100) NULL
    ,	first_name VARCHAR(100) NULL
    ,	last_name VARCHAR(100) NULL
    ,	civicrm_contact_id INT NULL
    ,	civicrm_case_id INT NULL
    ,   processed_by VARCHAR(500) NULL
    ,   processed_date DATE NULL
    )
;
