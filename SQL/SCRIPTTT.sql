drop database if exists nuevadb;
create database nuevadb;
use nuevadb;
#database generation
create table Persona (IDPersona int not null auto_increment,
						nombre NVARCHAR(30), 
                        apaterno NVARCHAR(30), 
                        amaterno NVARCHAR(30), 
                        IDCatalogoPersona int,
                        primary key(IDPersona));
create table CatalogoPersona (IDCatalogoPersona int not null,
						tipoPersona nvarchar(10),
                        primary key(IDCatalogoPersona));
create table Usuario (IDUsuario int not null auto_increment,
						nombreUsuario NVARCHAR(30), 
                        passwor_d NVARCHAR(100), 
                        IDPersona int,
                        IDCatalogoUsuario int,
                        primary key(IDUsuario));
create table CatalogoUsuario (IDCatalogoUsuario int not null,
						tipoUsuario nvarchar(13),
                        primary key(IDCatalogoUsuario));
create table Paciente (IDPaciente int not null auto_increment,
						edad int, 
                        sexo NVARCHAR(10),
                        PubK BLOB,
                        CURP NVARCHAR(18),
                        IDPersona int,
                        IDMedico int,
                        primary key(IDPaciente));
create table Medico (IDMedico int not null auto_increment,
						cedula int, 
                        correo NVARCHAR(30),
                        especialidad NVARCHAR(30),
                        ciudad NVARCHAR(30),
                        IDUsuario int,
                        primary key(IDMedico));
create table Administrador (IDAdministrador int not null auto_increment,
                        IDUsuario int,
                        primary key(IDAdministrador));
create table NotaMedica (IDNotaMedica int not null auto_increment,
                        iv BLOB,
                        lea_k BLOB,
			Resumen_Interrogatorio NVARCHAR(280),
                        Plan_Estudio NVARCHAR(280), 
                        Pronostico NVARCHAR(280), 
                        Exploracion_Fisica NVARCHAR(280), 
                        Resultados_Estudios NVARCHAR(280), 
                        Diagnostico_Problemas NVARCHAR(280), 
                        Estado_Mental NVARCHAR(280),
                        Fecha NVARCHAR(10), 
                        IDPaciente int,
			IDSignos int,
                        IDMedico int,
                        primary key(IDNotaMedica));
create table Signos (IDSignos int not null auto_increment,
			Peso int,
                        Talla int,
                        Presion NVARCHAR(15),
                        Frecuencia_Cardiaca NVARCHAR(15),
                        Frecuencia_Respiratorio NVARCHAR(15),
                        Temperatura NVARCHAR(3),
                        primary key(IDSignos));
#FOREIGN KEY RELATIONS
ALTER TABLE Usuario ADD CONSTRAINT FK_PersonaUsuario FOREIGN KEY (IDPersona) REFERENCES Persona(IDPersona) on delete cascade;
ALTER TABLE Paciente ADD CONSTRAINT FK_PersonaPaciente FOREIGN KEY (IDPersona) REFERENCES Persona(IDPersona) on delete cascade;
ALTER TABLE Paciente ADD CONSTRAINT FK_MedicoPaciente FOREIGN KEY (IDMedico) REFERENCES Medico(IDMedico) on delete cascade;
ALTER TABLE Administrador ADD CONSTRAINT FK_UsuarioAdmin FOREIGN KEY (IDUsuario) REFERENCES Usuario(IDUsuario) on delete cascade;
ALTER TABLE Medico ADD CONSTRAINT FK_UsuarioMedico FOREIGN KEY (IDUsuario) REFERENCES Usuario(IDUsuario) on delete cascade;
ALTER TABLE NotaMedica ADD CONSTRAINT FK_MedicoNota FOREIGN KEY (IDMedico) REFERENCES Medico(IDMedico) on delete cascade;
ALTER TABLE NotaMedica ADD CONSTRAINT FK_PacienteNota FOREIGN KEY (IDPaciente) REFERENCES Paciente(IDPaciente) on delete cascade;
ALTER TABLE NotaMedica ADD CONSTRAINT FK_SignosNota FOREIGN KEY (IDSignos) REFERENCES Signos(IDSignos) on delete cascade;
alter table Usuario add foreign key (IDCatalogoUsuario) REFERENCES CatalogoUsuario(IDCatalogoUsuario) on delete cascade;
alter table Persona add foreign key (IDCatalogoPersona) REFERENCES CatalogoPersona(IDCatalogoPersona) on delete cascade;
-- catalogos
insert into CatalogoPersona (IDCatalogoPersona,tipoPersona) values (1,"Usuario"),(2,"Persona");
insert into CatalogoUsuario (IDCatalogoUsuario,tipoUsuario) values (1,"Administrador"),(2,"Medico");
-- admins
insert into Persona (nombre,apaterno,amaterno,IDCatalogoPersona) values ("Cesar Uriel","Hernandez","Castellanos",1),("Mauricio Joel","Martinez","Islas",1),("Alejandro","Reyes","Valenzuela",1);#,("Medico","Perez","TDYU",1)
insert into Usuario (nombreUsuario,passwor_d,IDPersona,IDCatalogoUsuario) values ("CesarUrico",sha2("cesarurieladmin123",0),1,1),("Matrix",sha2("animel0v3r",0),2,1),("AlejandroR",sha2("JohnCena23231.1",0),3,1);#,("medicotest",sha2("medico",0),4,2)
-- pruebas
select * from Usuario;
select * from Medico;
select * from Persona;
select * from Paciente;
describe Usuario;
select * from NotaMedica;
select * from Signos;