from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
import pymysql

conn = 'mysql://b235f1c1020536:05c7bc48@us-cdbr-east-06.cleardb.net:3306/heroku_1b4da6f4c5dd562'

app = Flask(__name__)
app.config['SECRET_KEY']='secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b3d08a9d0aa394:1a28d8a8@us-cdbr-east-06.cleardb.net/heroku_4b2cb811500b51a?reconnect=true'
db = SQLAlchemy(app)

class DiseaseType(db.Model):
    __tablename__= 'diseasetype'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140), nullable=False)

    def __init__(self, id, description):
        self.id = id
        self.description = description

class Country(db.Model):
    __tablename__= 'country'
    cname = db.Column(db.String(50), primary_key=True)
    population = db.Column(db.BigInteger, nullable=False)

    def __init__(self, cname, population):
        self.cname = cname
        self.population = population

class Disease(db.Model):
    __tablename__= 'disease'
    disease_code = db.Column(db.String(50), primary_key=True)
    pathogen = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(140), nullable=False)
    id = db.Column(db.Integer, db.ForeignKey('diseasetype.id'), nullable=False)

    def __init__(self, disease_code, pathogen, description, id):
        self.disease_code = disease_code
        self.pathogen = pathogen
        self.description = description
        self.id = id

class Discover(db.Model):
    __tablename__= 'discover'
    cname = db.Column(db.String(50), db.ForeignKey('country.cname'), primary_key=True)
    disease_code = db.Column(db.String(50), db.ForeignKey('disease.disease_code'))
    first_enc_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, cname, disease_code, first_enc_date):
        self.cname = cname
        self.disease_code = disease_code
        self.first_enc_date = first_enc_date

class Users(db.Model):
    __tablename__= 'users'
    email = db.Column(db.String(60), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(40), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    cname = db.Column(db.String(50), db.ForeignKey('country.cname'), nullable=False)

    def __init__(self, email, name, surname, salary, phone, cname):
        self.email = email
        self.name = name
        self.surname = surname
        self.salary = salary
        self.phone = phone
        self.cname = cname

class PublicServant(db.Model):
    __tablename__= 'publicservant'
    email = db.Column(db.String(60), db.ForeignKey('users.email'), primary_key=True)
    department = db.Column(db.String(50), nullable=False)

    def __init__(self, email, department):
        self.email = email
        self.department = department

class Doctor(db.Model):
    __tablename__= 'doctor'
    email = db.Column(db.String(60), db.ForeignKey('users.email'), primary_key=True)
    degree = db.Column(db.String(20), nullable=False)

    def __init__(self, email, degree):
        self.email = email
        self.degree = degree

class Specialize(db.Model):
    __tablename__= 'specialize'
    id = db.Column(db.Integer, db.ForeignKey('diseasetype.id'), primary_key=True)
    email = db.Column(db.String(60), db.ForeignKey('doctor.email'), nullable=False)

    def __init__(self, id, email):
        self.id = id
        self.email = email

class Record(db.Model):
    __tablename__= 'record'
    email = db.Column(db.String(60), db.ForeignKey('publicservant.email'), primary_key=True)
    cname = db.Column(db.String(50), db.ForeignKey('country.cname'), primary_key=True)
    disease_code = db.Column(db.String(50), db.ForeignKey('disease.disease_code'), primary_key=True)
    total_deaths = db.Column(db.Integer, nullable=False)
    total_patients = db.Column(db.Integer, nullable=False)
    
    def __init__(self, email, cname, disease_code, total_deaths, total_patients):
        self.email = email
        self.cname = cname
        self.disease_code = disease_code
        self.total_deaths = total_deaths
        self.total_patients = total_patients


@app.route('/')
def index():
    return render_template('index.html', pageTitle='Tables')

#diseasetype
@app.route('/table_diseasetype')
def table_diseasetype():
    data_diseasetype = db.session.query(DiseaseType)
    return render_template('table_diseasetype.html', data=data_diseasetype)

@app.route('/table_diseasetype/add_diseasetype', methods=['GET', 'POST'])
def add_diseasetype():
    if request.method == 'POST':
        id = request.form['id']
        description = request.form['description']

        add_data = DiseaseType(id, description)
        
        db.session.add(add_data)
        db.session.commit()

        flash("Input Data Success")

        return redirect(url_for('table_diseasetype'))

    return render_template('add_diseasetype.html')

@app.route('/update_diseasetype/<int:id>')
def update_diseasetype(id):
    data_diseasetype = DiseaseType.query.get(id)
    return render_template('update_diseasetype.html', data=data_diseasetype)

@app.route('/diseasetype_process_edit', methods=['POST', 'GET'])
def diseasetype_process_edit():
    data_diseasetype = DiseaseType.query.get(request.form.get('id'))

    data_diseasetype.id = request.form['id']
    data_diseasetype.description = request.form['description']

    db.session.commit()

    flash('Edit Data Success')

    return redirect(url_for('table_diseasetype'))

@app.route('/delete_diseasetype/<int:id>')
def delete_diseasetype(id):
    data_diseasetype = DiseaseType.query.get(id)
    db.session.delete(data_diseasetype)
    db.session.commit()

    flash('Delete Data Success')

    return redirect(url_for('table_diseasetype'))

#country
@app.route('/table_country')
def table_country():
    data_country = db.session.query(Country)
    return render_template('table_country.html', data=data_country)

@app.route('/table_country/add_country', methods=['GET', 'POST'])
def add_country():
    if request.method == 'POST':
        cname = request.form['cname']
        population = request.form['population']

        add_data = Country(cname, population)
        
        db.session.add(add_data)
        db.session.commit()

        flash("Input Data Success")

        return redirect(url_for('table_country'))

    return render_template('add_country.html')

@app.route('/update_country/<string:cname>')
def update_country(cname):
    data_country = Country.query.get(cname)
    return render_template('update_country.html', data=data_country)

@app.route('/country_process_edit', methods=['POST', 'GET'])
def country_process_edit():
    data_country = Country.query.get(request.form.get('cname'))

    data_country.cname = request.form['cname']
    data_country.population = request.form['population']

    db.session.commit()

    flash('Edit Data Success')

    return redirect(url_for('table_country'))

@app.route('/delete_country/<string:cname>')
def delete_country(cname):
    data_country = Country.query.get(cname)
    db.session.delete(data_country)
    db.session.commit()

    flash('Delete Data Success')

    return redirect(url_for('table_country'))


#disease
@app.route('/table_disease')
def table_disease():
    data_disease = db.session.query(Disease)
    return render_template('table_disease.html', data=data_disease)

@app.route('/table_disease/add_disease', methods=['GET', 'POST'])
def add_disease():
    if request.method == 'POST':
        disease_code = request.form['disease_code']
        pathogen = request.form['pathogen']
        description = request.form['description']
        id = request.form['id']

        add_data = Disease(disease_code, pathogen, description, id)
        
        db.session.add(add_data)
        db.session.commit()

        flash("Input Data Success")

        return redirect(url_for('table_disease'))

    return render_template('add_disease.html')

@app.route('/update_disease/<string:disease_code>')
def update_disease(disease_code):
    data_disease = Disease.query.get(disease_code)
    return render_template('update_disease.html', data=data_disease)

@app.route('/disease_process_edit', methods=['POST', 'GET'])
def disease_process_edit():
    data_disease = Disease.query.get(request.form.get('disease_code'))

    data_disease.disease_code = request.form['disease_code']
    data_disease.pathogen = request.form['pathogen']
    data_disease.description = request.form['description']
    data_disease.id = request.form['id']

    db.session.commit()

    flash('Edit Data Success')

    return redirect(url_for('table_disease'))

@app.route('/delete_disease/<string:disease_code>')
def delete_disease(disease_code):
    data_disease = Disease.query.get(disease_code)
    db.session.delete(data_disease)
    db.session.commit()

    flash('Delete Data Success')

    return redirect(url_for('table_disease'))

#discover
@app.route('/table_discover')
def table_discover():
    data_discover = db.session.query(Discover)
    return render_template('table_discover.html', data=data_discover)

@app.route('/table_discover/add_discover', methods=['GET', 'POST'])
def add_discover():
    if request.method == 'POST':
        cname = request.form['cname']
        disease_code = request.form['disease_code']
        first_enc_date = request.form['first_enc_date']

        add_data = Discover(cname, disease_code, first_enc_date)
        
        db.session.add(add_data)
        db.session.commit()

        flash("Input Data Success")

        return redirect(url_for('table_discover'))

    return render_template('add_discover.html')

@app.route('/update_discover/<string:cname>')
def update_discover(cname):
    data_discover = Discover.query.get(cname)
    return render_template('update_discover.html', data=data_discover)

@app.route('/discover_process_edit', methods=['POST', 'GET'])
def discover_process_edit():
    data_discover = Discover.query.get(request.form.get('cname'))

    data_discover.cname = request.form['cname']
    data_discover.disease_code = request.form['disease_code']
    data_discover.first_enc_date = request.form['first_enc_date']

    db.session.commit()

    flash('Edit Data Success')

    return redirect(url_for('table_discover'))

@app.route('/delete_discover/<string:cname>')
def delete_discover(cname):
    data_discover = Discover.query.get(cname)
    db.session.delete(data_discover)
    db.session.commit()

    flash('Delete Data Success')

    return redirect(url_for('table_discover'))

#users
@app.route('/table_users')
def table_users():
    data_users = db.session.query(Users)
    return render_template('table_users.html', data=data_users)

@app.route('/table_users/add_users', methods=['GET', 'POST'])
def add_users():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        surname = request.form['surname']
        salary = request.form['salary']
        phone = request.form['phone']
        cname = request.form['cname']

        add_data = Users(email, name, surname, salary, phone, cname)
        
        db.session.add(add_data)
        db.session.commit()

        flash("Input Data Success")

        return redirect(url_for('table_users'))

    return render_template('add_users.html')

@app.route('/update_users/<string:email>')
def update_users(email):
    data_users = Users.query.get(email)
    return render_template('update_users.html', data=data_users)

@app.route('/users_process_edit', methods=['POST', 'GET'])
def users_process_edit():
    data_users = Users.query.get(request.form.get('email'))

    data_users.email = request.form['email']
    data_users.name = request.form['name']
    data_users.surname = request.form['surname']
    data_users.salary = request.form['salary']
    data_users.phone = request.form['phone']
    data_users.cname = request.form['cname']

    db.session.commit()

    flash('Edit Data Success')

    return redirect(url_for('table_users'))

@app.route('/delete_users/<string:email>')
def delete_users(email):
    data_users = Users.query.get(email)
    db.session.delete(data_users)
    db.session.commit()

    flash('Delete Data Success')

    return redirect(url_for('table_users'))

#publicservant
@app.route('/table_publicservant')
def table_publicservant():
    data_publicservant = db.session.query(PublicServant)
    return render_template('table_publicservant.html', data=data_publicservant)

@app.route('/table_publicservant/add_publicservant', methods=['GET', 'POST'])
def add_publicservant():
    if request.method == 'POST':
        email = request.form['email']
        department = request.form['department']

        add_data = PublicServant(email, department)
        
        db.session.add(add_data)
        db.session.commit()

        flash("Input Data Success")

        return redirect(url_for('table_publicservant'))

    return render_template('add_publicservant.html')

@app.route('/update_publicservant/<string:email>')
def update_publicservant(email):
    data_publicservant = PublicServant.query.get(email)
    return render_template('update_publicservant.html', data=data_publicservant)

@app.route('/publicservant_process_edit', methods=['POST', 'GET'])
def publicservant_process_edit():
    data_publicservant = PublicServant.query.get(request.form.get('email'))

    data_publicservant.email = request.form['email']
    data_publicservant.department = request.form['department']

    db.session.commit()

    flash('Edit Data Success')

    return redirect(url_for('table_publicservant'))

@app.route('/delete_publicservant/<string:email>')
def delete_publicservant(email):
    data_publicservant = PublicServant.query.get(email)
    db.session.delete(data_publicservant)
    db.session.commit()

    flash('Delete Data Success')

    return redirect(url_for('table_publicservant'))


#doctor
@app.route('/table_doctor')
def table_doctor():
    data_doctor = db.session.query(Doctor)
    return render_template('table_doctor.html', data=data_doctor)

@app.route('/table_doctor/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        email = request.form['email']
        degree = request.form['degree']

        add_data = Doctor(email, degree)
        
        db.session.add(add_data)
        db.session.commit()

        flash("Input Data Success")

        return redirect(url_for('table_doctor'))

    return render_template('add_doctor.html')

@app.route('/update_doctor/<string:email>')
def update_doctor(email):
    data_doctor = Doctor.query.get(email)
    return render_template('update_doctor.html', data=data_doctor)

@app.route('/doctor_process_edit', methods=['POST', 'GET'])
def doctor_process_edit():
    data_doctor = Doctor.query.get(request.form.get('email'))

    data_doctor.email = request.form['email']
    data_doctor.degree = request.form['degree']

    db.session.commit()

    flash('Edit Data Success')

    return redirect(url_for('table_doctor'))

@app.route('/delete_doctor/<string:email>')
def delete_doctor(email):
    data_doctor = Doctor.query.get(email)
    db.session.delete(data_doctor)
    db.session.commit()

    flash('Delete Data Success')

    return redirect(url_for('table_doctor'))


#specialize
@app.route('/table_specialize')
def table_specialize():
    data_specialize = db.session.query(Specialize)
    return render_template('table_specialize.html', data=data_specialize)

@app.route('/table_specialize/add_specialize', methods=['GET', 'POST'])
def add_specialize():
    if request.method == 'POST':
        id = request.form['id']
        email = request.form['email']

        add_data = Specialize(id, email)
        
        db.session.add(add_data)
        db.session.commit()

        flash("Input Data Success")

        return redirect(url_for('table_specialize'))

    return render_template('add_specialize.html')

@app.route('/update_specialize/<int:id>')
def update_specialize(id):
    data_specialize = Specialize.query.get(id)
    return render_template('update_specialize.html', data=data_specialize)

@app.route('/specialize_process_edit', methods=['POST', 'GET'])
def specialize_process_edit():
    data_specialize = Specialize.query.get(request.form.get('id'))

    data_specialize.id = request.form['id']
    data_specialize.email = request.form['email']

    db.session.commit()

    flash('Edit Data Success')

    return redirect(url_for('table_specialize'))

@app.route('/delete_specialize/<int:id>')
def delete_specialize(id):
    data_specialize = Specialize.query.get(id)
    db.session.delete(data_specialize)
    db.session.commit()

    flash('Delete Data Success')

    return redirect(url_for('table_specialize'))


#record
@app.route('/table_record')
def table_record():
    data_record = db.session.query(Record)
    return render_template('table_record.html', data=data_record)

@app.route('/table_record/add_record', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        email = request.form['email']
        cname = request.form['cname']
        disease_code = request.form['disease_code']
        total_deaths = request.form['total_deaths']
        total_patients = request.form['total_patients']

        add_data = Record(email, cname, disease_code, total_deaths, total_patients)
        
        db.session.add(add_data)
        db.session.commit()

        flash("Input Data Success")

        return redirect(url_for('table_record'))

    return render_template('add_record.html')

@app.route('/update_record/<string:email>')
def update_record(email):
    data_record = Record.query.get(email)
    return render_template('update_record.html', data=data_record)

@app.route('/record_process_edit', methods=['POST', 'GET'])
def record_process_edit():
    data_record = Record.query.get(request.form.get('email'))

    data_record.email = request.form['email']
    data_record.cname = request.form['cname']
    data_record.disease_code = request.form['disease_code']
    data_record.total_deaths = request.form['total_deaths']
    data_record.total_patients = request.form['total_patients']

    db.session.commit()

    flash('Edit Data Success')

    return redirect(url_for('table_record'))

@app.route('/delete_record/<string:email>')
def delete_record(email):
    data_record = Record.query.get(email)
    db.session.delete(data_record)
    db.session.commit()

    flash('Delete Data Success')

    return redirect(url_for('table_record'))