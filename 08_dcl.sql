-- Use these only if your environment allows creating new users
 CREATE USER prison_warden IDENTIFIED BY WardenPass2026;
 GRANT CONNECT, RESOURCE TO prison_warden;
 GRANT SELECT ON inmate TO prison_warden;

-- Demonstration of Revoke
REVOKE SELECT ON inmate FROM prison_warden;

COMMIT;