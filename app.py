from flask import Flask, render_template, request, redirect, url_for, flash, session
import db
import os
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.template_filter("strftime")
def jinja_strftime(value, fmt="%Y-%m-%d"):
    if value is None: return ""
    if value == "now": return datetime.now().strftime(fmt)
    if isinstance(value, (datetime, date)): return value.strftime(fmt)
    return str(value)

@app.route('/')
def index():
    if 'logged_in' in session: return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if db.verify_login(request.form['username'], request.form['password']):
            session['logged_in'] = True
            session['username'] = request.form['username']
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

# ==========================================
# DASHBOARD & INFRASTRUCTURE
# ==========================================
@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session: return redirect(url_for('login'))
    stats = db.get_dashboard_stats()
    wings = db.get_all_wings()
    cells = db.get_all_cells()
    return render_template('dashboard.html', stats=stats, wings=wings, cells=cells)

@app.route('/dashboard/wing/add', methods=['POST'])
def add_wing():
    if 'logged_in' not in session: return redirect(url_for('login'))
    data = {'wing_name': request.form['wing_name'], 'security_level': request.form['security_level']}
    success, msg = db.add_wing(data)
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('dashboard'))

@app.route('/dashboard/wing/delete/<int:id>', methods=['POST'])
def delete_wing(id):
    if 'logged_in' not in session: return redirect(url_for('login'))
    success, msg = db.delete_wing(id)
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('dashboard'))

@app.route('/dashboard/cell/add', methods=['POST'])
def add_cell():
    if 'logged_in' not in session: return redirect(url_for('login'))
    data = {'cell_id': request.form['cell_id'], 'max_capacity': request.form['max_capacity'], 'wing_id': request.form['wing_id']}
    success, msg = db.add_cell(data)
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('dashboard'))

@app.route('/dashboard/cell/delete/<int:id>', methods=['POST'])
def delete_cell(id):
    if 'logged_in' not in session: return redirect(url_for('login'))
    success, msg = db.delete_cell(id)
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('dashboard'))

# ==========================================
# INMATES & MEDICAL
# ==========================================
@app.route('/inmates')
def inmates():
    if 'logged_in' not in session: return redirect(url_for('login'))
    return render_template('inmates.html', 
                           inmates=db.get_all_inmates(), 
                           cells=db.get_available_cells(),
                           medical_sessions=db.get_all_medical(),
                           staff=db.get_all_staff())

@app.route('/inmates/add', methods=['POST'])
def add_inmate():
    if 'logged_in' not in session: return redirect(url_for('login'))
    data = {
        'name': request.form['name'], 'nic': request.form['nic'], 
        'admission_date': request.form['admission_date'], 
        'release_date': request.form.get('release_date'),
        'security_class': request.form['security_class'],
        'crime_category': request.form['crime_category'], 'cell_id': request.form['cell_id']
    }
    success, msg = db.add_inmate(data)
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('inmates'))

@app.route('/inmates/edit/<int:id>', methods=['POST'])
def edit_inmate(id):
    if 'logged_in' not in session: return redirect(url_for('login'))
    data = {
        'name': request.form['name'], 'nic': request.form['nic'], 
        'admission_date': request.form['admission_date'],
        'release_date': request.form.get('release_date'),
        'security_class': request.form['security_class'],
        'crime_category': request.form['crime_category'], 'cell_id': request.form['cell_id']
    }
    success, msg = db.update_inmate(id, data)
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('inmates'))

@app.route('/inmates/delete/<int:id>', methods=['POST'])
def delete_inmate(id):
    if 'logged_in' not in session: return redirect(url_for('login'))
    success, msg = db.delete_inmate(id)
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('inmates'))

@app.route('/medical/add', methods=['POST'])
def add_medical():
    if 'logged_in' not in session: return redirect(url_for('login'))
    data = {'session_date': request.form['session_date'], 'notes': request.form['notes'], 'staff_id': request.form['staff_id'], 'inmate_id': request.form['inmate_id']}
    success, msg = db.add_medical(data)
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('inmates'))

@app.route('/medical/delete/<int:id>', methods=['POST'])
def delete_medical(id):
    if 'logged_in' not in session: return redirect(url_for('login'))
    success, msg = db.delete_medical(id)
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('inmates'))

# ==========================================
# STAFF
# ==========================================
@app.route('/staff')
def staff():
    if 'logged_in' not in session: return redirect(url_for('login'))
    return render_template('staff.html', staff=db.get_all_staff())

@app.route('/staff/add', methods=['POST'])
def add_staff():
    if 'logged_in' not in session: return redirect(url_for('login'))
    data = {
        'name': request.form['name'], 'contact_info': request.form['contact_info'], 'hire_date': request.form['hire_date'],
        'staff_type': request.form['staff_type'], 'rank': request.form.get('rank'), 'shift_type': request.form.get('shift_type'),
        'specialty': request.form.get('specialty'), 'license_number': request.form.get('license_number')
    }
    success, msg = db.add_staff(data)
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('staff'))

@app.route('/staff/delete/<int:id>', methods=['POST'])
def delete_staff(id):
    if 'logged_in' not in session: return redirect(url_for('login'))
    success, msg = db.delete_staff(id)
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('staff'))

# ==========================================
# VISITATION
# ==========================================
@app.route('/visitation')
def visitation():
    if 'logged_in' not in session: return redirect(url_for('login'))
    return render_template('visitation.html', logs=db.get_visitation_logs(), visitors=db.get_all_visitors(), inmates=db.get_all_inmates())

@app.route('/visitation/log', methods=['POST'])
def log_visitation():
    if 'logged_in' not in session: return redirect(url_for('login'))
    data = {'visitor_id': request.form['visitor_id'], 'inmate_id': request.form['inmate_id'], 'visit_start_time': request.form['visit_start_time'].replace('T', ' '), 'visit_end_time': request.form['visit_end_time'].replace('T', ' '), 'purpose': request.form['purpose']}
    success, msg = db.log_visitation(data)
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('visitation'))

@app.route('/visitation/log/delete', methods=['POST'])
def delete_visitation_log():
    if 'logged_in' not in session: return redirect(url_for('login'))
    success, msg = db.delete_visitation_log(request.form['visitor_id'], request.form['inmate_id'], request.form['visit_start_time'])
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('visitation'))

@app.route('/visitors/add', methods=['POST'])
def add_visitor():
    if 'logged_in' not in session: return redirect(url_for('login'))
    data = {'name': request.form['name'], 'nic': request.form['nic'], 'relation_to_inmate': request.form['relation_to_inmate']}
    success, msg = db.add_visitor(data)
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('visitation'))

@app.route('/visitors/delete/<int:id>', methods=['POST'])
def delete_visitor(id):
    if 'logged_in' not in session: return redirect(url_for('login'))
    success, msg = db.delete_visitor(id)
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('visitation'))

# ==========================================
# INCIDENTS
# ==========================================
@app.route('/incidents')
def incidents():
    if 'logged_in' not in session: return redirect(url_for('login'))
    return render_template('incidents.html', incidents=db.get_all_incidents(), staff=db.get_all_staff())

@app.route('/incidents/add', methods=['POST'])
def add_incident():
    if 'logged_in' not in session: return redirect(url_for('login'))
    data = {'description': request.form['description'], 'incident_date': request.form['incident_date'], 'severity': request.form['severity'], 'reporter_id': request.form['reporter_id']}
    success, msg = db.add_incident(data)
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('incidents'))

@app.route('/incidents/delete/<int:id>', methods=['POST'])
def delete_incident(id):
    if 'logged_in' not in session: return redirect(url_for('login'))
    success, msg = db.delete_incident(id)
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('incidents'))

@app.route('/dashboard/wing/edit/<int:id>', methods=['POST'])
def edit_wing(id):
    if 'logged_in' not in session: return redirect(url_for('login'))
    success, msg = db.update_wing(id, {'wing_name': request.form['wing_name'], 'security_level': request.form['security_level']})
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('dashboard'))

@app.route('/dashboard/cell/edit/<int:id>', methods=['POST'])
def edit_cell(id):
    if 'logged_in' not in session: return redirect(url_for('login'))
    success, msg = db.update_cell(id, {'max_capacity': request.form['max_capacity'], 'wing_id': request.form['wing_id']})
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('dashboard'))

@app.route('/staff/edit/<int:id>', methods=['POST'])
def edit_staff(id):
    if 'logged_in' not in session: return redirect(url_for('login'))
    data = {
        'name': request.form['name'], 'contact_info': request.form['contact_info'], 'hire_date': request.form['hire_date'],
        'staff_type': request.form['staff_type'], 'rank': request.form.get('rank'), 'shift_type': request.form.get('shift_type'),
        'specialty': request.form.get('specialty'), 'license_number': request.form.get('license_number')
    }
    success, msg = db.update_staff(id, data)
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('staff'))

@app.route('/visitors/edit/<int:id>', methods=['POST'])
def edit_visitor(id):
    if 'logged_in' not in session: return redirect(url_for('login'))
    success, msg = db.update_visitor(id, {'name': request.form['name'], 'nic': request.form['nic'], 'relation_to_inmate': request.form['relation_to_inmate']})
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('visitation'))

@app.route('/incidents/edit/<int:id>', methods=['POST'])
def edit_incident(id):
    if 'logged_in' not in session: return redirect(url_for('login'))
    success, msg = db.update_incident(id, {'description': request.form['description'], 'incident_date': request.form['incident_date'], 'severity': request.form['severity'], 'reporter_id': request.form['reporter_id']})
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('incidents'))

@app.route('/medical/edit/<int:id>', methods=['POST'])
def edit_medical(id):
    if 'logged_in' not in session: return redirect(url_for('login'))
    success, msg = db.update_medical(id, {'session_date': request.form['session_date'], 'notes': request.form['notes'], 'staff_id': request.form['staff_id'], 'inmate_id': request.form['inmate_id']})
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('inmates'))

# ==========================================
# RAW SQL QUERY
# ==========================================
@app.route('/query', methods=['GET', 'POST'])
def query():
    if 'logged_in' not in session: return redirect(url_for('login'))
    query_str = ""
    columns = data = error = success_msg = None
    script_results = []
    
    if request.method == 'POST':
        if 'sql_files' in request.files:
            for file in request.files.getlist('sql_files'):
                if file and file.filename:
                    try:
                        content = file.read().decode('utf-8')
                        if content.strip():
                            success, msg, res = db.execute_sql_script(content, 'plsql' in file.filename.lower())
                            script_results.append({"filename": file.filename, "success": success, "msg": msg, "statements": res})
                    except Exception as e:
                        script_results.append({"filename": file.filename, "success": False, "msg": str(e), "statements": []})
                        
        query_str = request.form.get('query', '')
        if query_str and query_str.strip():
            success, msg, cols, res_data = db.execute_custom_query(query_str)
            if success:
                success_msg, columns, data = msg, cols, res_data
            else:
                error = msg
                
    return render_template('query.html', query=query_str, columns=columns, data=data, error=error, success=success_msg, script_results=script_results)

if __name__ == '__main__':
    print("Starting Prison Database Flask Application...")
    app.run(debug=True)
