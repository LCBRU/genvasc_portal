CREATE TABLE etl_practice_details (
        id INTEGER PRIMARY KEY
    ,   name VARCHAR(500) NOT NULL
    ,   code VARCHAR(50) NOT NULL
	,   status VARCHAR(500)
	,	is_deleted BOOL
    )
;

CREATE UNIQUE INDEX idx_etl_practice_details_code
ON etl_practice_details (code)
;
