#import lea_mfrc522_wrapper as lmw
from flask import Flask, render_template, flash, request, redirect, url_for, session,jsonify
from forms import LoginForm, RegistrationForm, MedicoForm, PatientForm, NoteForm
import flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin
from flask_login import login_user, logout_user, current_user, login_required
from flask_cors import CORS
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
#from flask_user import roles_required
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
import pymysql
import hashlib
import os
"""
	if(session['tipoUsuario']==2):
	else:
		return redirect(url_for('indexadmin'))
"""
#create the object of Flask
app  = Flask(__name__)
UPLOAD_FOLDER = 'files'
app.config['SECRET_KEY'] = 'hardsecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#SqlAlchemy Database Configuration With Mysql

conn_str = 'mysql+pymysql://root:thirtythree@localhost/nuevadb'
#conn_str = 'mysql+pymysql://root:''@localhost/nuevadb'

app.config['SQLALCHEMY_DATABASE_URI'] = conn_str
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#CORS(app)
#login code
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login'



#USUARIO
class UserInfo(UserMixin, db.Model):
	__tablename__ = 'Usuario'
	IDUsuario = db.Column(db.Integer,primary_key=True)
	nombreUsuario = db.Column(db.String(30))
	passwor_d = db.Column(db.String(100))
	IDPersona = db.Column(db.Integer,unique=True)
	IDCatalogoUsuario = db.Column(db.Integer)
	def __init__(self,IDUsuario,nombreUsuario,password,IDPersona,IDCatalogoUsuario):
			self.IDUsuario = IDUsuario
			self.nombreUsuario = nombreUsuario
			self.passwor_d = passwor_d
			self.IDPersona = IDPersona
			self.IDCatalogoUsuario = IDCatalogoUsuario
	def get_id(self):
			return self.IDUsuario
	def get_username(self):
			return self.nombreUsuario
	def get_passwor_d(self):
			return self.passwor_d
	def get_IDPersona(self):
			return self.IDPersona
	def get_IDCatalogoUsuario(self):
			return self.IDCatalogoUsuario

#Persona
class PersonInfo(UserMixin, db.Model):
	__tablename__ = 'Persona'
	IDPersona = db.Column(db.Integer,primary_key=True)
	nombre = db.Column(db.String(30))
	apaterno = db.Column(db.String(30))
	amaterno = db.Column(db.String(30))
	IDCatalogoPersona = db.Column(db.Integer)
	def __init__(self,IDPersona,nombre,apaterno,amaterno,IDCatalogoPersona):
			self.IDPersona = IDPersona
			self.nombre = nombre
			self.apaterno = apaterno
			self.amaterno = amaterno
			self.IDCatalogoPersona = IDCatalogoPersona
	def get_id(self):
			return self.IDPersona
	def get_nombre(self):
			return self.nombre
	def get_apaterno(self):
			return self.apaterno
	def get_amaterno(self):
			return self.amaterno
	def get_IDCatalogoPersona(self):
			return self.IDCatalogoPersona

#Medico
class MedicInfo(UserMixin, db.Model):
	__tablename__ = 'Medico'
	IDMedico = db.Column(db.Integer,primary_key=True)
	cedula = db.Column(db.Integer)
	correo = db.Column(db.String(30))
	especialidad = db.Column(db.String(30))
	ciudad = db.Column(db.String(30))
	IDUsuario = db.Column(db.Integer,unique=True)
	def __init__(self,IDMedico,cedula,correo,especialidad,ciudad,IDUsuario):
			self.IDUsuario = IDUsuario
			self.cedula = cedula
			self.correo = especialidad
			self.ciudad = ciudad
			self.IDUsuario = IDUsuario
	def get_id(self):
			return self.IDMedico
	def get_cedula(self):
			return self.cedula
	def get_correo(self):
			return self.correo
	def get_especialidad(self):
			return self.especialidad
	def get_ciudad(self):
			return self.ciudad
	def get_IDUsuario(self):
			return self.IDUsuario

#Paciente
class PatientInfo(UserMixin, db.Model):
	__tablename__ = 'Paciente'
	IDPaciente = db.Column(db.Integer,primary_key=True)
	edad = db.Column(db.Integer)
	sexo = db.Column(db.String(10))
	CURP = db.Column(db.String(18))
	Pubk = db.Column(db.LargeBinary)
	IDMedico = db.Column(db.Integer,unique=True)
	IDPersona = db.Column(db.Integer,unique=True)
	def __init__(self,IDPaciente,edad,sexo,Pubk,CURP,IDMedico,IDPersona):
			self.IDPaciente = IDPaciente
			self.edad = edad
			self.sexo = sexo
			self.PubK = Pubk
			self.CURP = CURP
			self.IDPersona = IDPersona
			self.IDMedico= IDMedico
	def get_id(self):
			return self.IDPaciente
	def get_edad(self):
			return self.edad
	def get_sexo(self):
			return self.sexo
	def get_CURP(self):
			return self.CURP
	def get_PubK(self):
			return self.PubK
	def get_IDPersona(self):
			return self.IDPersona
	def get_IDMedico(self):
			return self.IDMedico

#Nota Medica
class NoteInfo(UserMixin, db.Model):
	__tablename__ = 'NotaMedica'
	IDNotaMedica = db.Column(db.Integer,primary_key=True)
	iv = db.Column(db.LargeBinary)
	Resumen_Interrogatorio = db.Column(db.String(280))
	Plan_Estudio = db.Column(db.String(280))
	Pronostico = db.Column(db.String(280))
	Exploracion_Fisica = db.Column(db.String(280))
	Resultados_Estudios = db.Column(db.String(280))
	Diagnostico_Problemas = db.Column(db.String(280))
	Estado_Mental = db.Column(db.String(280))
	Fecha = db.Column(db.String(10))
	IDPaciente = db.Column(db.Integer,unique=True)
	IDSignos = db.Column(db.Integer,unique=True)
	IDMedico = db.Column(db.Integer,unique=True)
	def __init__(self,iv,IDNotaMedica,Resumen_Interrogatorio,Plan_Estudio,Pronostico,Exploracion_Fisica,Resultados_Estudios,
		Diagnostico_Problemas,Estado_Mental,Fecha,IDPaciente,IDSignos,IDMedico):
			self.IDNotaMedica = IDNotaMedica
			self.iv = iv
			self.Resumen_Interrogatorio = Resumen_Interrogatorio
			self.Plan_Estudio = Plan_Estudio
			self.Pronostico = Pronostico
			self.Exploracion_Fisica = Exploracion_Fisica
			self.Resultados_Estudios = Resultados_Estudios
			self.Diagnostico_Problemas = Diagnostico_Problemas
			self.Estado_Mental = Estado_Mental
			self.Fecha = Fecha
			self.IDPaciente = IDPaciente
			self.IDSignos = IDSignos
			self.IDMedico = IDMedico
	def get_id(self):
			return self.IDPaciente
	def get_iv(self):
			return self.iv
	def get_Resumen_Interrogatorio(self):
			return self.Resumen_Interrogatorio
	def get_Plan_Estudio(self):
			return self.Plan_Estudio
	def get_Pronostico(self):
			return self.Pronostico
	def get_Exploracion_Fisica(self):
			return self.Exploracion_Fisica
	def get_Resultados_Estudios(self):
			return self.Resultados_Estudios
	def get_Diagnostico_Problemas(self):
			return self.Diagnostico_Problemas
	def get_Estado_Mental(self):
			return self.Estado_Mental
	def get_Fecha(self):
			return self.Fecha
	def get_IDPaciente(self):
			return self.idPaciente
	def get_IDSignos(self):
			return self.IDSignos
	def get_IDMedico(self):
			return self.IDMedico

#Signos
class SignInfo(UserMixin, db.Model):
	__tablename__ = 'Signos'
	IDSignos = db.Column(db.Integer,primary_key=True)
	Peso  = db.Column(db.Integer)
	Talla = db.Column(db.Integer)
	Presion = db.Column(db.String(15))
	Frecuencia_Cardiaca = db.Column(db.String(15))
	Frecuencia_Respiratorio = db.Column(db.String(15))
	Temperatura = db.Column(db.String(3))
	def __init__(self,IDSignos,Peso,Talla,Presion,Frecuencia_Cardiaca,Frecuencia_Respiratorio,Temperatura):
			self.IDSignos = IDSignos
			self.Peso = Peso
			self.Talla = Talla
			self.Presion = Presion
			self.Frecuencia_Cardiaca = Frecuencia_Cardiaca
			self.Frecuencia_Respiratorio = Frecuencia_Respiratorio
			self.Temperatura = Temperatura
	def get_id(self):
			return self.IDSignos
	def get_Peso(self):
			return self.Peso
	def get_Talla(self):
			return self.Talla
	def get_Presion(self):
			return self.Presion
	def get_Frecuencia_Cardiaca(self):
			return self.Frecuencia_Cardiaca
	def get_Frecuencia_Respiratorio(self):
			return self.Frecuencia_Respiratorio
	def get_Temperatura(self):
			return self.Temperatura

def encrypt_string(hash_string):
	sha_signature = \
		hashlib.sha256(hash_string.encode()).hexdigest()
	return sha_signature

def read_file(filename):
	with open(filename, 'rb') as f:
		photo = f.read()
	return photo

@app.errorhandler(404)
def not_found(e):
# defining function
  return render_template("404.html")

@login_manager.user_loader
def load_user(user_id):
	return UserInfo.query.get(int(user_id))

#creating our routes
@app.route('/')
@login_required
def index():
	#return render_template('index.html', name = name)
	try:
		if(session['tipoUsuario']==2):
			return redirect(url_for('indexmedico'))
		elif(session['tipoUsuario']==1):
			return redirect(url_for('indexadmin'))
		else:
			return redirect(url_for('Login'))
	except Exception as e:
		return redirect(url_for('Login'))


#admin
@app.route('/admin/indexadmin')
@login_required
def indexadmin():
	if(session['tipoUsuario']==1):
		name = current_user.nombreUsuario
		return render_template('admin/indexadmin.html', name = name)
	else:
		return redirect(url_for('indexmedico'))


@app.route('/admin/altamedico', methods = ['GET', 'POST'])
@login_required
def altamedico():
	if(session['tipoUsuario']==1):
		form = MedicoForm()
		name = current_user.nombreUsuario
		if form.validate_on_submit():
			nombre = form.nombre.data
			apaterno = form.apaterno.data
			amaterno = form.amaterno.data
			nombreUsuario = form.nombreUsuario.data
			cpassword=form.confirmpasswor_d.data
			passwor_d = form.passwor_d.data
			ciudad = form.ciudad.data
			cedula = form.cedula.data
			especialidad = form.especialidad.data
			correo = form.correo.data
			if(cpassword==form.passwor_d.data):
				try:
					dbx = create_engine(conn_str, encoding='utf8')
					connection = dbx.raw_connection()
					cursor = connection.cursor()
					cursor.callproc('AltaMedico', [nombre,apaterno,amaterno,nombreUsuario,passwor_d,cedula,correo,ciudad,especialidad])
					results = cursor.fetchone()
					cursor.close()
					connection.commit()
					connection.close()
					print(results)
					if(results[0]=='REGISTRO EXITOSO'):
						form.nombre.data = ""
						form.apaterno.data = ""
						form.amaterno.data = ""
						form.nombreUsuario.data = ""
						form.passwor_d.data = ""
						form.ciudad.data = ""
						form.cedula.data = ""
						form.especialidad.data = ""
						form.correo.data = ""
						flash("¡Registro dado de alta!")
						#print("¡Registro dado de alta!")
					else:
						flash(results[0])
						#print("El nombre de usuario solicitado ya existe, favor de elegir otro.")
				except Exception as e:
					print(e)
			else:
				flash("Las contraseñas no coinciden, intente de nuevo.")

		return render_template('admin/altamedico.html', form=form)
	else:
		return redirect(url_for('indexmedico'))


@app.route('/admin/consultamedico')
@login_required
def consultamedico():
	if(session['tipoUsuario']==1):
		name = current_user.nombreUsuario
		dbx = create_engine(conn_str, encoding='utf8')
		connection = dbx.raw_connection()
		cursor = connection.cursor()
		cursor.execute("select * from datos_medico")
		data = cursor.fetchall()
		return render_template('admin/consultamedico.html', name = name, data=data)
	else:
		return redirect(url_for('indexmedico'))


@app.route('/admin/bajamedico')
@login_required
def bajamedico():
	if(session['tipoUsuario']==1):
		name = current_user.nombreUsuario
		dbx = create_engine(conn_str, encoding='utf8')
		connection = dbx.raw_connection()
		cursor = connection.cursor()
		cursor.execute("select * from datos_medico")
		data = cursor.fetchall()
		return render_template('admin/bajamedico.html', name = name,data=data)
	else:
		return redirect(url_for('indexmedico'))
#This route is for deleting our employee
@app.route('/admin/deleteMedico/<idPersona>/<idUsuario>/<idMedico>/', methods = ['GET', 'POST'])
def deleteMedico(idPersona,idUsuario,idMedico):
	if(session['tipoUsuario']==1):
		dataPersona = PersonInfo.query.get(idPersona)
		dataUsuario = UserInfo.query.get(idUsuario)
		dataMedico = MedicInfo.query.get(idMedico)
		#print(dataPersona+"."+dataUsuario+"."+dataMedico)
		db.session.delete(dataMedico)
		db.session.commit()
		#db.session.delete(dataUsuario)
		#db.session.commit()
		#db.session.delete(dataPersona)
		#db.session.commit()
		flash("¡Registro eliminado!")
		return redirect(url_for('bajamedico'))
	else:
		return redirect(url_for('indexmedico'))


@app.route('/admin/cambiomedico')
@login_required
def cambiomedico():
	if(session['tipoUsuario']==1):
		name = current_user.nombreUsuario
		dbx = create_engine(conn_str, encoding='utf8')
		connection = dbx.raw_connection()
		cursor = connection.cursor()
		cursor.execute("select * from datos_medico")
		data = cursor.fetchall()
		return render_template('admin/cambiomedico.html', name = name,data=data)
	else:
		return redirect(url_for('indexmedico'))


#this is our update route where we are going to update our employee
@app.route('/admin/datosMedico', methods = ['GET', 'POST'])
def datosMedico():
	if(session['tipoUsuario']==1):
		if request.method == 'POST':
			my_data = MedicInfo.query.get(request.form.get('id'))
			my_data.correo = request.form['correo']
			my_data.especialidad = request.form['especialidad']
			my_data.ciudad = request.form['ciudad']
			my_data.cedula = request.form['cedula']
			db.session.commit()
			flash("¡Registro actualizado!")
			return redirect(url_for('cambiomedico'))
	else:
		return redirect(url_for('indexmedico'))


#this is our update route where we are going to update our employee
@app.route('/admin/datosPersona', methods = ['GET', 'POST'])
def datosPersona():
	if(session['tipoUsuario']==1):
		if request.method == 'POST':
			my_data = PersonInfo.query.get(request.form.get('id'))
			my_data.nombre = request.form['nombre']
			my_data.apaterno = request.form['apaterno']
			my_data.amaterno = request.form['amaterno']
			db.session.commit()
			flash("¡Registro actualizado!")
			return redirect(url_for('cambiomedico'))
	else:
		return redirect(url_for('indexmedico'))


#this is our update route where we are going to update our employee
@app.route('/admin/datosUsuario', methods = ['GET', 'POST'])
def datosUsuario():
	if(session['tipoUsuario']==1):
		if request.method == 'POST':
			my_data = UserInfo.query.get(request.form.get('id'))
			my_data.nombreUsuario = request.form['username']
			db.session.commit()
			flash("¡Registro actualizado!")
			return redirect(url_for('cambiomedico'))
	else:
		return redirect(url_for('indexmedico'))


#medico
@app.route('/medico/indexmedico')
@login_required
def indexmedico():
	if(session['tipoUsuario']==2):
		name = current_user.nombreUsuario
		identificador = session['identificador']
		print(identificador)
		return render_template('medico/indexmedico.html', name = name)
	else:
		return redirect(url_for('indexadmin'))

@app.route('/medico/adminpaciente')
@login_required
def adminpaciente():
	if(session['tipoUsuario']==2):
		name = current_user.nombreUsuario
		return render_template('medico/adminpaciente.html', name = name)
	else:
		return redirect(url_for('indexadmin'))

@app.route('/medico/altapaciente', methods = ['GET', 'POST'])
@login_required
def altapaciente():
	if(session['tipoUsuario']==2):
		form = PatientForm()
		name = current_user.nombreUsuario
		if form.validate_on_submit():
			#Datos de paciente
			nombre = form.nombre.data
			apaterno = form.apaterno.data
			amaterno = form.amaterno.data
			curp = form.curp.data
			sexo = form.sexo.data
			edad = form.edad.data
			#Llave RSA
			privateKeyName=apaterno+"_"+amaterno+"_"+nombre+'_private.pem'
			#publicKeyName=apaterno+"_"+amaterno+"_"+nombre+'_public.pem'
			keyPair = RSA.generate(3072)
			pubKey = keyPair.publickey()
			pubKeyPEM = pubKey.exportKey('PEM')
			privKeyPEM = keyPair.exportKey('PEM')
			with open(privateKeyName,'wb') as privateKeyFile:
				privateKeyFile.write(privKeyPEM)
			# new_key = RSA.generate(2048, e=65537)
			# private_key = new_key.exportKey('PEM')
			# public_key = new_key.publickey().exportKey('PEM')
			# with open(privateKeyName,'wb') as privateKeyFile,open(publicKeyName,'wb') as publicKeyFile:
			# 	privateKeyFile.write(private_key)
			# 	publicKeyFile.write(public_key)
			#Guardado en BD
			print(pubKeyPEM)
			dbx = create_engine(conn_str, encoding='utf8')
			connection = dbx.raw_connection()
			cursor = connection.cursor()
			#datakey = read_file(publicKeyName)
			try:
			#Pubk = convertToBinaryData(publicKeyFile)
				cursor.callproc('AltaPaciente', [nombre,apaterno,amaterno,sexo,int(edad),curp,int(session['identificador']),pubKeyPEM])
				results = cursor.fetchone()
				cursor.close()
				connection.commit()
				connection.close()
				print(results)
				if(results[0]=='REGISTRO EXITOSO'):
					form.nombre.data = ""
					form.apaterno.data = ""
					form.amaterno.data = ""
					form.edad.data = ""
					form.curp.data = ""
					flash("¡Registro dado de alta!, revise el archivo de llave privada correspondiente al usuario paciente.")
					#print("¡Registro dado de alta!")
				else:
					flash(results[0])
			except Exception as e:
				print(e)
		return render_template('medico/altapaciente.html', form=form)
	else:
		return redirect(url_for('indexadmin'))


@app.route('/medico/consultapaciente')
@login_required
def consultapaciente():
	if(session['tipoUsuario']==2):
		name = current_user.nombreUsuario
		dbx = create_engine(conn_str, encoding='utf8')
		connection = dbx.raw_connection()
		cursor = connection.cursor()
		cursor.execute("select * from datos_paciente where idMedico="+str(session['identificador']))
		data = cursor.fetchall()
		return render_template('medico/consultapaciente.html', name = name, data=data)
	else:
		return redirect(url_for('indexadmin'))


@app.route('/medico/cambiopaciente')
@login_required
def cambiopaciente():
	if(session['tipoUsuario']==2):
		name = current_user.nombreUsuario
		dbx = create_engine(conn_str, encoding='utf8')
		connection = dbx.raw_connection()
		cursor = connection.cursor()
		cursor.execute("select * from datos_paciente where idMedico="+str(session['identificador']))
		data = cursor.fetchall()
		return render_template('medico/cambiopaciente.html', name = name, data=data)

	else:
		return redirect(url_for('indexadmin'))

@app.route('/medico/datosPersonaPaciente', methods = ['GET', 'POST'])
def datosPersonaPaciente():
	if(session['tipoUsuario']==2):
		if request.method == 'POST':
			my_data = PersonInfo.query.get(request.form.get('id'))
			my_data.nombre = request.form['nombre']
			my_data.apaterno = request.form['apaterno']
			my_data.amaterno = request.form['amaterno']

			db.session.commit()
			flash("¡Registro actualizado!")
			return redirect(url_for('cambiopaciente'))
	else:
		return redirect(url_for('indexadmin'))


@app.route('/medico/datosPaciente', methods = ['GET', 'POST'])
def datosPaciente():
	if(session['tipoUsuario']==2):
		if request.method == 'POST':
			my_data = PatientInfo.query.get(request.form.get('id'))
			my_data.sexo = request.form['sexo']
			my_data.edad = request.form['edad']
			my_data.CURP = request.form['curp']
			db.session.commit()
			flash("¡Registro actualizado!")
			return redirect(url_for('cambiopaciente'))
	else:
		return redirect(url_for('indexadmin'))

@app.route('/medico/bajapaciente')
@login_required
def bajapaciente():
	if(session['tipoUsuario']==2):
		name = current_user.nombreUsuario
		dbx = create_engine(conn_str, encoding='utf8')
		connection = dbx.raw_connection()
		cursor = connection.cursor()
		cursor.execute("select * from datos_paciente where idMedico="+str(session['identificador']))
		data = cursor.fetchall()
		return render_template('medico/bajapaciente.html', name = name,data=data)
	else:
		return redirect(url_for('indexadmin'))


@app.route('/medico/deletePaciente/<idPersona>/<idPaciente>/', methods = ['GET', 'POST'])
def deletePaciente(idPersona,idPaciente):
	if(session['tipoUsuario']==2):
		dataPersona = PersonInfo.query.get(idPersona)
		dataPaciente = PatientInfo.query.get(idPaciente)
		db.session.delete(dataPaciente)
		db.session.commit()
		#db.session.delete(dataPersona)
		#db.session.commit()
		flash("¡Registro eliminado!")
		return redirect(url_for('bajapaciente'))
	else:
		return redirect(url_for('indexadmin'))

@app.route('/medico/adminota')
@login_required
def adminota():
	if(session['tipoUsuario']==2):
		name = current_user.nombreUsuario
		return render_template('medico/adminota.html', name = name)
	else:
		return redirect(url_for('indexadmin'))

@app.route('/medico/seleccionpaciente')
@login_required
def seleccionpaciente():
	if(session['tipoUsuario']==2):
		name = current_user.nombreUsuario
		dbx = create_engine(conn_str, encoding='utf8')
		connection = dbx.raw_connection()
		cursor = connection.cursor()
		cursor.execute("select * from datos_paciente where idMedico="+str(session['identificador']))
		data = cursor.fetchall()
		return render_template('medico/seleccionpaciente.html', name = name, data=data)
	else:
		return redirect(url_for('indexadmin'))

@app.route('/medico/altanota/<idPaciente>/', methods = ['GET', 'POST'])
@login_required
def altanota(idPaciente):
	if(session['tipoUsuario']==2):
		form = NoteForm()
		name = current_user.nombreUsuario
		session['idPaciente'] = idPaciente
		if form.validate_on_submit():
			resumenInterrogatorio = form.resumenInterrogatorio.data
			planotratamiento = form.planotratamiento.data
			pronostico = form.pronostico.data
			exploracion = form.exploracion.data
			resultado = form.resultado.data
			diagnostico = form.diagnostico.data
			edomental = form.edomental.data
			#fecha= form.fecha.data
			#SIGNOS
			peso = form.peso.data
			talla = form.talla.data
			tension = form.tension.data
			frecuenciaCardiaca = form.frecuenciaCardiaca.data
			frecuenciaRespiratoria = form.frecuenciaRespiratoria.data
			temperatura = form.temperatura.data
			#TAG
			criteriodiagnostico = form.criteriodiagnostico.data
			sugerenciasdiagnosticas = form.sugerenciasdiagnosticas.data
			motivoconsulta = form.motivoconsulta.data
			#Vector de inicialización
			iv=get_random_bytes(16)
			lea_k=get_random_bytes(16)
			#print("VECTORES GENERADOS")
			# binascii.hexlify(encrypted)  -> a la base
			#print("Encrypted: ", binascii.hexlify(encrypted))
			#decryptor = PKCS1_OAEP.new(pubKey)
			#decrypted = decryptor.decrypt(encrypted)  -> llave de lea descifrada
			#Guardado en base
			try:
				dbx = create_engine(conn_str, encoding='utf8')
				connection = dbx.raw_connection()
				cursor = connection.cursor()
				cursor.execute("select Pubk from Paciente where idPaciente="+str(session['idPaciente']))
				pubKey = cursor.fetchone()
				cursor.close()
				#print("LLAVE CIFRADA")
				print(pubKey[0])
				
				newk = RSA.importKey(pubKey[0])
				encryptor = PKCS1_OAEP.new(newk)
				msg = lea_k

				key_encrypted = encryptor.encrypt(msg)
				#print("LLAVE CIFRADA")
				cursor2 = connection.cursor()
				cursor2.callproc('AltaNota',
					[iv,key_encrypted,resumenInterrogatorio,planotratamiento,pronostico,exploracion,resultado,diagnostico,edomental,
					peso,talla,tension,frecuenciaCardiaca,frecuenciaRespiratoria,temperatura,session['idPaciente'],session['identificador']])
				results = cursor2.fetchone()
				cursor2.close()
				connection.commit()
				connection.close()
				print("archivo GENERADO")
				if(results[0]=='REGISTRO EXITOSO'):
					form.resumenInterrogatorio.data=""
					form.planotratamiento.data=""
					form.pronostico.data=""
					form.exploracion.data=""
					form.resultado.data=""

					form.diagnostico.data=""
					form.edomental.data=""
					#form.fecha.data=""
					#SIGNOS
					form.peso.data=""
					form.talla.data=""
					form.tension.data=""
					form.frecuenciaCardiaca.data=""
					form.frecuenciaRespiratoria.data=""
					form.temperatura.data=""
					#TAG
					# kanye for president
					form.criteriodiagnostico.data=""
					form.sugerenciasdiagnosticas.data=""
					form.motivoconsulta.data=""
					"""
						AQUÍ ES DONDE VA LO DE BAJAR INFORMACIÓN A LA ETIQUETA
					"""
					pt = bytearray()
					wrapper = lmw.lea_mfrc522_wrapper()
					cbytes = bytearray(criteriodiagnostico.ljust(480, '\0'), 'utf-8')
					sbytes = bytearray(sugerenciasdiagnosticas.ljust(140, '\0'), 'utf-8')
					mbytes = bytearray(motivoconsulta.ljust(132, '\0'), 'utf-8')
					pt.extend(cbytes)
					pt.extend(sbytes)
					pt.extend(mbytes)
					print(pt)
					wrapper.write_tag(pt, lea_k, iv)

					flash("¡Registro dado de alta e información introducida en etiqueta!")
				else:
					flash(results[0])
			except Exception as e:
				print(e)
		return render_template('medico/altanota.html', form = form)
	else:
		return redirect(url_for('indexadmin'))


@app.route('/medico/seleccionpacientenota')
@login_required
def seleccionpacientenota():
	if(session['tipoUsuario']==2):
		name = current_user.nombreUsuario
		dbx = create_engine(conn_str, encoding='utf8')
		connection = dbx.raw_connection()
		cursor = connection.cursor()
		cursor.execute("select * from datos_paciente where idMedico="+str(session['identificador']))
		data = cursor.fetchall()
		return render_template('medico/seleccionpacientenota.html', name = name, data=data)
	else:
		return redirect(url_for('indexadmin'))


@app.route('/medico/consultanotaregular/<idPaciente>/', methods = ['GET', 'POST'])
@login_required
def consultanotaregular(idPaciente):
	if(session['tipoUsuario']==2):
		name = current_user.nombreUsuario
		session['idPaciente'] = idPaciente
		dbx = create_engine(conn_str, encoding='utf8')
		connection = dbx.raw_connection()
		cursor = connection.cursor()
		cursor.execute("select * from buscar_nota where idPaciente="+str(session['idPaciente']))
		data = cursor.fetchall()
		return render_template('medico/consultanotaregular.html', data=data)
	else:
		return redirect(url_for('indexadmin'))

@app.route('/medico/seleccionpacientenotabaja')
@login_required
def seleccionpacientenotabaja():
	if(session['tipoUsuario']==2):
		name = current_user.nombreUsuario
		dbx = create_engine(conn_str, encoding='utf8')
		connection = dbx.raw_connection()
		cursor = connection.cursor()
		cursor.execute("select * from datos_paciente where idMedico="+str(session['identificador']))
		data = cursor.fetchall()
		return render_template('medico/seleccionpacientenotabaja.html', name = name, data=data)
	else:
		return redirect(url_for('indexadmin'))


@app.route('/medico/bajanota/<idPaciente>/', methods = ['GET', 'POST'])
@login_required
def bajanota(idPaciente):
	if(session['tipoUsuario']==2):
		name = current_user.nombreUsuario
		session['idPaciente'] = idPaciente
		dbx = create_engine(conn_str, encoding='utf8')
		connection = dbx.raw_connection()
		cursor = connection.cursor()
		cursor.execute("select * from buscar_nota where idPaciente="+str(session['idPaciente']))
		data = cursor.fetchall()
		return render_template('medico/bajanota.html', data=data)
	else:
		return redirect(url_for('indexadmin'))

@app.route('/deletenota/<IDNotaMedica>/<IDSignos>/', methods = ['GET', 'POST'])
@login_required
def deletenota(IDNotaMedica,IDSignos):
	if(session['tipoUsuario']==2):
		dataSignos = SignInfo.query.get(IDSignos)
		dataNota = NoteInfo.query.get(IDNotaMedica)
		db.session.delete(dataSignos)
		db.session.commit()
		#db.session.delete(dataNota)
		#db.session.commit()
		flash("¡Registro eliminado!")
		return redirect(url_for('adminota'))
	else:
		return redirect(url_for('indexadmin'))

@app.route('/medico/seleccionpacientenotacambio')
@login_required
def seleccionpacientenotacambio():
	if(session['tipoUsuario']==2):
		name = current_user.nombreUsuario
		dbx = create_engine(conn_str, encoding='utf8')
		connection = dbx.raw_connection()
		cursor = connection.cursor()
		cursor.execute("select * from datos_paciente where idMedico="+str(session['identificador']))
		data = cursor.fetchall()
		return render_template('medico/seleccionpacientenotacambio.html', name = name, data=data)
	else:
		return redirect(url_for('indexadmin'))


@app.route('/medico/cambionota/<idPaciente>/', methods = ['GET', 'POST'])
@login_required
def cambionota(idPaciente):
	if(session['tipoUsuario']==2):
		name = current_user.nombreUsuario
		session['idPaciente'] = idPaciente
		dbx = create_engine(conn_str, encoding='utf8')
		connection = dbx.raw_connection()
		cursor = connection.cursor()
		cursor.execute("select * from buscar_nota where idPaciente="+str(session['idPaciente']))
		data = cursor.fetchall()
		return render_template('medico/cambionota.html', data=data)
	else:
		return redirect(url_for('indexadmin'))

@app.route('/medico/notaInfo', methods = ['GET', 'POST'])
@login_required
def notaInfo():
	if(session['tipoUsuario']==2):
		if request.method == 'POST':
			my_data = NoteInfo.query.get(request.form.get('id'))
			my_data.Resumen_Interrogatorio = request.form['resumenInterrogatorioinfo']
			my_data.Plan_Estudio = request.form['planotratamientoinfo']
			my_data.Pronostico = request.form['pronosticoinfo']
			my_data.Exploracion_Fisica = request.form['exploracioninfo']
			my_data.Resultados_Estudios = request.form['resultadoinfo']
			my_data.Diagnostico_Problemas = request.form['diagnosticoinfo']
			my_data.Estado_Mental = request.form['edomentalinfo']
			db.session.commit()
			flash("¡Registro actualizado!")
			return redirect(url_for('adminota'))
	else:
		return redirect(url_for('indexadmin'))

@app.route('/medico/notaSignos', methods = ['GET', 'POST'])
@login_required
def notaSignos():
	if(session['tipoUsuario']==2):
		if request.method == 'POST':
			my_data = SignInfo.query.get(request.form.get('id'))
			my_data.Peso = request.form['pesosignos']
			my_data.Talla = request.form['tallasignos']
			my_data.Presion = request.form['tensionsignos']
			my_data.Frecuencia_Cardiaca = request.form['frecuenciaCardiacasignos']
			my_data.Frecuencia_Respiratorio = request.form['frecuenciaRespiratoriasignos']
			my_data.Temperatura = request.form['temperaturasignos']
			db.session.commit()
			flash("¡Registro actualizado!")
			return redirect(url_for('adminota'))
	else:
		return redirect(url_for('indexadmin'))


@app.route('/medico/notequery/<IDNotaMedica>/<idSignos>/', methods=['GET', 'POST'])
@login_required
def notequery(IDNotaMedica,idSignos):
	if(session['tipoUsuario']==2):
		dbx = create_engine(conn_str, encoding='utf8')
		connection = dbx.raw_connection()
		cursor = connection.cursor()
		#print(str(IDNotaMedica))
		#print(str(idSignos))
		cursor.execute("select * from nota_paciente where IDNotaMedica="+str(IDNotaMedica)+" and idSignos="+str(idSignos))
		res = cursor.fetchall()
		datos = []
		content = {}
		for result in res:
			content = {'IDNotaMedica': result[0], 'IDSignos': result[1], 'Resumen_Interrogatorio': result[2], 'Plan_Estudio': result[3], 'Pronostico': result[4]
			, 'Exploracion_Fisica': result[5], 'Resultados_Estudios': result[6], 'Diagnostico_Problemas': result[7], 'Estado_Mental': result[8]
			, 'Fecha': result[9], 'Peso': result[10], 'Talla': result[11], 'Presion': result[12]
			, 'Frecuencia_Cardiaca': result[13], 'Frecuencia_Respiratorio': result[14], 'Temperatura': result[15]}
			datos.append(content)
			content = {}
		return jsonify(datos)
	else:
		return redirect(url_for('indexadmin'))

@app.route('/medico/readtag')
@login_required
def readtag():
	if(session['tipoUsuario']==2):
		name = current_user.nombreUsuario
		dbx = create_engine(conn_str, encoding='utf8')
		connection = dbx.raw_connection()
		cursor = connection.cursor()
		cursor.execute("select * from datos_paciente where idMedico="+str(session['identificador']))
		data = cursor.fetchall()
		return render_template('medico/readtag.html', name = name, data=data)
	else:
		return redirect(url_for('indexadmin'))

@app.route('/medico/selectkey/<idPaciente>/', methods = ['GET', 'POST'])
@login_required
def selectkey(idPaciente):
	if(session['tipoUsuario']==2):
		name = current_user.nombreUsuario
		session['idPaciente'] = idPaciente

		if request.method == 'POST':
			f = request.files['file']
			if f.filename == '':
				flash("¡No se selecciono ningun archivo!")
			else:
				criterio = ''
				sugerencias = ''
				motivo = ''
			try:
				f.save(os.path.join('/home/pi/web/python/files/',secure_filename(f.filename)))
				name = current_user.nombreUsuario
				dbx = create_engine(conn_str, encoding='utf8')
				connection = dbx.raw_connection()
				cursor = connection.cursor()
				cursor.execute("select * from nota_blob where idPaciente="+str(session['idPaciente']))
				data = cursor.fetchone()
				archivo = open("files/"+f.filename,"rb")
				llaveprivadafilecontent= archivo.read()
				archivo.close()
				os.remove("'/home/pi/web/python/files/'"+f.filename)
				#os.remove("/home/pi/web/python/files/"+f.filename)

				private_key= RSA.importKey(llaveprivadafilecontent)
				leaciphered= data[2]
				iv = data[3]

				decryptor = PKCS1_OAEP.new(private_key)
				decrypted = decryptor.decrypt(leaciphered)

				#print(decrypted)
				wrapper = lmw.lea_mfrc522_wrapper()
				raw_bytes = wrapper.read_tag(decrypted, iv)
				criterio = raw_bytes[:480].decode('utf-8')
				sugerencias = raw_bytes[480:620].decode('utf-8')
				motivo = raw_bytes[620:].decode('utf-8')
				print(criterio)
				print(sugerencias)
				print(motivo)
				return render_template('medico/showtag.html',kanyewest=criterio,bromomento=sugerencias,urico=motivo)
			except Exception as e:
				flash("¡Ha ocurrido un error con la lectura de la etiqueta!")
				return redirect(url_for('indexmedico'))
				print(e.value)
				
				"""
					Leer etiqueta y redirigir a showtag con la información de la misma
				"""
		return render_template('medico/selectkey.html')
	else:
		return redirect(url_for('indexadmin'))

@app.route('/medico/showtag')
@login_required
def showtag():
	if(session['tipoUsuario']==2):
		return render_template('medico/showtag.html')
	else:
		return redirect(url_for('indexadmin'))



#login route
@app.route('/login' , methods = ['GET', 'POST'])
def Login():
	form = LoginForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			user = UserInfo.query.filter_by(nombreUsuario=form.nombreUsuario.data).first()
			if user:
				sha_signature = encrypt_string(form.passwor_d.data)
				if user.passwor_d==sha_signature:
					login_user(user)
					if(user.IDCatalogoUsuario==1):
						session['identificador'] = '0'
						session['tipoUsuario']=user.IDCatalogoUsuario
						return redirect(url_for('indexadmin'))
					else:
						dbx = create_engine(conn_str, encoding='utf8')
						connection = dbx.raw_connection()
						cursor = connection.cursor()
						cursor.execute("select idMedico from Medico where idUsuario ="+str(user.IDUsuario))
						identifier = cursor.fetchone()
						session['identificador'] = identifier[0]
						session['tipoUsuario']=user.IDCatalogoUsuario
						return redirect(url_for('indexmedico'))
				else:
					flash("Las credenciales de acceso son incorrectas. Intente de nuevo.")
			else:
				flash("Este usuario no está asociado con ninguna cuenta.")
	return render_template('login.html', form = form)

@app.route('/logout')


@login_required
def logout():
	session.pop('username', None)
	logout_user()
	return redirect(url_for('Login'))

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/creditos')
def creditos():
	return render_template('credits.html')

@app.route('/reddr')
def reddr():
	try:
		if(session['tipoUsuario']==2):
			return redirect(url_for('indexmedico'))
		elif(session['tipoUsuario']==1):
			return redirect(url_for('indexadmin'))
		else:
			return redirect(url_for('Login'))
	except Exception as e:
		return redirect(url_for('Login'))

#register route
@app.route('/register' , methods = ['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = generate_password_hash(form.password.data, method = 'sha256')
		username = form.username.data
		password = hashed_password
		new_register =UserInfo(nombreUsuario=username, passwor_d=password)
		db.session.add(new_register)
		db.session.commit()
		flash("Registration was successful, please login")
		return redirect(url_for('Login'))
	return render_template('registration.html', form=form)

#run flask app
if __name__ == "__main__":

	#app.run(debug=True)
	#app.run(host= '0.0.0.0', debug=True)
	#app.run(debug=True)
	app.run(host= '0.0.0.0', debug=True)
 
