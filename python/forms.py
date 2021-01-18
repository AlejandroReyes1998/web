from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,IntegerField,SelectField,FieldList,TextField,DateField,TextAreaField
from wtforms.validators import InputRequired,Email,Length,Regexp
from wtforms_components import TimeField

class LoginForm(FlaskForm):
	nombreUsuario = StringField(u'Nombre de usuario', validators=[InputRequired(message="Este campo es obligatorio")])
	passwor_d = PasswordField(u'Contraseña', validators=[InputRequired(message="Este campo es obligatorio")])

class RegistrationForm(FlaskForm):
	nombreUsuario = StringField('Nombre de usuario', validators=[InputRequired()])
	passwor_d = PasswordField('Contraseña', validators=[InputRequired()])

class MedicoForm(FlaskForm):
	nombre = StringField('Nombre', validators=[InputRequired(message="Este campo es obligatorio"),Regexp("^[a-zA-ZÀ-ÿ\u00f1\u00d1 ]*$", flags=0, message="No se admiten caracteres numéricos")])
	apaterno = StringField('Apellido paterno', validators=[InputRequired(message="Este campo es obligatorio"),Regexp("^[a-zA-ZÀ-ÿ\u00f1\u00d1 ]*$", flags=0, message="No se admiten caracteres numéricos")])
	amaterno = StringField('Apellido materno', validators=[InputRequired(message="Este campo es obligatorio"),Regexp("^[a-zA-ZÀ-ÿ\u00f1\u00d1 ]*$", flags=0, message="No se admiten caracteres numéricos")])
	cedula = IntegerField('Número de cédula', validators=[InputRequired(message="Este campo es obligatorio")])
	correo = StringField('Correo Electrónico', validators=[InputRequired(message="Este campo es obligatorio"), Email()])
	especialidad = StringField('Especialidad', validators=[InputRequired(message="Este campo es obligatorio"),Regexp("^[a-zA-ZÀ-ÿ\u00f1\u00d1 ]*$", flags=0, message="No se admiten caracteres numéricos")])
	ciudad = StringField('Ciudad donde ejerce', validators=[InputRequired(message="Este campo es obligatorio"),Regexp("^[a-zA-ZÀ-ÿ\u00f1\u00d1 ]*$", flags=0, message="No se admiten caracteres numéricos")])
	nombreUsuario = StringField('Nombre de usuario', validators=[InputRequired(message="Este campo es obligatorio")])
	passwor_d = PasswordField('Contraseña', validators=[InputRequired(message="Este campo es obligatorio")])
	confirmpasswor_d = PasswordField('Confirmar Contraseña', validators=[InputRequired(message="Este campo es obligatorio")])

class PatientForm(FlaskForm):
	nombre = StringField('Nombre', validators=[InputRequired(message="Este campo es obligatorio")])
	apaterno = StringField('Apellido paterno', validators=[InputRequired(message="Este campo es obligatorio"),Regexp("^[a-zA-ZÀ-ÿ\u00f1\u00d1 ]*$", flags=0, message="No se admiten caracteres numéricos")])
	amaterno = StringField('Apellido materno', validators=[InputRequired(message="Este campo es obligatorio"),Regexp("^[a-zA-ZÀ-ÿ\u00f1\u00d1 ]*$", flags=0, message="No se admiten caracteres numéricos")])
	sexo = SelectField('Sexo', choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Indefinido', 'Indefinido')])
	edad = IntegerField('Edad (años)', validators=[InputRequired(message="Este campo es obligatorio")])
	curp = StringField('CURP', validators=[InputRequired(message="Este campo es obligatorio"),Regexp("^[A-Z]{1}[AEIOU]{1}[A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM]{1}(AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]{1}[0-9]{1}$", flags=0, message="Esta CURP no es válida")])

class NoteForm(FlaskForm):
	#NOTA MÉDICA
	resumenInterrogatorio = TextAreaField('Resumen del interrogatorio', render_kw={"rows": 4, "cols": 30})
	planotratamiento = TextAreaField('Plan de estudio/tratamiento', render_kw={"rows": 4, "cols": 30})
	pronostico = TextAreaField('Pronóstico', render_kw={"rows": 4, "cols": 30})
	exploracion = TextAreaField('Exploración física', render_kw={"rows": 4, "cols": 30})
	resultado = TextAreaField('Resultado de estudios', render_kw={"rows": 4, "cols": 30})
	diagnostico = TextAreaField('Diagnóstico/Problemas', render_kw={"rows": 4, "cols": 30})
	edomental = TextAreaField('Estado mental', render_kw={"rows": 4, "cols": 30})
	#fecha= DateField('Fecha de registro (DD/MM/AAAA)',format='%d/%m/%Y', validators=[InputRequired(message="Este campo es obligatorio")])
	#SIGNOS
	peso = IntegerField('Peso (KG)', validators=[InputRequired(message="Este campo es obligatorio")])
	talla = IntegerField('Talla (CM)', validators=[InputRequired(message="Este campo es obligatorio")])
	tension = StringField('Tensión (mm)', validators=[InputRequired(message="Este campo es obligatorio")])
	frecuenciaCardiaca = StringField('Frecuencia Cardiaca (lat/min)', validators=[InputRequired(message="Este campo es obligatorio")])
	frecuenciaRespiratoria = IntegerField('Frecuencia respiratoria (por minuto)', validators=[InputRequired(message="Este campo es obligatorio")])
	temperatura = IntegerField('Temperatura (°C)', validators=[InputRequired(message="Este campo es obligatorio")])
	#TAG
	criteriodiagnostico = TextAreaField('Criterio Diagnóstico', validators=[InputRequired(message="Este campo es obligatorio")], render_kw={"rows": 4, "cols": 30})
	sugerenciasdiagnosticas = TextAreaField('Sugerencias diagnósticas', validators=[InputRequired(message="Este campo es obligatorio")], render_kw={"rows": 4, "cols": 30})
	motivoconsulta = TextAreaField('Motivo de la consulta', validators=[InputRequired(message="Este campo es obligatorio")], render_kw={"rows": 4, "cols": 30})