CREATE UNIQUE INDEX idx_visitor_nic ON visitor(nic);
CREATE INDEX idx_inmate_cell_fk ON inmate(cell_id);
CREATE INDEX idx_incident_severity ON incident_report(severity);

COMMIT;