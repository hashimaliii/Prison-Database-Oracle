-- 1. Master/Lookup Tables (Wings and Cells)
INSERT INTO wing (wing_id, wing_name, security_level) VALUES (1, 'Alpha Block', 'Maximum');
INSERT INTO wing (wing_id, wing_name, security_level) VALUES (2, 'Beta Block', 'Medium');
INSERT INTO wing (wing_id, wing_name, security_level) VALUES (3, 'Gamma Ward', 'Minimum');

INSERT INTO cell (cell_id, max_capacity, wing_id) VALUES (101, 2, 1);
INSERT INTO cell (cell_id, max_capacity, wing_id) VALUES (102, 4, 2);
INSERT INTO cell (cell_id, max_capacity, wing_id) VALUES (103, 1, 1);
INSERT INTO cell (cell_id, max_capacity, wing_id) VALUES (104, 5, 3);
INSERT INTO cell (cell_id, max_capacity, wing_id) VALUES (105, 5, 3);

-- 2. Visitors (Requirement: 5-10 rows)
INSERT INTO visitor (visitor_id, name, nic, relation_to_inmate) VALUES (1, 'Sajid Khan', '33102-1111111-1', 'Brother');
INSERT INTO visitor (visitor_id, name, nic, relation_to_inmate) VALUES (2, 'Bilal Khan', '33102-2222222-2', 'Lawyer');
INSERT INTO visitor (visitor_id, name, nic, relation_to_inmate) VALUES (3, 'Hamza Ali', '33102-3333333-3', 'Father');
INSERT INTO visitor (visitor_id, name, nic, relation_to_inmate) VALUES (4, 'Faisal Rizwan', '33102-4444444-4', 'Cousin');
INSERT INTO visitor (visitor_id, name, nic, relation_to_inmate) VALUES (5, 'Zubair Jameel', '33102-5555555-5', 'Friend');
INSERT INTO visitor (visitor_id, name, nic, relation_to_inmate) VALUES (6, 'Kashif Anwar', '33102-6666666-6', 'Legal Counsel');

-- 3. Inmates (Requirement: 15-20 rows)
INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
VALUES (inmate_seq.NEXTVAL, 'Ahmed Hassan', '33102-1234567-1', TO_DATE('2024-01-15', 'YYYY-MM-DD'), 'High', 'Felony', 101);
INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
VALUES (inmate_seq.NEXTVAL, 'Zain Ul Abidin', '33102-7654321-2', TO_DATE('2025-02-10', 'YYYY-MM-DD'), 'Low', 'Misdemeanor', 102);
INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
VALUES (inmate_seq.NEXTVAL, 'Muhammad Ali', '33102-1112223-3', TO_DATE('2023-05-12', 'YYYY-MM-DD'), 'High', 'Robbery', 101);
INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
VALUES (inmate_seq.NEXTVAL, 'Umar Farooq', '33102-4445556-6', TO_DATE('2024-08-20', 'YYYY-MM-DD'), 'Medium', 'Fraud', 102);
INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
VALUES (inmate_seq.NEXTVAL, 'Hamza Shehbaz', '33102-7778889-9', TO_DATE('2025-01-05', 'YYYY-MM-DD'), 'Low', 'Trespassing', 103);
INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
VALUES (inmate_seq.NEXTVAL, 'Bilal Ahmed', '33102-1212121-1', TO_DATE('2024-11-30', 'YYYY-MM-DD'), 'High', 'Assault', 104);
INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
VALUES (inmate_seq.NEXTVAL, 'Usman Tariq', '33102-3434343-4', TO_DATE('2023-12-15', 'YYYY-MM-DD'), 'Medium', 'Theft', 104);
INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
VALUES (inmate_seq.NEXTVAL, 'Zubair Shah', '33102-1231234-5', TO_DATE('2024-03-10', 'YYYY-MM-DD'), 'High', 'Burglary', 101);
INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
VALUES (inmate_seq.NEXTVAL, 'Irfan Junejo', '33102-5554443-2', TO_DATE('2025-01-20', 'YYYY-MM-DD'), 'Medium', 'Cybercrime', 105);
INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
VALUES (inmate_seq.NEXTVAL, 'Murtaza Javed', '33102-9876543-1', TO_DATE('2023-11-11', 'YYYY-MM-DD'), 'Low', 'Vandalism', 105);
INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
VALUES (inmate_seq.NEXTVAL, 'Salman Khan', '33102-0000001-1', TO_DATE('2024-06-01', 'YYYY-MM-DD'), 'Medium', 'Theft', 102);
INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
VALUES (inmate_seq.NEXTVAL, 'Asad Ullah', '33102-0000002-2', TO_DATE('2024-07-15', 'YYYY-MM-DD'), 'High', 'Assault', 101);
INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
VALUES (inmate_seq.NEXTVAL, 'Riaz Ahmed', '33102-0000003-3', TO_DATE('2023-09-10', 'YYYY-MM-DD'), 'Low', 'Trespassing', 103);
INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
VALUES (inmate_seq.NEXTVAL, 'Qasim Ali', '33102-0000004-4', TO_DATE('2025-03-05', 'YYYY-MM-DD'), 'Medium', 'Fraud', 102);
INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
VALUES (inmate_seq.NEXTVAL, 'Faizan Malik', '33102-0000005-5', TO_DATE('2024-12-25', 'YYYY-MM-DD'), 'High', 'Robbery', 101);
INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
VALUES (inmate_seq.NEXTVAL, 'Hassan Raza', '33102-0000006-6', TO_DATE('2024-02-14', 'YYYY-MM-DD'), 'Low', 'Vandalism', 105);
INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
VALUES (inmate_seq.NEXTVAL, 'Abid Hussain', '33102-0000007-7', TO_DATE('2023-10-30', 'YYYY-MM-DD'), 'Medium', 'Burglary', 104);
INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
VALUES (inmate_seq.NEXTVAL, 'Imran Khan', '33102-0000008-8', TO_DATE('2024-05-20', 'YYYY-MM-DD'), 'High', 'Cybercrime', 101);
INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
VALUES (inmate_seq.NEXTVAL, 'Shahid Afridi', '33102-0000009-9', TO_DATE('2025-04-12', 'YYYY-MM-DD'), 'Low', 'Trespassing', 105);
INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
VALUES (inmate_seq.NEXTVAL, 'Babar Azam', '33102-0000010-0', TO_DATE('2024-08-01', 'YYYY-MM-DD'), 'Medium', 'Theft', 102);


INSERT INTO visitation_log (visitor_id, inmate_id, visit_start_time, visit_end_time, purpose)
VALUES (1, 100, TO_DATE('2026-05-14 10:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-14 11:00', 'YYYY-MM-DD HH24:MI'), 'Monthly Family Visit');
INSERT INTO visitation_log (visitor_id, inmate_id, visit_start_time, visit_end_time, purpose)
VALUES (2, 101, TO_DATE('2026-05-14 11:30', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-14 12:30', 'YYYY-MM-DD HH24:MI'), 'Legal Aid');
INSERT INTO visitation_log (visitor_id, inmate_id, visit_start_time, visit_end_time, purpose)
VALUES (3, 102, TO_DATE('2026-05-15 09:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-15 10:00', 'YYYY-MM-DD HH24:MI'), 'Personal Matter');
INSERT INTO visitation_log VALUES (4, 103, TO_DATE('2026-05-15 14:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-15 15:00', 'YYYY-MM-DD HH24:MI'), 'Family Support');
INSERT INTO visitation_log VALUES (5, 104, TO_DATE('2026-05-16 10:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-16 11:00', 'YYYY-MM-DD HH24:MI'), 'Medical Update');
INSERT INTO visitation_log VALUES (6, 105, TO_DATE('2026-05-16 13:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-16 14:00', 'YYYY-MM-DD HH24:MI'), 'Counseling');
INSERT INTO visitation_log VALUES (1, 106, TO_DATE('2026-05-17 08:30', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-17 09:30', 'YYYY-MM-DD HH24:MI'), 'Brotherly Visit');
INSERT INTO visitation_log VALUES (2, 107, TO_DATE('2026-05-17 11:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-17 12:00', 'YYYY-MM-DD HH24:MI'), 'Bail Consultation');
INSERT INTO visitation_log VALUES (3, 108, TO_DATE('2026-05-18 15:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-18 16:00', 'YYYY-MM-DD HH24:MI'), 'Social Call');
INSERT INTO visitation_log VALUES (4, 109, TO_DATE('2026-05-19 10:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-19 11:00', 'YYYY-MM-DD HH24:MI'), 'General Visit');
INSERT INTO visitation_log VALUES (5, 110, TO_DATE('2026-05-19 12:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-19 13:00', 'YYYY-MM-DD HH24:MI'), 'Welfare Check');
INSERT INTO visitation_log VALUES (6, 111, TO_DATE('2026-05-20 09:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-20 10:00', 'YYYY-MM-DD HH24:MI'), 'Family Case');
INSERT INTO visitation_log VALUES (1, 112, TO_DATE('2026-05-20 14:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-20 15:00', 'YYYY-MM-DD HH24:MI'), 'Personal Consultation');
INSERT INTO visitation_log VALUES (2, 113, TO_DATE('2026-05-21 10:30', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-21 11:30', 'YYYY-MM-DD HH24:MI'), 'Legal Update');
INSERT INTO visitation_log VALUES (3, 114, TO_DATE('2026-05-21 13:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-21 14:00', 'YYYY-MM-DD HH24:MI'), 'Property Discussion');
INSERT INTO visitation_log VALUES (4, 115, TO_DATE('2026-05-22 09:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-22 10:00', 'YYYY-MM-DD HH24:MI'), 'Parental Visit');
INSERT INTO visitation_log VALUES (5, 116, TO_DATE('2026-05-22 11:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-22 12:00', 'YYYY-MM-DD HH24:MI'), 'Routine Check');
INSERT INTO visitation_log VALUES (6, 117, TO_DATE('2026-05-23 15:30', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-23 16:30', 'YYYY-MM-DD HH24:MI'), 'Final Discussion');
INSERT INTO visitation_log VALUES (1, 118, TO_DATE('2026-05-24 10:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-24 11:00', 'YYYY-MM-DD HH24:MI'), 'Regular Visit');
INSERT INTO visitation_log VALUES (2, 119, TO_DATE('2026-05-24 12:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-24 13:00', 'YYYY-MM-DD HH24:MI'), 'Legal Paperwork');
INSERT INTO visitation_log VALUES (3, 100, TO_DATE('2026-05-25 09:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-25 10:00', 'YYYY-MM-DD HH24:MI'), 'Emergency Visit');
INSERT INTO visitation_log VALUES (4, 101, TO_DATE('2026-05-25 11:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-25 12:00', 'YYYY-MM-DD HH24:MI'), 'Health Discussion');
INSERT INTO visitation_log VALUES (5, 102, TO_DATE('2026-05-26 14:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-26 15:00', 'YYYY-MM-DD HH24:MI'), 'Case Review');
INSERT INTO visitation_log VALUES (6, 103, TO_DATE('2026-05-26 15:30', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-26 16:30', 'YYYY-MM-DD HH24:MI'), 'Financial Matter');
INSERT INTO visitation_log VALUES (1, 104, TO_DATE('2026-05-27 10:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-27 11:00', 'YYYY-MM-DD HH24:MI'), 'Child Support');
INSERT INTO visitation_log VALUES (2, 105, TO_DATE('2026-05-27 13:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-27 14:00', 'YYYY-MM-DD HH24:MI'), 'Bail Discussion');
INSERT INTO visitation_log VALUES (3, 106, TO_DATE('2026-05-28 09:30', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-28 10:30', 'YYYY-MM-DD HH24:MI'), 'Spousal Visit');
INSERT INTO visitation_log VALUES (4, 107, TO_DATE('2026-05-28 11:30', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-28 12:30', 'YYYY-MM-DD HH24:MI'), 'Inheritance Law');
INSERT INTO visitation_log VALUES (5, 108, TO_DATE('2026-05-29 15:00', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-29 16:00', 'YYYY-MM-DD HH24:MI'), 'Property Case');
INSERT INTO visitation_log VALUES (6, 109, TO_DATE('2026-05-29 16:30', 'YYYY-MM-DD HH24:MI'), TO_DATE('2026-05-29 17:30', 'YYYY-MM-DD HH24:MI'), 'Final Appeal Check');

-- First, insert into the Parent table (staff)
INSERT INTO staff (staff_id, name, contact_info) VALUES (staff_seq.NEXTVAL, 'Major Arshad', '0300-1112223');
INSERT INTO staff (staff_id, name, contact_info) VALUES (staff_seq.NEXTVAL, 'Officer Kamran', '0300-7778889');
INSERT INTO staff (staff_id, name, contact_info) VALUES (staff_seq.NEXTVAL, 'Dr. Sarah Ahmed', '0300-4445556');
INSERT INTO staff (staff_id, name, contact_info) VALUES (staff_seq.NEXTVAL, 'Officer Zaid', '0321-9990001');   
INSERT INTO staff (staff_id, name, contact_info) VALUES (staff_seq.NEXTVAL, 'Major Bilal', '0321-8887776');  

-- Second, insert into the Sub-entity tables using those specific IDs
-- Guards
INSERT INTO guard (staff_id, rank, shift_type) VALUES (500, 'Senior Warden', 'Morning');
INSERT INTO guard (staff_id, rank, shift_type) VALUES (501, 'Patrol Officer', 'Night');
INSERT INTO guard (staff_id, rank, shift_type) VALUES (503, 'Senior Guard', 'Morning');
INSERT INTO guard (staff_id, rank, shift_type) VALUES (504, 'Senior Warden', 'Night');

-- Professionals (Doctors/Psychiatrists)
INSERT INTO professional (staff_id, specialty, license_number) VALUES (502, 'General Physician', 'PMDC-99887');

COMMIT;​