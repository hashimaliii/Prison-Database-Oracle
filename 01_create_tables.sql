CREATE TABLE wing (
    wing_id        NUMBER(10) PRIMARY KEY,
    wing_name      VARCHAR2(50) NOT NULL UNIQUE,
    security_level VARCHAR2(20) CHECK (security_level IN ('Minimum', 'Medium', 'Maximum'))
);

CREATE TABLE cell (
    cell_id      NUMBER(10) PRIMARY KEY,
    max_capacity NUMBER(2) NOT NULL CHECK (max_capacity > 0),
    wing_id      NUMBER(10)
);

CREATE TABLE staff (
    staff_id     NUMBER(10) PRIMARY KEY,
    name         VARCHAR2(100) NOT NULL,
    contact_info VARCHAR2(50),
    hire_date    DATE DEFAULT SYSDATE
);

CREATE TABLE guard (
    staff_id     NUMBER(10) PRIMARY KEY,
    rank         VARCHAR2(30),
    shift_type   VARCHAR2(20),
    CONSTRAINT fk_guard_staff FOREIGN KEY (staff_id) REFERENCES staff(staff_id) ON DELETE CASCADE
);

CREATE TABLE professional (
    staff_id       NUMBER(10) PRIMARY KEY,
    specialty      VARCHAR2(50),
    license_number VARCHAR2(50) UNIQUE,
    CONSTRAINT fk_prof_staff FOREIGN KEY (staff_id) REFERENCES staff(staff_id) ON DELETE CASCADE
);

CREATE TABLE inmate (
    inmate_id      NUMBER(10) PRIMARY KEY,
    name           VARCHAR2(100) NOT NULL,
    nic            VARCHAR2(20) UNIQUE NOT NULL,
    admission_date DATE DEFAULT SYSDATE,
    release_date   DATE,
    security_class VARCHAR2(20),
    crime_category VARCHAR2(50),
    cell_id        NUMBER(10),
    CONSTRAINT chk_release_dates CHECK (release_date >= admission_date)
);

CREATE TABLE visitor (
    visitor_id   NUMBER(10) PRIMARY KEY,
    name         VARCHAR2(100) NOT NULL,
    nic          VARCHAR2(20) UNIQUE NOT NULL,
    relation_to_inmate VARCHAR2(50)
);

CREATE TABLE visitation_log (
    visitor_id      NUMBER(10),
    inmate_id       NUMBER(10),
    visit_start_time DATE,
    visit_end_time   DATE,
    purpose         VARCHAR2(255),
    CONSTRAINT pk_visitation_log PRIMARY KEY (visitor_id, inmate_id, visit_start_time)
);

CREATE TABLE incident_report (
    incident_id   NUMBER(10) PRIMARY KEY,
    description   VARCHAR2(500) NOT NULL,
    incident_date DATE DEFAULT SYSDATE,
    severity      NUMBER(1) CHECK (severity BETWEEN 1 AND 5),
    reporter_id   NUMBER(10)
);

CREATE TABLE medical_session (
    session_id   NUMBER(10) PRIMARY KEY,
    session_date DATE DEFAULT SYSDATE,
    notes        VARCHAR2(1000),
    staff_id     NUMBER(10),
    inmate_id    NUMBER(10)
);

COMMIT;