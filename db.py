import oracledb
from werkzeug.security import check_password_hash

# Database Configuration
DB_USER = "HR"
DB_PASSWORD = "123"
DB_DSN = "localhost:1521/xe"

try:
    oracledb.init_oracle_client(lib_dir=r"C:\oraclexe\app\oracle\product\11.2.0\server\bin")
except Exception:
    pass

def get_connection():
    try:
        return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
    except oracledb.DatabaseError as e:
        print(f"Database connection error: {e}")
        return None

def test_connection():
    conn = get_connection()
    if conn:
        conn.close()
        return True
    return False

def verify_login(username, password):
    if username == 'admin' and password == 'admin123':
        return True
    return False

def get_dashboard_stats():
    conn = get_connection()
    if not conn: return {"total_inmates": 0, "total_staff": 0, "total_incidents": 0, "available_cells": 0}
    cursor = conn.cursor()
    stats = {}
    try:
        cursor.execute("SELECT COUNT(*) FROM inmate")
        stats['total_inmates'] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM staff")
        stats['total_staff'] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM incident_report")
        stats['total_incidents'] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM cell WHERE max_capacity > (SELECT COUNT(*) FROM inmate WHERE inmate.cell_id = cell.cell_id)")
        stats['available_cells'] = cursor.fetchone()[0]
        return stats
    except oracledb.DatabaseError:
        return {"total_inmates": 0, "total_staff": 0, "total_incidents": 0, "available_cells": 0}
    finally:
        cursor.close()
        conn.close()

# ==========================================
# INMATES
# ==========================================
def get_all_inmates():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        query = """
            SELECT i.inmate_id, i.name, i.nic, i.admission_date, i.release_date, i.security_class, i.crime_category, c.cell_id, w.wing_name
            FROM inmate i
            LEFT JOIN cell c ON i.cell_id = c.cell_id
            LEFT JOIN wing w ON c.wing_id = w.wing_id
            ORDER BY i.inmate_id
        """
        cursor.execute(query)
        columns = [col[0].lower() for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except oracledb.DatabaseError:
        return []
    finally:
        cursor.close()
        conn.close()

def add_inmate(data):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO inmate (inmate_id, name, nic, admission_date, release_date, security_class, crime_category, cell_id)
            VALUES (inmate_seq.NEXTVAL, :name, :nic, TO_DATE(:admission_date, 'YYYY-MM-DD'), 
                    CASE WHEN :release_date IS NOT NULL THEN TO_DATE(:release_date, 'YYYY-MM-DD') ELSE NULL END, 
                    :security_class, :crime_category, :cell_id)
        """, {
            'name': data['name'], 
            'nic': data['nic'], 
            'admission_date': data['admission_date'], 
            'release_date': data.get('release_date') or None, 
            'security_class': data['security_class'], 
            'crime_category': data['crime_category'], 
            'cell_id': data['cell_id']
        })
        conn.commit()
        return True, "Inmate added."
    except oracledb.DatabaseError as e:
        return False, e.args[0].message
    finally:
        cursor.close()
        conn.close()

def update_inmate(inmate_id, data):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE inmate SET name=:name, nic=:nic, 
            admission_date=TO_DATE(:admission_date, 'YYYY-MM-DD'),
            release_date=CASE WHEN :release_date IS NOT NULL THEN TO_DATE(:release_date, 'YYYY-MM-DD') ELSE NULL END,
            security_class=:security_class, crime_category=:crime_category, cell_id=:cell_id
            WHERE inmate_id = :id
        """, {
            'name': data['name'], 
            'nic': data['nic'], 
            'admission_date': data['admission_date'], 
            'release_date': data.get('release_date') or None, 
            'security_class': data['security_class'], 
            'crime_category': data['crime_category'], 
            'cell_id': data['cell_id'], 
            'id': inmate_id
        })
        conn.commit()
        return True, "Inmate updated."
    except oracledb.DatabaseError as e:
        return False, e.args[0].message
    finally:
        cursor.close()
        conn.close()

def delete_inmate(inmate_id):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM inmate WHERE inmate_id = :1", (inmate_id,))
        conn.commit()
        return True, "Inmate deleted."
    except oracledb.DatabaseError as e:
        return False, f"Cannot delete inmate: {e.args[0].message}"
    finally:
        cursor.close()
        conn.close()

# ==========================================
# STAFF
# ==========================================
def get_all_staff():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        query = """
            SELECT s.staff_id, s.name, s.contact_info, s.hire_date, 
                   g.rank, g.shift_type,
                   p.specialty, p.license_number
            FROM staff s
            LEFT JOIN guard g ON s.staff_id = g.staff_id
            LEFT JOIN professional p ON s.staff_id = p.staff_id
            ORDER BY s.staff_id
        """
        cursor.execute(query)
        columns = [col[0].lower() for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except oracledb.DatabaseError:
        return []
    finally:
        cursor.close()
        conn.close()

def add_staff(data):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT NVL(MAX(staff_id), 0) + 1 FROM staff")
        new_id = cursor.fetchone()[0]
        
        cursor.execute("INSERT INTO staff (staff_id, name, contact_info, hire_date) VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'))",
                       (new_id, data['name'], data['contact_info'], data['hire_date']))
        
        if data['staff_type'] == 'guard':
            cursor.execute("INSERT INTO guard (staff_id, rank, shift_type) VALUES (:1, :2, :3)", (new_id, data['rank'], data['shift_type']))
        elif data['staff_type'] == 'professional':
            cursor.execute("INSERT INTO professional (staff_id, specialty, license_number) VALUES (:1, :2, :3)", (new_id, data['specialty'], data['license_number']))
            
        conn.commit()
        return True, "Staff added."
    except oracledb.DatabaseError as e:
        return False, e.args[0].message
    finally:
        cursor.close()
        conn.close()

def update_staff(staff_id, data):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE staff SET name=:1, contact_info=:2, hire_date=TO_DATE(:3, 'YYYY-MM-DD') WHERE staff_id=:4",
                       (data['name'], data['contact_info'], data['hire_date'], staff_id))
        
        if data['staff_type'] == 'guard':
            # Check if exists, else insert
            cursor.execute("SELECT COUNT(*) FROM guard WHERE staff_id = :1", (staff_id,))
            if cursor.fetchone()[0] > 0:
                cursor.execute("UPDATE guard SET rank=:1, shift_type=:2 WHERE staff_id=:3", (data['rank'], data['shift_type'], staff_id))
            else:
                cursor.execute("INSERT INTO guard (staff_id, rank, shift_type) VALUES (:1, :2, :3)", (staff_id, data['rank'], data['shift_type']))
            cursor.execute("DELETE FROM professional WHERE staff_id=:1", (staff_id,))
            
        elif data['staff_type'] == 'professional':
            cursor.execute("SELECT COUNT(*) FROM professional WHERE staff_id = :1", (staff_id,))
            if cursor.fetchone()[0] > 0:
                cursor.execute("UPDATE professional SET specialty=:1, license_number=:2 WHERE staff_id=:3", (data['specialty'], data['license_number'], staff_id))
            else:
                cursor.execute("INSERT INTO professional (staff_id, specialty, license_number) VALUES (:1, :2, :3)", (staff_id, data['specialty'], data['license_number']))
            cursor.execute("DELETE FROM guard WHERE staff_id=:1", (staff_id,))
            
        conn.commit()
        return True, "Staff updated."
    except oracledb.DatabaseError as e:
        return False, e.args[0].message
    finally:
        cursor.close()
        conn.close()

def delete_staff(staff_id):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM guard WHERE staff_id = :1", (staff_id,))
        cursor.execute("DELETE FROM professional WHERE staff_id = :1", (staff_id,))
        cursor.execute("DELETE FROM staff WHERE staff_id = :1", (staff_id,))
        conn.commit()
        return True, "Staff deleted."
    except oracledb.DatabaseError as e:
        return False, f"Cannot delete staff: {e.args[0].message}"
    finally:
        cursor.close()
        conn.close()

# ==========================================
# VISITORS
# ==========================================
def get_all_visitors():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM visitor ORDER BY visitor_id")
        columns = [col[0].lower() for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except oracledb.DatabaseError:
        return []
    finally:
        cursor.close()
        conn.close()

def add_visitor(data):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT NVL(MAX(visitor_id), 0) + 1 FROM visitor")
        new_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO visitor (visitor_id, name, nic, relation_to_inmate) VALUES (:1, :2, :3, :4)", 
                       (new_id, data['name'], data['nic'], data['relation_to_inmate']))
        conn.commit()
        return True, "Visitor added."
    except oracledb.DatabaseError as e:
        return False, e.args[0].message
    finally:
        cursor.close()
        conn.close()

def update_visitor(visitor_id, data):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE visitor SET name=:1, nic=:2, relation_to_inmate=:3 WHERE visitor_id=:4", 
                       (data['name'], data['nic'], data['relation_to_inmate'], visitor_id))
        conn.commit()
        return True, "Visitor updated."
    except oracledb.DatabaseError as e:
        return False, e.args[0].message
    finally:
        cursor.close()
        conn.close()

def delete_visitor(visitor_id):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM visitor WHERE visitor_id = :1", (visitor_id,))
        conn.commit()
        return True, "Visitor deleted."
    except oracledb.DatabaseError as e:
        return False, f"Cannot delete visitor: {e.args[0].message}"
    finally:
        cursor.close()
        conn.close()

# ==========================================
# VISITATION LOGS
# ==========================================
def get_visitation_logs():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        query = """
            SELECT vl.visitor_id, vl.inmate_id, vl.visit_start_time, vl.visit_end_time, vl.purpose,
                   v.name as visitor_name, i.name as inmate_name
            FROM visitation_log vl
            JOIN visitor v ON vl.visitor_id = v.visitor_id
            JOIN inmate i ON vl.inmate_id = i.inmate_id
            ORDER BY vl.visit_start_time DESC
        """
        cursor.execute(query)
        columns = [col[0].lower() for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except oracledb.DatabaseError:
        return []
    finally:
        cursor.close()
        conn.close()

def log_visitation(data):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO visitation_log (visitor_id, inmate_id, visit_start_time, visit_end_time, purpose) VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD HH24:MI'), TO_DATE(:4, 'YYYY-MM-DD HH24:MI'), :5)", 
                       (data['visitor_id'], data['inmate_id'], data['visit_start_time'], data['visit_end_time'], data['purpose']))
        conn.commit()
        return True, "Visitation log recorded."
    except oracledb.DatabaseError as e:
        return False, e.args[0].message
    finally:
        cursor.close()
        conn.close()

def update_visitation_log(visitor_id, inmate_id, old_start_time, data):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE visitation_log SET visit_end_time=TO_DATE(:1, 'YYYY-MM-DD HH24:MI'), purpose=:2 
            WHERE visitor_id=:3 AND inmate_id=:4 AND visit_start_time=TO_DATE(:5, 'YYYY-MM-DD HH24:MI:SS')
        """, (data['visit_end_time'], data['purpose'], visitor_id, inmate_id, old_start_time))
        conn.commit()
        return True, "Visitation log updated."
    except oracledb.DatabaseError as e:
        return False, e.args[0].message
    finally:
        cursor.close()
        conn.close()

def delete_visitation_log(visitor_id, inmate_id, start_time):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM visitation_log WHERE visitor_id=:1 AND inmate_id=:2 AND visit_start_time=TO_DATE(:3, 'YYYY-MM-DD HH24:MI:SS')", 
                       (visitor_id, inmate_id, start_time))
        conn.commit()
        return True, "Visitation log deleted."
    except oracledb.DatabaseError as e:
        return False, e.args[0].message
    finally:
        cursor.close()
        conn.close()

# ==========================================
# INCIDENTS
# ==========================================
def get_all_incidents():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        query = """
            SELECT ir.incident_id, ir.description, ir.incident_date, ir.severity, ir.reporter_id, s.name as reporter_name
            FROM incident_report ir
            LEFT JOIN staff s ON ir.reporter_id = s.staff_id
            ORDER BY ir.incident_date DESC
        """
        cursor.execute(query)
        columns = [col[0].lower() for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except oracledb.DatabaseError:
        return []
    finally:
        cursor.close()
        conn.close()

def add_incident(data):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT NVL(MAX(incident_id), 0) + 1 FROM incident_report")
        new_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO incident_report (incident_id, description, incident_date, severity, reporter_id) VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4, :5)", 
                       (new_id, data['description'], data['incident_date'], data['severity'], data['reporter_id']))
        conn.commit()
        return True, "Incident added."
    except oracledb.DatabaseError as e:
        return False, e.args[0].message
    finally:
        cursor.close()
        conn.close()

def update_incident(incident_id, data):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE incident_report SET description=:1, incident_date=TO_DATE(:2, 'YYYY-MM-DD'), severity=:3, reporter_id=:4 WHERE incident_id=:5", 
                       (data['description'], data['incident_date'], data['severity'], data['reporter_id'], incident_id))
        conn.commit()
        return True, "Incident updated."
    except oracledb.DatabaseError as e:
        return False, e.args[0].message
    finally:
        cursor.close()
        conn.close()

def delete_incident(incident_id):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM incident_report WHERE incident_id = :1", (incident_id,))
        conn.commit()
        return True, "Incident deleted."
    except oracledb.DatabaseError as e:
        return False, f"Cannot delete incident: {e.args[0].message}"
    finally:
        cursor.close()
        conn.close()

# ==========================================
# WINGS & CELLS (Infrastructure)
# ==========================================
def get_all_wings():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM wing ORDER BY wing_id")
        columns = [col[0].lower() for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except oracledb.DatabaseError:
        return []
    finally:
        cursor.close()
        conn.close()

def add_wing(data):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT NVL(MAX(wing_id), 0) + 1 FROM wing")
        new_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO wing (wing_id, wing_name, security_level) VALUES (:1, :2, :3)", 
                       (new_id, data['wing_name'], data['security_level']))
        conn.commit()
        return True, "Wing added."
    except oracledb.DatabaseError as e:
        return False, e.args[0].message
    finally:
        cursor.close()
        conn.close()

def update_wing(wing_id, data):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE wing SET wing_name=:1, security_level=:2 WHERE wing_id=:3", 
                       (data['wing_name'], data['security_level'], wing_id))
        conn.commit()
        return True, "Wing updated."
    except oracledb.DatabaseError as e:
        return False, e.args[0].message
    finally:
        cursor.close()
        conn.close()

def delete_wing(wing_id):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM wing WHERE wing_id = :1", (wing_id,))
        conn.commit()
        return True, "Wing deleted."
    except oracledb.DatabaseError as e:
        return False, f"Cannot delete wing: {e.args[0].message}"
    finally:
        cursor.close()
        conn.close()

def get_all_cells():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        query = """
            SELECT c.cell_id, c.max_capacity, c.wing_id, w.wing_name,
                   (SELECT COUNT(*) FROM inmate i WHERE i.cell_id = c.cell_id) as current_occupants
            FROM cell c
            JOIN wing w ON c.wing_id = w.wing_id
        """
        cursor.execute(query)
        columns = [col[0].lower() for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except oracledb.DatabaseError:
        return []
    finally:
        cursor.close()
        conn.close()

def get_available_cells():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        query = """
            SELECT c.cell_id, c.max_capacity, w.wing_name,
                   (SELECT COUNT(*) FROM inmate i WHERE i.cell_id = c.cell_id) as current_occupants
            FROM cell c
            JOIN wing w ON c.wing_id = w.wing_id
            WHERE c.max_capacity > (SELECT COUNT(*) FROM inmate i WHERE i.cell_id = c.cell_id)
        """
        cursor.execute(query)
        columns = [col[0].lower() for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except oracledb.DatabaseError:
        return []
    finally:
        cursor.close()
        conn.close()

def add_cell(data):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO cell (cell_id, max_capacity, wing_id) VALUES (:1, :2, :3)", 
                       (data['cell_id'], data['max_capacity'], data['wing_id']))
        conn.commit()
        return True, "Cell added."
    except oracledb.DatabaseError as e:
        return False, e.args[0].message
    finally:
        cursor.close()
        conn.close()

def update_cell(cell_id, data):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE cell SET max_capacity=:1, wing_id=:2 WHERE cell_id=:3", 
                       (data['max_capacity'], data['wing_id'], cell_id))
        conn.commit()
        return True, "Cell updated."
    except oracledb.DatabaseError as e:
        return False, e.args[0].message
    finally:
        cursor.close()
        conn.close()

def delete_cell(cell_id):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM cell WHERE cell_id = :1", (cell_id,))
        conn.commit()
        return True, "Cell deleted."
    except oracledb.DatabaseError as e:
        return False, f"Cannot delete cell: {e.args[0].message}"
    finally:
        cursor.close()
        conn.close()

# ==========================================
# MEDICAL SESSIONS
# ==========================================
def get_all_medical():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        query = """
            SELECT ms.session_id, ms.session_date, ms.notes, ms.staff_id, ms.inmate_id,
                   s.name as staff_name, i.name as inmate_name
            FROM medical_session ms
            LEFT JOIN staff s ON ms.staff_id = s.staff_id
            LEFT JOIN inmate i ON ms.inmate_id = i.inmate_id
            ORDER BY ms.session_date DESC
        """
        cursor.execute(query)
        columns = [col[0].lower() for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except oracledb.DatabaseError:
        return []
    finally:
        cursor.close()
        conn.close()

def add_medical(data):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT NVL(MAX(session_id), 0) + 1 FROM medical_session")
        new_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO medical_session (session_id, session_date, notes, staff_id, inmate_id) VALUES (:1, TO_DATE(:2, 'YYYY-MM-DD'), :3, :4, :5)", 
                       (new_id, data['session_date'], data['notes'], data['staff_id'], data['inmate_id']))
        conn.commit()
        return True, "Medical session added."
    except oracledb.DatabaseError as e:
        return False, e.args[0].message
    finally:
        cursor.close()
        conn.close()

def update_medical(session_id, data):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE medical_session SET session_date=TO_DATE(:1, 'YYYY-MM-DD'), notes=:2, staff_id=:3, inmate_id=:4 WHERE session_id=:5", 
                       (data['session_date'], data['notes'], data['staff_id'], data['inmate_id'], session_id))
        conn.commit()
        return True, "Medical session updated."
    except oracledb.DatabaseError as e:
        return False, e.args[0].message
    finally:
        cursor.close()
        conn.close()

def delete_medical(session_id):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM medical_session WHERE session_id = :1", (session_id,))
        conn.commit()
        return True, "Medical session deleted."
    except oracledb.DatabaseError as e:
        return False, f"Cannot delete medical session: {e.args[0].message}"
    finally:
        cursor.close()
        conn.close()

# ==========================================
# RAW QUERY & SCRIPT EXECUTOR
# ==========================================
def execute_custom_query(query):
    conn = get_connection()
    if not conn: return False, "DB connection failed", None, None
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        if cursor.description: # SELECT query
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
            return True, "Query executed successfully.", columns, data
        else: # DML / DDL
            conn.commit()
            return True, f"Statement executed successfully. Rows affected: {cursor.rowcount}", None, None
    except Exception as e:
        return False, str(e), None, None
    finally:
        cursor.close()
        conn.close()

def execute_sql_script(script_text, is_plsql=False):
    conn = get_connection()
    if not conn: return False, "DB connection failed", []
    cursor = conn.cursor()
    results = []
    
    try:
        statements = script_text.split('/' if is_plsql else ';')
        for stmt in statements:
            stmt = stmt.strip()
            if not stmt or stmt.upper() == 'COMMIT' or stmt.upper() == 'EXIT':
                continue
                
            if not is_plsql:
                # Remove line-level comments before executing
                lines = [line for line in stmt.split('\n') if not line.strip().startswith('--')]
                stmt = '\n'.join(lines).strip()
                
            if stmt:
                try:
                    cursor.execute(stmt)
                    results.append({"status": "success", "stmt": stmt[:100] + "..." if len(stmt)>100 else stmt, "msg": "Executed successfully"})
                except oracledb.DatabaseError as e:
                    error, = e.args
                    results.append({"status": "error", "stmt": stmt[:100] + "..." if len(stmt)>100 else stmt, "msg": error.message})
                    
        conn.commit()
        return True, "Script execution completed.", results
    except Exception as e:
        return False, str(e), []
    finally:
        cursor.close()
        conn.close()
