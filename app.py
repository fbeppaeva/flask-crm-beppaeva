from flask import Flask, render_template, request, redirect, url_for, flash, session
from extensions import db
from flasgger import Swagger

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your-secret-key-change-this'

db.init_app(app)
swagger = Swagger(app)

users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}

from models import Customer, Lead


def init_sample_data():
    if len(Customer.get_all_customers()) == 0:
        Customer.add_customer('John Doe', 'john@example.com', 'Acme Corp', '555-0001', 'active')
        Customer.add_customer('Jane Smith', 'jane@example.com', 'Tech Solutions', '555-0002', 'prospect')
        Customer.add_customer('Bob Wilson', 'bob@example.com', 'Global Industries', '555-0003', 'inactive')

    if len(Lead.get_all_leads()) == 0:
        Lead.add_lead('Alice Brown', 'alice@example.com', 'StartUp Inc', 50000, 'Website')
        Lead.add_lead('Charlie Davis', 'charlie@example.com', 'Enterprise Ltd', 100000, 'Referral')


def login_required():
    return "user" in session


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = users.get(username)

        if user and user["password"] == password:
            session["user"] = username
            session["role"] = user["role"]
            flash(f'Logged in as {username}', 'success')
            return redirect(url_for('customers'))

        flash('Invalid username or password', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))


@app.route('/')
def index():
    if not login_required():
        return redirect(url_for('login'))

    total_customers = len(Customer.get_all_customers())
    total_leads = len(Lead.get_all_leads())
    return render_template('index.html', total_customers=total_customers, total_leads=total_leads)


@app.route('/customers')
def customers():
    if not login_required():
        return redirect(url_for('login'))

    return render_template('customers.html', customers=Customer.get_all_customers())


@app.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    if not login_required():
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        company = request.form.get('company')
        phone = request.form.get('phone')
        status = request.form.get('status', 'prospect')

        if not all([name, email, company, phone]):
            flash('All fields are required!', 'error')
            return redirect(url_for('add_customer'))

        Customer.add_customer(name, email, company, phone, status)
        flash(f'Customer {name} added successfully!', 'success')
        return redirect(url_for('customers'))

    return render_template('add_customer.html')


@app.route('/customers/<int:customer_id>')
def customer_detail(customer_id):
    if not login_required():
        return redirect(url_for('login'))

    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        flash('Customer not found!', 'error')
        return redirect(url_for('customers'))
    return render_template('customer_detail.html', customer=customer)


@app.route('/customers/<int:customer_id>/edit', methods=['GET', 'POST'])
def edit_customer(customer_id):
    if not login_required():
        return redirect(url_for('login'))

    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        flash('Customer not found!', 'error')
        return redirect(url_for('customers'))

    if request.method == 'POST':
        Customer.update_customer(
            customer_id,
            request.form.get('name'),
            request.form.get('email'),
            request.form.get('company'),
            request.form.get('phone'),
            request.form.get('status')
        )
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('customer_detail', customer_id=customer_id))

    return render_template('edit_customer.html', customer=customer)


@app.route('/customers/<int:customer_id>/delete', methods=['POST'])
def delete_customer(customer_id):
    if not login_required():
        return redirect(url_for('login'))

    if session.get("role") != "admin":
        flash('Only admin can delete customers!', 'error')
        return redirect(url_for('customers'))

    Customer.delete_customer(customer_id)
    flash('Customer deleted successfully!', 'success')
    return redirect(url_for('customers'))


@app.route('/leads')
def leads():
    if not login_required():
        return redirect(url_for('login'))

    return render_template('leads.html', leads=Lead.get_all_leads())


@app.route('/leads/add', methods=['GET', 'POST'])
def add_lead():
    if not login_required():
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        company = request.form.get('company')
        value = request.form.get('value')
        source = request.form.get('source')

        if not all([name, email, company, value, source]):
            flash('All fields are required!', 'error')
            return redirect(url_for('add_lead'))

        try:
            Lead.add_lead(name, email, company, float(value), source)
            flash(f'Lead {name} added successfully!', 'success')
        except ValueError:
            flash('Deal value must be a number!', 'error')

        return redirect(url_for('leads'))

    return render_template('add_lead.html')


@app.route('/leads/<int:lead_id>')
def lead_detail(lead_id):
    if not login_required():
        return redirect(url_for('login'))

    lead = Lead.get_lead_by_id(lead_id)
    if not lead:
        flash('Lead not found!', 'error')
        return redirect(url_for('leads'))
    return render_template('lead_detail.html', lead=lead)


@app.route('/leads/<int:lead_id>/delete', methods=['POST'])
def delete_lead(lead_id):
    if not login_required():
        return redirect(url_for('login'))

    if session.get("role") != "admin":
        flash('Only admin can delete leads!', 'error')
        return redirect(url_for('leads'))

    Lead.delete_lead(lead_id)
    flash('Lead deleted successfully!', 'success')
    return redirect(url_for('leads'))


# -------------------------
# REST API + Swagger
# -------------------------

@app.route('/api/health', methods=['GET'])
def api_health():
    """
    Health Check
    ---
    tags:
      - API
    responses:
      200:
        description: API is running
        schema:
          type: object
          properties:
            status:
              type: string
              example: API running
    """
    return {"status": "API running"}, 200


@app.route('/api/customers', methods=['GET'])
def api_get_customers():
    """
    Get all customers
    ---
    tags:
      - Customers API
    responses:
      200:
        description: List of all customers
        schema:
          type: object
          properties:
            customers:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  email:
                    type: string
                  company:
                    type: string
                  phone:
                    type: string
                  status:
                    type: string
    """
    if not login_required():
        return {"error": "Unauthorized"}, 401

    customers = Customer.get_all_customers()
    data = []

    for c in customers:
        data.append({
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "company": c.company,
            "phone": c.phone,
            "status": c.status
        })

    return {"customers": data}, 200


@app.route('/api/customers', methods=['POST'])
def api_add_customer():
    """
    Create a new customer
    ---
    tags:
      - Customers API
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - company
            - phone
          properties:
            name:
              type: string
              example: Max Mustermann
            email:
              type: string
              example: max@example.com
            company:
              type: string
              example: Test GmbH
            phone:
              type: string
              example: 123456
            status:
              type: string
              example: prospect
    responses:
      201:
        description: Customer created successfully
    """
    if not login_required():
        return {"error": "Unauthorized"}, 401

    data = request.get_json()

    if not data:
        return {"error": "No JSON data provided"}, 400

    name = data.get('name')
    email = data.get('email')
    company = data.get('company')
    phone = data.get('phone')
    status = data.get('status', 'prospect')

    if not all([name, email, company, phone]):
        return {"error": "Missing required fields"}, 400

    customer = Customer.add_customer(name, email, company, phone, status)

    return {
        "message": "Customer created successfully",
        "customer": {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "company": customer.company,
            "phone": customer.phone,
            "status": customer.status
        }
    }, 201


@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
def api_update_customer(customer_id):
    """
    Update a customer
    ---
    tags:
      - Customers API
    parameters:
      - in: path
        name: customer_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
            company:
              type: string
            phone:
              type: string
            status:
              type: string
    responses:
      200:
        description: Customer updated successfully
      404:
        description: Customer not found
    """
    if not login_required():
        return {"error": "Unauthorized"}, 401

    data = request.get_json()

    if not data:
        return {"error": "No JSON data provided"}, 400

    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        return {"error": "Customer not found"}, 404

    name = data.get('name', customer.name)
    email = data.get('email', customer.email)
    company = data.get('company', customer.company)
    phone = data.get('phone', customer.phone)
    status = data.get('status', customer.status)

    Customer.update_customer(customer_id, name, email, company, phone, status)

    updated_customer = Customer.get_customer_by_id(customer_id)

    return {
        "message": "Customer updated successfully",
        "customer": {
            "id": updated_customer.id,
            "name": updated_customer.name,
            "email": updated_customer.email,
            "company": updated_customer.company,
            "phone": updated_customer.phone,
            "status": updated_customer.status
        }
    }, 200


@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def api_delete_customer(customer_id):
    """
    Delete a customer
    ---
    tags:
      - Customers API
    parameters:
      - in: path
        name: customer_id
        type: integer
        required: true
    responses:
      200:
        description: Customer deleted successfully
      403:
        description: Only admin can delete customers
      404:
        description: Customer not found
    """
    if not login_required():
        return {"error": "Unauthorized"}, 401

    if session.get("role") != "admin":
        return {"error": "Only admin can delete customers"}, 403

    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        return {"error": "Customer not found"}, 404

    Customer.delete_customer(customer_id)
    return {"message": "Customer deleted successfully"}, 200


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


with app.app_context():
    db.create_all()
    init_sample_data()


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)