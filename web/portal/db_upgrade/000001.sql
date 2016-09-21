CREATE TABLE practice (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   name VARCHAR(500) NOT NULL
    ,   code VARCHAR(50) NOT NULL
    ,   date_created DATETIME NOT NULL
    )
;

CREATE UNIQUE INDEX idx_practice_name
ON practice (name)
;

CREATE UNIQUE INDEX idx_practice_code
ON practice (code)
;
