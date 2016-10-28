ALTER TABLE recruit
   	ADD daps_submission_id INTEGER NULL,
	ADD CONSTRAINT fk_recruit_daps_submission FOREIGN KEY (daps_submission_id) REFERENCES daps_submission(id)
;

CREATE INDEX idx_recruit_daps_submission_id
ON recruit (daps_submission_id)
;