INSERT INTO role(name, description)
VALUES ('admin', 'Administrators')
;

SET @adminRoleId = LAST_INSERT_ID()
;

INSERT INTO user(email, password, first_name, last_name, active, confirmed_at)
VALUES ('richard.a.bramley@uhl-tr.nhs.uk', '', 'Richard', 'Bramley', 1, CURDATE())
;

SET @richardUserId = LAST_INSERT_ID()
;

INSERT INTO roles_users(user_id, role_id)
VALUES (@richardUserId, @adminRoleId)
;

INSERT INTO user (email, password, first_name, last_name, active, confirmed_at)
VALUES ('lcbruit@uhl-tr.nhs.uk', '', 'System', 'User', 1, CURDATE())
;

SET @systemUserId = LAST_INSERT_ID()
;

INSERT INTO roles_users(user_id, role_id)
VALUES (@systemUserId, @adminRoleId)
;