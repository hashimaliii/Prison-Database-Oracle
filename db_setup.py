import oracledb
import os

# ==========================================
# Database Connection Configuration
# Update these with your Oracle 11g details
# ==========================================
DB_USER = "HR" 
DB_PASSWORD = "123" 
DB_DSN = "localhost:1521/xe" # e.g., localhost:1521/xe or ORCL

# Ordered list of SQL files for setup
SQL_FILES = [
    '10_drop_all.sql',
    '01_create_tables.sql',
    '02_constraints.sql',
    '03_sequences.sql',
    '04_indexes.sql',
    '05_insert_data.sql',
    '07_views.sql',
    '08_dcl.sql',
    '11_resync_sequences.sql',
    '09_plsql.sql',
]

def execute_sql_file(cursor, filepath):
    if not os.path.exists(filepath):
        print(f"[-] File not found: {filepath}")
        return

    with open(filepath, 'r') as file:
        sql_content = file.read()

    # Handle PL/SQL blocks differently (split by '/' instead of ';')
    if 'plsql' in filepath.lower():
        statements = sql_content.split('/')
        for stmt in statements:
            stmt = stmt.strip()
            if stmt:
                try:
                    cursor.execute(stmt)
                    print(f"[+] Executed PL/SQL block from {filepath}")
                except oracledb.DatabaseError as e:
                    error, = e.args
                    print(f"[-] Error executing PL/SQL in {filepath}: {error.message}")
    else:
        # Standard SQL statements separated by ';'
        statements = sql_content.split(';')
        for stmt in statements:
            stmt = stmt.strip()
            # Skip empty lines, COMMIT, EXIT
            if not stmt or stmt.upper() == 'COMMIT' or stmt.upper() == 'EXIT':
                continue
            
            # Remove line-level comments before executing
            lines = [line for line in stmt.split('\n') if not line.strip().startswith('--')]
            clean_stmt = '\n'.join(lines).strip()
            
            if clean_stmt:
                try:
                    cursor.execute(clean_stmt)
                except oracledb.DatabaseError as e:
                    error, = e.args
                    print(f"[-] Error executing statement in {filepath}:\n{clean_stmt}\nError: {error.message}\n")

def main():
    try:
        print("Connecting to Oracle Database...")
        
        # Enable Thick mode for Oracle 11g using the local installation binaries
        try:
            oracledb.init_oracle_client(lib_dir=r"C:\oraclexe\app\oracle\product\11.2.0\server\bin")
        except Exception as e:
            pass # Ignore if already initialized

        connection = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
        cursor = connection.cursor()
        print("[+] Connected successfully.")

        for sql_file in SQL_FILES:
            print(f"[*] Running {sql_file}...")
            execute_sql_file(cursor, sql_file)

        connection.commit()
        print("[+] All scripts executed successfully and changes committed.")

    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"[-] Database connection error: {error.message}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    main()
