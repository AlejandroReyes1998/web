use nuevadb;
drop view if exists datos_medico;
create view datos_medico as select Persona.nombre,Persona.apaterno,Persona.amaterno,
Medico.cedula,Medico.especialidad,Medico.correo,Medico.ciudad,
Usuario.nombreUsuario, Persona.idPersona, Usuario.idUsuario, Medico.idMedico
FROM Persona INNER JOIN Usuario ON Persona.idPersona = Usuario.idPersona
INNER JOIN  Medico ON Usuario.idUsuario = Medico.idUsuario;
select * from datos_medico;
create view medico_cedula as select Persona.nombre,Persona.apaterno,Persona.amaterno,
Medico.cedula FROM Persona INNER JOIN Usuario ON Persona.idPersona = Usuario.idPersona
INNER JOIN  Medico ON Usuario.idUsuario = Medico.idUsuario;
select * from medico_cedula;
drop view  if exists datos_paciente;
create view datos_paciente as select Persona.nombre,Persona.apaterno,Persona.amaterno,
Paciente.sexo, Paciente.edad, Persona.idPersona,Paciente.idPaciente,Paciente.idMedico FROM Persona INNER JOIN Paciente ON Persona.idPersona = Paciente.idPersona;
select * from datos_paciente where idMedico = 1;
drop view if exists buscar_nota;
create view buscar_nota as select 
NotaMedica.Fecha, Persona.nombre,Persona.apaterno,Persona.amaterno,Paciente.idPaciente,
NotaMedica.IDNotaMedica,Signos.idSignos,Paciente.idMedico
FROM Persona INNER JOIN Paciente ON Persona.idPersona = Paciente.idPersona 
INNER JOIN NotaMedica ON Paciente.idPaciente = NotaMedica.idPaciente
INNER JOIN  Signos ON NotaMedica.idSignos = Signos.idSignos;
select * from buscar_nota where idPaciente = 2;
select * from datos_paciente;
#select * from datos_paciente where idMedico = 1;
drop view if exists nota_paciente;
create view nota_paciente as select NotaMedica.IDNotaMedica,NotaMedica.IDSignos,NotaMedica.Resumen_Interrogatorio,NotaMedica.Plan_Estudio,
NotaMedica.Pronostico,NotaMedica.Exploracion_Fisica,NotaMedica.Resultados_Estudios,NotaMedica.Diagnostico_Problemas,NotaMedica.Estado_Mental,
NotaMedica.Fecha,Signos.Peso,Signos.Talla,Signos.Presion,Signos.Frecuencia_Cardiaca,Signos.Frecuencia_Respiratorio,Signos.Temperatura 
from NotaMedica JOIN  Signos ON NotaMedica.idSignos = Signos.idSignos;
select * from nota_paciente;

