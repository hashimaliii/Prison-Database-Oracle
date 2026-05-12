# Prison Database Oracle System

A robust, web-based database management system for a prison facility, built using Python Flask and Oracle 11g XE. The application provides a comprehensive UI to manage inmates, staff, prison cells, visitations, and security incidents.

## Features
- **Dashboard Overview:** Quick statistics on total inmates, active staff, available cell capacity, and recorded incidents.
- **Inmate Registry:** Register new inmates, assign them to available cells based on security clearance and capacity, and track their admission records.
- **Staff Directory:** Manage prison personnel, differentiating between standard guards (with ranks and shifts) and medical/professional staff.
- **Visitation Logs:** Register recurring visitors and schedule specific visit time slots with assigned inmates.
- **Incident Reporting:** Track security events, their severity (1-5 scale), and the reporting staff member.

## Tech Stack
- **Backend:** Python, Flask, Werkzeug
- **Database:** Oracle 11g XE
- **Database Driver:** `oracledb` (running in Thick mode for 11g compatibility)
- **Frontend:** HTML5, Jinja2 Templates, Bootstrap 5

## Prerequisites
1. **Oracle Database 11g Express Edition (XE)** installed locally.
2. **Python 3.8+** installed.

## Installation & Setup

### 1. Install Python Dependencies
Open your terminal in the project directory and install the required packages:
```bash
pip install -r requirements.txt
```
*(Or manually run: `pip install flask werkzeug oracledb==1.4.2`)*

### 2. Configure Database Connection
By default, the application connects using standard Oracle XE credentials. If you changed these during your installation, update the following lines at the top of `db.py` and `db_setup.py`:
```python
DB_USER = "system" 
DB_PASSWORD = "123" 
DB_DSN = "localhost:1521/xe"
```

### 3. Initialize the Database
Before running the web app, you need to execute the SQL setup scripts to create the tables, sequences, constraints, and insert the seed data.

**Option A (Using Python):**
Run the automated Python database setup script:
```bash
python db_setup.py
```

**Option B (Using Windows Batch):**
Double-click `run_oracle_setup.bat` and follow the prompts to execute the master SQL script via `sqlplus`.

### 4. Start the Web Server
Launch the Flask application:
```bash
python app.py
```
Open your web browser and navigate to: `http://127.0.0.1:5000`

## Default Login Credentials
Once the web app is running, use the following credentials to access the system:
- **Username:** `admin`
- **Password:** `admin123`

*(Note: These credentials are securely hashed and stored in the `admin_users` table during the database setup phase).*

---
**Troubleshooting Oracle Connections:** 
If you encounter `DPY-3010` or `ORA-28040` errors, it means the Python library is struggling to connect to the older Oracle 11g authentication protocol. The `db.py` file is pre-configured to use **Thick mode** by pointing directly to the `C:\oraclexe\app\oracle\product\11.2.0\server\bin` directory to bypass this issue. Ensure your Oracle installation exists at this path.
