ALTER TABLE practice_registration
   	ADD user_id INTEGER NOT NULL,
	ADD CONSTRAINT fk_practice_registration_user FOREIGN KEY (user_id) REFERENCES user(id)
;

CREATE INDEX idx_practice_registration_user_id
ON practice_registration (user_id)
;