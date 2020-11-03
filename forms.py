from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,IntegerField,SelectField,FieldList,TextField,DateField,TextAreaField
from wtforms.validators import InputRequired,Email,Length
from wtforms_components import TimeField

class LoginForm(FlaskForm):
	nombreUsuario = StringField(u'Nombre de usuario', validators=[InputRequired()])
	passwor_d = PasswordField(u'Contraseña', validators=[InputRequired()])

class RegistrationForm(FlaskForm):
	nombreUsuario = StringField('Nombre de usuario', validators=[InputRequired()])
	passwor_d = PasswordField('Contraseña', validators=[InputRequired()])

class MedicoForm(FlaskForm):
	nombre = StringField('Nombre', validators=[InputRequired()])
	apaterno = StringField('Apellido paterno', validators=[InputRequired()])
	amaterno = StringField('Apellido materno', validators=[InputRequired()])
	cedula = IntegerField('Número de cédula', validators=[InputRequired()])
	correo = StringField('Correo Electrónico', validators=[InputRequired(), Email()])
	especialidad = StringField('Especialidad', validators=[InputRequired()])
	ciudad = StringField('Ciudad donde ejerce', validators=[InputRequired()])
	nombreUsuario = StringField('Nombre de usuario', validators=[InputRequired()])
	passwor_d = PasswordField('Contraseña', validators=[InputRequired()])
	confirmpasswor_d = PasswordField('Confirmar Contraseña', validators=[InputRequired()])

class PatientForm(FlaskForm):
	nombre = StringField('Nombre', validators=[InputRequired()])
	apaterno = StringField('Apellido paterno', validators=[InputRequired()])
	amaterno = StringField('Apellido materno', validators=[InputRequired()])
	sexo = SelectField('Sexo', choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Indefinido', 'Indefinido')])
	edad = IntegerField('Edad (años)', validators=[InputRequired()])

class NoteForm(FlaskForm):
	#NOTA MÉDICA
	resumenInterrogatorio = TextAreaField('Resumen del interrogatorio', render_kw={"rows": 4, "cols": 30})
	planotratamiento = TextAreaField('Plan de estudio/tratamiento', render_kw={"rows": 4, "cols": 30})
	pronostico = TextAreaField('Pronostico', render_kw={"rows": 4, "cols": 30})
	exploracion = TextAreaField('Exploracion física', render_kw={"rows": 4, "cols": 30})
	resultado = TextAreaField('Resultado de estudios', render_kw={"rows": 4, "cols": 30})
	diagnostico = TextAreaField('Diagnostico/Problemas', render_kw={"rows": 4, "cols": 30})
	edomental = TextAreaField('Estado mental', render_kw={"rows": 4, "cols": 30})
	fecha= DateField('Fecha de registro (DD/MM/AAAA)',format='%d/%m/%Y', validators=[InputRequired()])
	#SIGNOS
	peso = IntegerField('Peso (KG)', validators=[InputRequired()])
	talla = IntegerField('Talla (CM)', validators=[InputRequired()])
	tension = StringField('Tension (mm)', validators=[InputRequired()])
	frecuenciaCardiaca = StringField('Frecuencia Cardiaca (lat/min)', validators=[InputRequired()])
	frecuenciaRespiratoria = IntegerField('Frecuencia respiratoria (por minuto)', validators=[InputRequired()])
	temperatura = IntegerField('Temperatura (°C)', validators=[InputRequired()])
	#TAG
	criteriodiagnostico = TextAreaField('Criterio Diagnostico', validators=[InputRequired()], render_kw={"rows": 4, "cols": 30})
	sugerenciasdiagnosticas = TextAreaField('Sugerencias diagnosticas', validators=[InputRequired()], render_kw={"rows": 4, "cols": 30})
	motivoconsulta = TextAreaField('Motivo de la consulta', validators=[InputRequired()], render_kw={"rows": 4, "cols": 30})