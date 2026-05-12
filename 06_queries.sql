-- Phase 4: Required Query Categories
-- Author: Saleha Asghar & Zainab Saeed


-- 1. Basic SELECT with WHERE
-- Business Question: Retrieve all inmates currently assigned to high-security classification.
SELECT * FROM inmate
WHERE security_class = 'High';

-- 2. Aggregate Functions
-- Business Question: Calculate the total number of inmates currently housed in the facility.
SELECT COUNT(inmate_id) AS total_inmates FROM inmate;

-- 3. GROUP BY + HAVING
-- Business Question: List crime categories that have more than 2 inmates to identify high-risk groups.
SELECT crime_category, COUNT(*)
FROM inmate
GROUP BY crime_category
HAVING COUNT(*) > 2;

-- 4. INNER JOIN (2+ tables)
-- Business Question: Display a list of inmates alongside their assigned Wing names.
SELECT i.name AS inmate_name, w.wing_name
FROM inmate i
JOIN cell c ON i.cell_id = c.cell_id
JOIN wing w ON c.wing_id = w.wing_id;

-- 5. Outer JOIN
-- Business Question: Display all cells in the prison, including those that are currently empty.
SELECT c.cell_id, i.name AS inmate_name
FROM cell c
LEFT OUTER JOIN inmate i ON c.cell_id = i.cell_id;

-- 6. Subquery (non-correlated)
-- Business Question: Find names of inmates who were admitted after the very first inmate arrived.
SELECT name FROM inmate
WHERE admission_date > (SELECT MIN(admission_date) FROM inmate);

-- 7. Correlated Subquery
-- Business Question: Identify staff members who are specifically assigned to the 'Senior' guard rank.
SELECT s.name
FROM staff s
WHERE EXISTS (
    SELECT 1 FROM guard g
    WHERE g.staff_id = s.staff_id
    AND g.rank = 'Senior Warden'
);

-- 8. Multi-table JOIN (3+ tables)
-- Business Question: Generate a full audit trail showing which visitor met which inmate and in which wing.
SELECT v.name AS visitor, i.name AS inmate, w.wing_name
FROM visitor v
JOIN visitation_log vl ON v.visitor_id = vl.visitor_id
JOIN inmate i ON vl.inmate_id = i.inmate_id
JOIN cell c ON i.cell_id = c.cell_id
JOIN wing w ON c.wing_id = w.wing_id;

COMMIT;​