CREATE OR REPLACE VIEW view_wing_occupancy AS
SELECT w.wing_name, COUNT(i.inmate_id) AS current_inmates
FROM wing w
LEFT JOIN cell c ON w.wing_id = c.wing_id
LEFT JOIN inmate i ON c.cell_id = i.cell_id
GROUP BY w.wing_name;

CREATE OR REPLACE VIEW view_visitor_lookup AS
SELECT name, security_class FROM inmate;

CREATE OR REPLACE VIEW view_visitation_dashboard AS
SELECT v.name AS visitor, i.name AS inmate, vl.purpose
FROM visitor v
JOIN visitation_log vl ON v.visitor_id = vl.visitor_id
JOIN inmate i ON vl.inmate_id = i.inmate_id;

COMMIT;