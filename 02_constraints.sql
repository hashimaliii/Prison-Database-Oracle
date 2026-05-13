ALTER TABLE cell ADD CONSTRAINT fk_cell_wing
    FOREIGN KEY (wing_id) REFERENCES wing(wing_id) ON DELETE SET NULL;

ALTER TABLE inmate ADD CONSTRAINT fk_inmate_cell
    FOREIGN KEY (cell_id) REFERENCES cell(cell_id) ON DELETE SET NULL;

ALTER TABLE incident_report ADD CONSTRAINT fk_incident_guard
    FOREIGN KEY (reporter_id) REFERENCES guard(staff_id) ON DELETE SET NULL;

ALTER TABLE medical_session ADD CONSTRAINT fk_med_prof
    FOREIGN KEY (staff_id) REFERENCES professional(staff_id) ON DELETE CASCADE;

ALTER TABLE medical_session ADD CONSTRAINT fk_med_inmate
    FOREIGN KEY (inmate_id) REFERENCES inmate(inmate_id) ON DELETE CASCADE;

ALTER TABLE visitation_log ADD CONSTRAINT fk_visit_visitor
    FOREIGN KEY (visitor_id) REFERENCES visitor(visitor_id) ON DELETE CASCADE;

ALTER TABLE visitation_log ADD CONSTRAINT fk_visit_inmate
    FOREIGN KEY (inmate_id) REFERENCES inmate(inmate_id) ON DELETE CASCADE;
COMMIT;