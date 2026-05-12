import oracledb
from werkzeug.security import check_password_hash

# Database Configuration
DB_USER = "system"
DB_PASSWORD = "123"
DB_DSN = "localhost:1521/xe"

# Initialize Thick mode for Oracle 11g
try:
    oracledb.init_oracle_client(lib_dir=r"C:\oraclexe\app\oracle\product\11.2.0\server\bin")
except Exception:
    pass # Ignore if already initialized or not needed

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
    conn = get_connection()
    if not conn: return False
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT password_hash FROM admin_users WHERE username = :1", (username,))
        row = cursor.fetchone()
        if row and check_password_hash(row[0], password):
            return True
        return False
    finally:
        cursor.close()
        conn.close()

def get_dashboard_stats():
    conn = get_connection()
    if not conn: return {"total_inmates": 0, "total_staff": 0, "total_incidents": 0}
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
    finally:
        cursor.close()
        conn.close()

# --- Inmates ---
def get_all_inmates():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        query = """
            SELECT i.inmate_id, i.name, i.nic, i.admission_date, i.security_class, i.crime_category, c.cell_id, w.wing_name
            FROM inmate i
            LEFT JOIN cell c ON i.cell_id = c.cell_id
            LEFT JOIN wing w ON c.wing_id = w.wing_id
            ORDER BY i.inmate_id
        """
        cursor.execute(query)
        columns = [col[0].lower() for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
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
    finally:
        cursor.close()
        conn.close()

def add_inmate(data):
    conn = get_connection()
    if not conn: return False, "Database connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO inmate (inmate_id, name, nic, admission_date, security_class, crime_category, cell_id)
            VALUES (inmate_seq.NEXTVAL, :name, :nic, TO_DATE(:admission_date, 'YYYY-MM-DD'), :security_class, :crime_category, :cell_id)
        """, (data['name'], data['nic'], data['admission_date'], data['security_class'], data['crime_category'], data['cell_id']))
        conn.commit()
        return True, "Inmate successfully added."
    except oracledb.DatabaseError as e:
        error, = e.args
        return False, error.message
    finally:
        cursor.close()
        conn.close()

# --- Staff ---
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
    finally:
        cursor.close()
        conn.close()

# --- Visitors ---
def get_all_visitors():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM visitor ORDER BY visitor_id")
        columns = [col[0].lower() for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()

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
    finally:
        cursor.close()
        conn.close()

def add_visitor(data):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        # Since we don't have a visitor_seq in the schema by default, we'll get MAX(visitor_id) + 1
        cursor.execute("SELECT NVL(MAX(visitor_id), 0) + 1 FROM visitor")
        new_id = cursor.fetchone()[0]
        
        cursor.execute("""
            INSERT INTO visitor (visitor_id, name, nic, relation_to_inmate)
            VALUES (:id, :name, :nic, :relation)
        """, (new_id, data['name'], data['nic'], data['relation_to_inmate']))
        conn.commit()
        return True, "Visitor added."
    except oracledb.DatabaseError as e:
        error, = e.args
        return False, error.message
    finally:
        cursor.close()
        conn.close()

def log_visitation(data):
    conn = get_connection()
    if not conn: return False, "DB connection failed"
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO visitation_log (visitor_id, inmate_id, visit_start_time, visit_end_time, purpose)
            VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD HH24:MI'), TO_DATE(:4, 'YYYY-MM-DD HH24:MI'), :5)
        """, (data['visitor_id'], data['inmate_id'], data['visit_start_time'], data['visit_end_time'], data['purpose']))
        conn.commit()
        return True, "Visitation log recorded."
    except oracledb.DatabaseError as e:
        error, = e.args
        return False, error.message
    finally:
        cursor.close()
        conn.close()

# --- Incidents ---
def get_all_incidents():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        query = """
            SELECT ir.incident_id, ir.description, ir.incident_date, ir.severity, s.name as reporter_name
            FROM incident_report ir
            LEFT JOIN staff s ON ir.reporter_id = s.staff_id
            ORDER BY ir.incident_date DESC
        """
        cursor.execute(query)
        columns = [col[0].lower() for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()
