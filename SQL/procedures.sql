use nuevadb;
#PROCEDURES
drop procedure if exists AltaMedico;
DELIMITER //
CREATE PROCEDURE AltaMedico(
	IN sp_nombre NVARCHAR(30),
    IN sp_apaterno NVARCHAR(30),
    IN sp_amaterno NVARCHAR(30),
    IN sp_username NVARCHAR(30),
    IN sp_password NVARCHAR(100),
    IN sp_cedula NVARCHAR(30),
    IN sp_correo NVARCHAR(30),
    IN sp_ciudad NVARCHAR(30),
    IN sp_especialidad NVARCHAR(30)
)
BEGIN
	declare existe_username int;
    declare existe_cedula int;
    declare existe_correo int;
	set existe_username = (select count(*) from Usuario where nombreUsuario = sp_username);
    set existe_cedula = (select count(*) from Medico where cedula = sp_cedula);
    set existe_correo = (select count(*) from Medico where correo = sp_correo);
    IF existe_username = 0 THEN
		IF existe_cedula = 0 THEN
			IF existe_correo = 0 THEN
				insert into Persona (nombre,apaterno,amaterno,IDCatalogoPersona) values (sp_nombre,sp_apaterno,sp_amaterno,1);
				insert into Usuario (nombreUsuario,passwor_d,IDPersona,IDCatalogoUsuario) values (sp_username,sha2(sp_password,0),
				(select MAX(idPersona) FROM Persona),2);
				insert into Medico (cedula,correo,especialidad,ciudad,IDUsuario) values (sp_cedula,sp_correo,sp_especialidad,sp_ciudad,
				(select MAX(idUsuario) FROM Usuario));
				SELECT 'REGISTRO EXITOSO' AS MSJ;
			ELSE
				SELECT 'El correo electrónico introducido ya se encuentra registrado.' AS MSJ;
			END IF;
		ELSE
			SELECT 'La cédula introducida ya se encuentra registrada.' AS MSJ;
		END IF;
    ELSE
		SELECT 'El nombre de usuario solicitado ya existe, favor de elegir otro.' AS MSJ;
    END IF;
END //
DELIMITER ;
drop procedure if exists CambioMedicoPersonal;
DELIMITER //
CREATE PROCEDURE CambioMedicoPersonal(
	IN sp_nombre NVARCHAR(30),
    IN sp_apaterno NVARCHAR(30),
    IN sp_amaterno NVARCHAR(30),
    IN sp_idPersona int
)
BEGIN
	UPDATE Persona set nombre=sp_nombre,apaterno=sp_apaterno,amaterno=sp_amaterno where idPersona=sp_idPersona;
END //
DELIMITER ;
drop procedure if exists CambioMedicoUsuario;
DELIMITER //
CREATE PROCEDURE CambioMedicoUsuario(
    IN sp_username NVARCHAR(30),
    IN sp_idUsuario int
)
BEGIN
	UPDATE Usuario set nombreUsuario=sp_username where idUsuario=sp_idUsuario;
END //
DELIMITER ;

drop procedure if exists CambioMedicoTotal;
DELIMITER //
CREATE PROCEDURE CambioMedicoTotal(
	IN sp_nombre NVARCHAR(30),
    IN sp_apaterno NVARCHAR(30),
    IN sp_amaterno NVARCHAR(30),
	IN sp_username NVARCHAR(30),
    IN sp_cedula NVARCHAR(30),
    IN sp_correo NVARCHAR(30),
    IN sp_ciudad NVARCHAR(30),
    IN sp_especialidad NVARCHAR(30),
    IN sp_idMedico int,
	IN sp_idUsuario int,
    IN sp_idPersona int
)
BEGIN
	declare existe_username int;
    declare existe_cedula int;
    declare existe_correo int;
	set existe_username = (select count(*) from Usuario where nombreUsuario = sp_username and idUsuario <> sp_idUsuario);
    set existe_cedula = (select count(*) from Medico where cedula = sp_cedula and idMedico <> sp_idMedico);
    set existe_correo = (select count(*) from Medico where correo = sp_correo and idMedico <> sp_idMedico);
    IF existe_username = 0 THEN
		IF existe_cedula = 0 THEN
			IF existe_correo = 0 THEN
				UPDATE Medico set cedula=sp_cedula,correo=sp_correo,ciudad=sp_ciudad,especialidad=sp_especialidad where idMedico=sp_idMedico;
                UPDATE Usuario set nombreUsuario=sp_username where idUsuario=sp_idUsuario;
                UPDATE Persona set nombre=sp_nombre,apaterno=sp_apaterno,amaterno=sp_amaterno where idPersona=sp_idPersona;
				SELECT 'Registro actualizado!' AS MSJ;
			ELSE
				SELECT 'El correo electrónico introducido ya se encuentra registrado.' AS MSJ;
			END IF;
		ELSE
			SELECT 'La cédula introducida ya se encuentra registrada.' AS MSJ;
		END IF;
    ELSE
		SELECT 'El nombre de usuario solicitado ya existe, favor de elegir otro.' AS MSJ;
    END IF;
END //
DELIMITER ;
call AltaMedico('Almanaque','Trivino','FERNANDEZ','extra','innings',2020201,'a@b.com','Farmaceutirco','Benito Juarez');
#call AltaMedico('Almanaquex','Trivinox','FERNANDEZx','extrax','innings',20202012,'a@bx.com','Farmaceutirco','Benito Juarez');
#call CambioMedicoTotal('Almanaque','Trivino','Gonzalez','extra',2020201,'a@b.com','Farmaceutirco','Benito Juarez',1,4,4);
#call CambioMedicoTotal('Almanaquex','Trivinox','FERNANDEZx','extrao',20202010,'a@bo.com','Farmaceutirco','Benito Juarez',2,5,5);
#select * from usuario;

drop procedure if exists AltaPaciente;
DELIMITER //
CREATE PROCEDURE AltaPaciente(
	IN sp_nombre NVARCHAR(30),
    IN sp_apaterno NVARCHAR(30),
    IN sp_amaterno NVARCHAR(30),
    IN sp_sexo NVARCHAR(10),
    IN sp_edad int,
    IN sp_CURP NVARCHAR(18),
	IN sp_idMedico int,
    IN sp_PubK BLOB
)
BEGIN
	declare existe_curp int;
	set existe_curp = (select count(*) from Paciente where CURP = sp_CURP);
    if existe_curp = 0 then
		insert into Persona (nombre,apaterno,amaterno,IDCatalogoPersona) values (sp_nombre,sp_apaterno,sp_amaterno,2);
		insert into Paciente (sexo,edad,CURP,PubK,IDPersona,IDMedico) values (sp_sexo,sp_edad,sp_CURP,sp_PubK,(select MAX(idPersona) FROM Persona),sp_idMedico);
		SELECT 'REGISTRO EXITOSO' AS MSJ;
	else
		SELECT 'La CURP introducida ya existe' AS MSJ;
	END IF;
END //
DELIMITER ;

drop procedure if exists CambioPacienteTotal;
DELIMITER //
CREATE PROCEDURE CambioPacienteTotal(
	IN sp_nombre NVARCHAR(30),
    IN sp_apaterno NVARCHAR(30),
    IN sp_amaterno NVARCHAR(30),
    IN sp_sexo NVARCHAR(10),
    IN sp_edad int,
    IN sp_CURP NVARCHAR(18),
    IN sp_idPersona int,
    IN sp_idPaciente int
)
BEGIN
    declare existe_CURP int;
	set existe_CURP = (select count(*) from Paciente where CURP = sp_CURP and idPaciente <> sp_idPaciente);
    IF existe_CURP = 0 THEN
			UPDATE Paciente set sexo=sp_sexo,edad=sp_edad,CURP=sp_CURP where idPaciente=sp_idPaciente;
			UPDATE Persona set nombre=sp_nombre,apaterno=sp_apaterno,amaterno=sp_amaterno where idPersona=sp_idPersona;
				SELECT 'Registro actualizado!' AS MSJ;
		ELSE
			SELECT 'La CURP introducida ya está registrada previamente' AS MSJ;
	END IF;
END //
DELIMITER ;

drop procedure if exists Login;
DELIMITER //
CREATE PROCEDURE Login(
	IN sp_username NVARCHAR(30),
    IN sp_password NVARCHAR(30)
)
BEGIN
	declare existe int;
	set existe = (select count(*) from Usuario where nombreUsuario = sp_username and passwor_d = sha2(sp_password,0));
	IF existe = 0 THEN
		SELECT 'Las credenciales de acceso son incorrectas. Intente de nuevo.' AS MSJ;
	ELSE
		SELECT 'USUARIO Y PASSWORD ENCONTRADOS' AS MSJ;
    END IF;
END //
#select * from Paciente;
#select * from Medico;
#drop procedure if exists Login;
#CALL LOGIN('medicotest','medico');
DELIMITER ;
drop procedure if exists AltaNota;
DELIMITER //
CREATE PROCEDURE AltaNota(
		IN sp_iv BLOB,
        IN sp_leak BLOB,
		IN sp_Resumen_Interrogatorio NVARCHAR(280),
		IN sp_Plan_Estudio NVARCHAR(280),
		IN sp_Pronostico NVARCHAR(280),
		IN sp_Exploracion_Fisica NVARCHAR(280),
		IN sp_Resultados_Estudios NVARCHAR(280),
		IN sp_Diagnostico_Problemas NVARCHAR(280),
		IN sp_Estado_Mental NVARCHAR(280),
        IN sp_Peso int,
		IN sp_Talla int,
		IN sp_Presion NVARCHAR(15),
		IN sp_Frecuencia_Cardiaca NVARCHAR(15),
		IN sp_Frecuencia_Respiratorio NVARCHAR(15),
		IN sp_Temperatura NVARCHAR(3),
		IN sp_IDPaciente int,
		IN sp_IDMedico int
)
BEGIN
	insert into Signos (Peso,Talla,Presion,Frecuencia_Cardiaca,Frecuencia_Respiratorio,Temperatura)
    values (sp_Peso,sp_Talla,sp_Presion,sp_Frecuencia_Cardiaca,sp_Frecuencia_Respiratorio,sp_Temperatura);
	insert into NotaMedica (iv,leak,Resumen_Interrogatorio,Plan_Estudio,Pronostico,Exploracion_Fisica,Resultados_Estudios,Diagnostico_Problemas,Estado_Mental,IDPaciente,IDMedico,IDSignos) 
    values (sp_iv,sp_leak,sp_Resumen_Interrogatorio,sp_Plan_Estudio,sp_Pronostico,sp_Exploracion_Fisica,sp_Resultados_Estudios,sp_Diagnostico_Problemas,sp_Estado_Mental,sp_IDPaciente,sp_IDMedico,(select MAX(idSignos) FROM Signos));
    SELECT 'REGISTRO EXITOSO' AS MSJ;
END //
