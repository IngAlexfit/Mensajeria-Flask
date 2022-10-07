import sqlite3

def ver_enviados(correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select m.asunto,m.mensaje,m.fecha,m.hora,u.nombreusuario from usuarios u,mensajeria m where u.correo=m.destino and m.origen='"+correo+"' order by fecha desc,hora desc"
    cursor.execute(consulta)
    return cursor.fetchall()

def ver_recibidos(correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select m.asunto,m.mensaje,m.fecha,m.hora,u.nombreusuario from usuarios u,mensajeria m where u.correo=m.origen and m.destino='"+correo+"' order by fecha desc,hora desc"
    cursor.execute(consulta)
    return cursor.fetchall()    

def consultar_usuario(correo, password):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select *from usuarios where correo='"+correo+"' and password='"+password+"'"
    cursor.execute(consulta)

    return cursor.fetchall()    
    

    
def consultar_usuarios(usuario):
    
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select *from usuarios where nombreusuario='"+usuario+"'"
    cursor.execute(consulta)
    return cursor.fetchall() 
def consultar_correo(correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select *from usuarios where correo='"+correo+"'"
    cursor.execute(consulta)
    return cursor.fetchall()     
def consultar_cuentvalida(correo, password):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select *from usuarios where correo='"+correo+"' and password='"+password+"' and estado='1'"
    cursor.execute(consulta)
    return cursor.fetchall()

def lista_destinatarios(usuario):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select *from usuarios where correo<>'"+usuario+"'"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado 



def registrar_usuarios(nombre,correo, password,codigo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="insert into usuarios (nombreusuario,correo,password,estado,codigoactivacion) values ('"+nombre+"','"+correo+"','"+password+"','0','"+codigo+"')"
    cursor.execute(consulta)
    db.commit()
    return "1" 

def registrar_email(origen,destino, asunto,mensaje):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="insert into mensajeria (asunto,mensaje,fecha,hora,origen,destino,estado) values ('"+asunto+"','"+mensaje+"',DATE('now'),TIME('now'),'"+origen+"','"+destino+"','0')"
    cursor.execute(consulta)
    db.commit()
    return "1"    


def activarU(codigo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="update usuarios set estado='1' where codigoactivacion='"+codigo+"'"
    cursor.execute(consulta)
    db.commit()
    
    consulta="select *from usuarios where codigoactivacion='"+codigo+"' and estado='1'"
    cursor.execute(consulta)
    return cursor.fetchall()

