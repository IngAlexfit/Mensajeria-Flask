from flask import Flask, render_template, request
import hashlib
import controlador as controlador
from datetime import datetime
import envioemail

app = Flask(__name__)

email_origen=""

@app.route("/")
def hello_world():
    return render_template("login.html")

@app.route("/verifciarUsuario",methods=["GET","POST"])
def verifciarUsuario():
    
    correo=request.form["txtusuario"]
    password=request.form["txtpass"]
    
    password2=password.encode()
    password2=hashlib.sha384(password2).hexdigest()
    
    respuesta=controlador.consultar_usuario(correo, password2)
    respuesta2=controlador.consultar_cuentvalida(correo, password2)
    print("respuesssssst",respuesta2)

    global email_origen

    
    if len(respuesta)==0:
       mensajes= "Error de autenticacion, veririfique su usuario y contraseña."
       return render_template("informacion.html",data=mensajes)

    if len(respuesta2)==0 :
       mensajes= "Por favor, verifique su cuenta "
       info="El codigo de verificacion lo encontrara en su bandeja de entrada o en correo no deseado"
       return render_template("Validacion.html")
    else:
        return render_template("principal.html")
    
    
    
@app.route("/registrarUsuario",methods=["GET","POST"])
def registrarUsuario():
    if request.method=="POST":
        nombre=request.form["txtnombre"]
        correo=request.form["txtusuario2registro"]
        password=request.form["txtpassregistro"]
        password2=password.encode()
        password2=hashlib.sha384(password2).hexdigest()
        codigo=datetime.now()
        codigo2=str(codigo)
        codigo2=codigo2.replace("-","")
        codigo2=codigo2.replace(":","")
        codigo2=codigo2.replace(".","")
        codigo2=codigo2.replace(" ","")

        respuesta1=controlador.consultar_usuarios(nombre)
        respuesta2=controlador.consultar_correo(correo)
        print("user ",respuesta1)
        if len(respuesta1) != 0 and len(respuesta2) != 0 :
           mensajes= "Error de registro, Ya existe un Usuario  con los datos ingresados"
           return render_template("informacion.html",data=mensajes)
        elif len(respuesta1) != 0 and len(respuesta2) == 0:
           mensajes= "Error de registro, Ya existe un Usuario  con el usuario ingresado"
           return render_template("informacion.html",data=mensajes)
        elif len(respuesta2) != 0 and len(respuesta1) == 0:   
           mensajes= "Error de registro, Ya existe un Usuario  con el correo ingresado"
           return render_template("informacion.html",data=mensajes)
        else:
            controlador.registrar_usuarios(nombre,correo,password2,codigo2)

            envioemail.enviaractivacion(correo,codigo2)

            mensajes= "Usuario registrado satisfactoriamente."
            mensajes2= "Por Favor, revisar bandeja de correo no deseado" 
            return render_template("informacion.html",data=mensajes,data2=mensajes2)

@app.route("/enviarMail",methods=["GET","POST"])
def enviarMail():
    if request.method=="POST":
        emailDestino=request.form["emailDestino"]    
        asunto=request.form["asunto"]    
        mensaje=request.form["mensaje"]        
        controlador.registrar_email(email_origen,emailDestino,asunto,mensaje)
        mensaje2="Sr Usuario usted recibio un mensaje nuevo, por favor ingrese a la plataforma para observar su email, en la pestaña Historial. \n\n Muchas gracias."
        envioemail.enviar (emailDestino,mensaje2,"Nuevo mensaje enviado")
        return "Email enviado satifactoriamente"    


@app.route("/ActivarUsuario",methods=["GET","POST"])
def ActivarUsuario():
    
    codigo=request.form["txtcodigo"]
    
    respuesta=controlador.activarU(codigo)
    if len(respuesta)==0:
        mensajes= "El codigo es incorrecto"
        return render_template("informacion.html",data=mensajes)
    else:
        mensajes= "Usuario Activado con EXITO"
        return render_template("informacion.html",data=mensajes)



@app.route("/HistorialEnviados",methods=["GET","POST"])
def HistorialEnviados():
    resultado=controlador.ver_enviados(email_origen)
    return render_template("respuesta.html",data=resultado)        
    
@app.route("/HistorialRecibidos",methods=["GET","POST"])
def HistorialRecibidos():
    resultado=controlador.ver_recibidos(email_origen)
    return render_template("respuesta.html",data=resultado) 
    
    
