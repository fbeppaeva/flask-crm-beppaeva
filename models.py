from extensions import db


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default="prospect")

    def __init__(self, name, email, company, phone, status="prospect"):
        self.name = name
        self.email = email
        self.company = company
        self.phone = phone
        self.status = status

    @classmethod
    def add_customer(cls, name, email, company, phone, status="prospect"):
        customer = cls(name, email, company, phone, status)
        db.session.add(customer)
        db.session.commit()
        return customer

    @classmethod
    def get_all_customers(cls):
        return cls.query.all()

    @classmethod
    def get_customer_by_id(cls, customer_id):
        return cls.query.get(customer_id)

    @classmethod
    def update_customer(cls, customer_id, name, email, company, phone, status):
        customer = cls.get_customer_by_id(customer_id)
        if customer:
            customer.name = name
            customer.email = email
            customer.company = company
            customer.phone = phone
            customer.status = status
            db.session.commit()

    @classmethod
    def delete_customer(cls, customer_id):
        customer = cls.get_customer_by_id(customer_id)
        if customer:
            db.session.delete(customer)
            db.session.commit()


class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default="new")

    def __init__(self, name, email, company, value, source):
        self.name = name
        self.email = email
        self.company = company
        self.value = value
        self.source = source
        self.status = "new"

    @classmethod
    def add_lead(cls, name, email, company, value, source):
        lead = cls(name, email, company, value, source)
        db.session.add(lead)
        db.session.commit()
        return lead

    @classmethod
    def get_all_leads(cls):
        return cls.query.all()

    @classmethod
    def get_lead_by_id(cls, lead_id):
        return cls.query.get(lead_id)

    @classmethod
    def delete_lead(cls, lead_id):
        lead = cls.get_lead_by_id(lead_id)
        if lead:
            db.session.delete(lead)
            db.session.commit()