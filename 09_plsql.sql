CREATE OR REPLACE TRIGGER trg_check_cell_capacity
BEFORE INSERT ON inmate
FOR EACH ROW
DECLARE
    v_current_count NUMBER;
    v_max_capacity  NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_current_count FROM inmate WHERE cell_id = :NEW.cell_id;
    SELECT max_capacity INTO v_max_capacity FROM cell WHERE cell_id = :NEW.cell_id;
    IF v_current_count >= v_max_capacity THEN
        RAISE_APPLICATION_ERROR(-20001, 'Cell Capacity Reached');
    END IF;
END;
/