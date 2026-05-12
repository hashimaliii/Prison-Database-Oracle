from flask import Flask, render_template, request, redirect, url_for, flash, session
import db
import os
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = os.urandom(24)

# --- Jinja helpers ---
@app.template_filter("strftime")
def jinja_strftime(value, fmt="%Y-%m-%d"):
    if value is None:
        return ""
    if value == "now":
        return datetime.now().strftime(fmt)
    if isinstance(value, (datetime, date)):
        return value.strftime(fmt)
    return str(value)

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if db.verify_login(username, password):
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# --- Dashboard ---
@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session: return redirect(url_for('login'))
    stats = db.get_dashboard_stats()
    return render_template('dashboard.html', stats=stats)

# --- Inmates ---
@app.route('/inmates')
def inmates():
    if 'logged_in' not in session: return redirect(url_for('login'))
    all_inmates = db.get_all_inmates()
    available_cells = db.get_available_cells()
    return render_template('inmates.html', inmates=all_inmates, cells=available_cells)

@app.route('/inmates/add', methods=['POST'])
def add_inmate():
    if 'logged_in' not in session: return redirect(url_for('login'))
    
    data = {
        'name': request.form['name'],
        'nic': request.form['nic'],
        'admission_date': request.form['admission_date'],
        'security_class': request.form['security_class'],
        'crime_category': request.form['crime_category'],
        'cell_id': request.form['cell_id']
    }
    success, msg = db.add_inmate(data)
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('inmates'))

# --- Staff ---
@app.route('/staff')
def staff():
    if 'logged_in' not in session: return redirect(url_for('login'))
    staff_list = db.get_all_staff()
    return render_template('staff.html', staff=staff_list)

# --- Visitation ---
@app.route('/visitation')
def visitation():
    if 'logged_in' not in session: return redirect(url_for('login'))
    logs = db.get_visitation_logs()
    visitors = db.get_all_visitors()
    all_inmates = db.get_all_inmates()
    return render_template('visitation.html', logs=logs, visitors=visitors, inmates=all_inmates)

@app.route('/visitation/log', methods=['POST'])
def log_visitation():
    if 'logged_in' not in session: return redirect(url_for('login'))
    
    data = {
        'visitor_id': request.form['visitor_id'],
        'inmate_id': request.form['inmate_id'],
        'visit_start_time': request.form['visit_start_time'],  # Expected 'YYYY-MM-DD HH24:MI'
        'visit_end_time': request.form['visit_end_time'],      # Expected 'YYYY-MM-DD HH24:MI'
        'purpose': request.form['purpose']
    }
    
    # Simple validation formatting from HTML5 datetime-local (e.g. "2026-05-13T10:00")
    if 'T' in data['visit_start_time']:
        data['visit_start_time'] = data['visit_start_time'].replace('T', ' ')
    if 'T' in data['visit_end_time']:
        data['visit_end_time'] = data['visit_end_time'].replace('T', ' ')
        
    success, msg = db.log_visitation(data)
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('visitation'))

@app.route('/visitors/add', methods=['POST'])
def add_visitor():
    if 'logged_in' not in session: return redirect(url_for('login'))
    data = {
        'name': request.form['name'],
        'nic': request.form['nic'],
        'relation_to_inmate': request.form['relation_to_inmate']
    }
    success, msg = db.add_visitor(data)
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('visitation'))

# --- Incidents ---
@app.route('/incidents')
def incidents():
    if 'logged_in' not in session: return redirect(url_for('login'))
    all_incidents = db.get_all_incidents()
    return render_template('incidents.html', incidents=all_incidents)

# --- Custom SQL Query & Script Runner ---
@app.route('/query', methods=['GET', 'POST'])
def query():
    if 'logged_in' not in session: return redirect(url_for('login'))
    
    query_str = ""
    columns = None
    data = None
    error = None
    success_msg = None
    script_results = []
    
    if request.method == 'POST':
        # Handle Script Uploads
        if 'sql_files' in request.files:
            files = request.files.getlist('sql_files')
            for file in files:
                if file and file.filename:
                    is_plsql = 'plsql' in file.filename.lower()
                    try:
                        content = file.read().decode('utf-8')
                        if content.strip():
                            success, msg, res = db.execute_sql_script(content, is_plsql)
                            script_results.append({
                                "filename": file.filename,
                                "success": success,
                                "msg": msg,
                                "statements": res
                            })
                    except Exception as e:
                        script_results.append({
                            "filename": file.filename,
                            "success": False,
                            "msg": str(e),
                            "statements": []
                        })
                        
        # Handle Raw Query
        query_str = request.form.get('query', '')
        if query_str and query_str.strip():
            success, msg, cols, res_data = db.execute_custom_query(query_str)
            if success:
                success_msg = msg
                columns = cols
                data = res_data
            else:
                error = msg
                
    return render_template('query.html', query=query_str, columns=columns, data=data, error=error, success=success_msg, script_results=script_results)

if __name__ == '__main__':
    print("Starting Prison Database Flask Application...")
    if not db.test_connection():
        print("WARNING: Could not connect to Oracle Database.")
    else:
        print("Database connection OK.")
    app.run(debug=True)
