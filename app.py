from datetime import datetime
from flask import Flask,render_template,request,redirect,url_for,session
import funciones
app = Flask(__name__)
# rutas
app.secret_key='mysecret_key'


from datetime import datetime
from flask import Flask,render_template,request,redirect,url_for,session
import bbdd as db
import funciones


app=Flask(__name__)
app.secret_key='mysecret_key'


parada=[]
@app.route("/")
def login():
    paradas=[]     
    cur = db.connection.cursor()
    # Execute a query
    cur.execute("SELECT nombre FROM tabla_index")
    resultado=cur.fetchall()
    for paradax in resultado:
      paradas+=paradax  
    cur.close()               
    return render_template('login.html',n_paradas=paradas)

@app.route("/new_data", methods=["POST"])
def new_data(): 
    global parada  
    parada = request.form['parada'].lower()
    cedula = request.form['cedula']
    password = request.form['clave']
    cur = db.connection.cursor()   
    query=f"SELECT cedula FROM {parada} WHERE cedula = '{cedula}' "
    cur.execute(query)
    result=cur.fetchall()
    if result != []:  
      cur.execute(f"SELECT password FROM tabla_index  WHERE nombre = '{parada}'" )
      ident=cur.fetchall() 
      for id in ident:   
       if password == id[0]:       
           cur.close()                       
           return redirect (url_for("info"))         

@app.route('/info') 
def info(): 
    fecha = datetime.strftime(datetime.now(),"%Y %m %d - %H:%M:%S")
    informacion=funciones.info_parada(parada)
    print(informacion)
    cabecera=funciones.info_cabecera(parada) 
    print(cabecera)
    cant = funciones.num_miembros(parada)
    print(cant)
    presidente=funciones.fun_miembros_p(parada)
    print(presidente)
    veedor=funciones.fun_miembro_v(parada)
    print(veedor)
    miembros=funciones.lista_miembros(parada)
    dirigencia= ('operativa',cant,presidente,veedor)
    return render_template('info.html',informacion=informacion,miembros=miembros,cabecera=cabecera,fecha=fecha,dirigentes=dirigencia) 

@app.route('/aportes') 
def aportes():
    return render_template('login_a.html',parada=parada)



@app.route('/finanzas', methods=["GET", "POST"]) 
def finanzas(): 
    fecha = datetime.strftime(datetime.now(),"%Y %m %d - %H:%M:%S")
    diario=funciones.diario_general(parada)
    return render_template('finanzas.html',diario=diario,fecha=fecha,parada=parada)

@app.route('/direccion') 
def direccion(): 
    return render_template('direccion.html')


@app.route('/administrar') 
def administrar():
    return render_template('login_dir.html')

@app.route('/login_a', methods =['GET', 'POST'])
def login_a():
    msg = ''
    account=[]
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account=funciones.logge_a(parada,password)                                       
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            fecha = datetime.strftime(datetime.now(),"%Y %m %d - %H:%M:%S")  
            informacion=funciones.info_parada(parada) 
            miembros=funciones.lista_miembros(parada)
            datos=funciones.aportacion(parada) 
            cabecera=funciones.info_cabecera(parada)
            return render_template('usuario.html',informacion=informacion,miembros=miembros,datos=datos,cabecera=cabecera,fecha=fecha)
        else:
            msg = 'Incorrecto nombre de usuario / password !'
    return render_template('login_a.html', msg = msg)


@app.route('/login_dir', methods =['GET', 'POST'])
def login_dir():
    msg = ''
    account=[]
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        query=f"SELECT * FROM usuarios WHERE nombre ='{username}' AND password = '{password}'"
        accounts = db.consultar_db(query) 
        for accountx in accounts:
          account +=accountx                                          
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            fecha = datetime.strftime(datetime.now(),"%Y %m %d - %H:%M:%S")  
            return render_template('index.html',fecha=fecha)
        else:
            msg = 'Incorrecto nombre de usuario / password !'
    return render_template('login_dir.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('info'))



@app.route('/nueva_p') 
def nueva_p(): 
    return render_template('direccion.html')
                           
                           
@app.route('/editar_p') 
def editar_p(): 
    return render_template('direccion.html')                           
                           
@app.route('/n_miembro') 
def n_miembro(): 
    return render_template('direccion.html')
                           
                           
@app.route('/editar_miembro') 
def editar_miembro(): 
    return render_template('direccion.html') 
 
 
                                    
@app.route("/data_cuotas", methods=["GET","POST"])
def data_cuotas():
    my_list=[];suma_no=[];suma_si=[]
    if request.method == 'POST':
       hoy = request.form['time']
       cant=request.form['numero']
       valor_cuota=request.form['valor']
       parada=request.form['parada']  
       for i in range(int(cant)): 
            my_list +=(request.form.getlist('item')[i],   
                       request.form.getlist('estado')[i],   
                       request.form.getlist('nombre')[i], 
                       request.form.getlist('documento')[i])     
       string=funciones.dividir_lista(my_list,4)     
       query=f'CREATE TABLE IF NOT EXISTS {parada}_cuota( item VARCHAR(50)  NULL, fecha VARCHAR(50)  NULL, estado VARCHAR(50)  NULL, nombre VARCHAR(50)  NULL, cedula VARCHAR(50)  NULL)' 
       db.modificar_db(query) 
              
       for data in string:
          query=f"INSERT INTO {parada}_cuota(item, fecha, estado, nombre, cedula) VALUES('{data[0]}', '{hoy}',  '{data[1]}', '{data[2]}', '{data[3]}')"
          db.modificar_db(query)   
     
       query=f"SELECT COUNT(estado) FROM {parada}_cuota WHERE estado = 'no_pago' "   
       suma=db.consultar_db(query)
       for num in suma:
        suma_no=num[0]    
       print(suma_no)
       
       
       query=f"SELECT COUNT(estado) FROM {parada}_cuota WHERE estado = 'pago' "   
       sumas=db.consultar_db(query)  
       for numb in sumas:
           suma_si=numb[0]
            
         
       n_aporte=int(suma_si) * float(valor_cuota)
       n_pendiente=int(suma_no) * float(valor_cuota)

       query=f"UPDATE tabla_index SET aporte={n_aporte}, pendiente={n_pendiente} WHERE nombre='{parada}'"
       db.modificar_db(query) 
                       
                                                         
       return redirect(url_for('data_confirmacion')) 

@app.route("/data_bancos",methods=["GET","POST"])
def data_bancos(): 
    if request.method == 'POST':
       hoy = request.form['time']
       parada=request.form['parada'] 
       nom_banco = request.form['nom_banco'] 
       t_cuenta = request.form['t_cuenta']
       n_cuenta = request.form['n_cuenta']
       balance_c = request.form['balance']       
       query = f"CREATE TABLE IF NOT EXISTS {parada}_banco( fecha VARCHAR(50)  NULL, banco VARCHAR(50) NULL, tipo_cuenta VARCHAR(50) NULL,  numero_cuenta VARCHAR(50) NULL, balance DECIMAl(10,2) unsigned DEFAULT 0)"                                                                                                                          
       db.modificar_db(query)
       
       query=f"INSERT INTO {parada}_banco(fecha, banco, tipo_cuenta, numero_cuenta, balance) VALUES('{hoy}', '{nom_banco}', '{t_cuenta}', '{n_cuenta}', {balance_c})"
       db.modificar_db(query)
                 
       query=f"UPDATE tabla_index SET balance_banco={balance_c} WHERE nombre='{parada}'"
       db.modificar_db(query)  
 
       return redirect(url_for('data_confirmacion'))   

@app.route("/data_gastos",methods=["POST"])
def data_gastos(): 
    n_gastos=[]
    hoy=request.form['time']
    descripcion_gastos = request.form['descripcion_g'] 
    cantidad_gastos = request.form['cantidad_g']
                
    query = f"CREATE TABLE IF NOT EXISTS {parada}_gastos( fecha VARCHAR(50)  NULL,descripcion_gastos VARCHAR(50) NULL, cantidad_gastos DECIMAl(10,2) unsigned DEFAULT 0)"                                                                                                                          
    db.modificar_db(query)
    
    query=f"INSERT INTO {parada}_gastos(fecha, descripcion_gastos, cantidad_gastos) VALUES('{hoy}', '{descripcion_gastos}', {cantidad_gastos})"
    db.modificar_db(query)
    
    query=f"SELECT SUM(cantidad_gastos) FROM  {parada}_gastos "
    suma=db.consultar_db(query) 
    for total in suma:
      n_gastos=total[0]           
    query=f"UPDATE tabla_index SET gastos={n_gastos} WHERE nombre='{parada}'"
    db.modificar_db(query)

    return redirect(url_for('data_confirmacion'))    
 
 
@app.route("/data_ingresos",methods=["POST"])
def data_ingresos(): 
    n_ingresos=[]

    hoy=request.form['time']
    descripcion_ingreso = request.form['descripcion_i'] 
    cantidad_ingreso = request.form['cantidad_i']   

    query = f"CREATE TABLE IF NOT EXISTS {parada}_ingresos( fecha VARCHAR(50)  NULL, descripcion_ingresos VARCHAR(50)  NULL, cantidad_ingresos DECIMAl(10,2) unsigned DEFAULT 0)"                                                                                                                          
    db.modificar_db(query)
    
    query=f"INSERT INTO {parada}_ingresos(fecha, descripcion_ingresos, cantidad_ingresos) VALUES('{hoy}', '{descripcion_ingreso}', { cantidad_ingreso})"
    db.modificar_db(query)
    
    query=f"SELECT SUM(cantidad_ingresos) FROM  {parada}_ingresos "
    suma=db.consultar_db(query) 
    for total in suma:  
     n_ingresos=total[0]
    
    query=f"UPDATE tabla_index SET ingresos={n_ingresos}  WHERE nombre='{parada}'"
    db.modificar_db(query)    
    return redirect(url_for('data_confirmacion'))        
              
@app.route("/data_prestamos",methods=["POST"])
def data_prestamos():            
       n_prestamos=[] 
       hoy=request.form['time']               
       prestamo = request.form['descripcion_p'] 
       monto = request.form['cantidad_p']
       
       query = f"CREATE TABLE IF NOT EXISTS {parada}_prestamos( fecha VARCHAR(50)  NULL, prestamo_a VARCHAR(50)  NULL, monto_prestamo DECIMAl(10,2) unsigned DEFAULT 0 )"                                                                                                                          
       db.modificar_db(query)
       
       query=f"INSERT INTO {parada}_prestamos(fecha, prestamo_a, monto_prestamo) VALUES('{hoy}',  '{prestamo}', {monto})"
       db.modificar_db(query)
             
       query=f"SELECT SUM(monto_prestamo) FROM  {parada}_prestamos "
       suma=db.consultar_db(query) 
       for total in suma:
         n_prestamos=total[0]   
       
       query=f"UPDATE tabla_index SET prestamos={n_prestamos}  WHERE nombre='{parada}'"
       db.modificar_db(query)      
             
       return redirect(url_for('data_confirmacion')) 

@app.route("/data_abonos",methods=["POST"])
def data_abonos():               
       n_abonos=[]
       abono_persona=[]
       prestamo=[] 
       balance_prestamos=[]
       hoy=request.form['time']       
       abono_a = request.form['descripcion_a'] 
       cantidad_a = request.form['cantidad_a']  

       query = f"CREATE TABLE IF NOT EXISTS {parada}_abonos( fecha VARCHAR(50)  NULL,  abono_a VARCHAR(50)  NULL, monto_abono DECIMAl(10,2) unsigned DEFAULT 0, balance_prestamo DECIMAl(10,2) unsigned DEFAULT 0)"                                                                                                                          
       db.modificar_db(query)
       
       query=f"INSERT INTO {parada}_abonos(fecha, abono_a, monto_abono) VALUES('{hoy}', '{abono_a}', {cantidad_a})"
       db.modificar_db(query)
             
       query=f"SELECT SUM(monto_abono) FROM  {parada}_abonos "
       suma=db.consultar_db(query) 
       for total in suma: 
         n_abonos=total[0]


       query=f"SELECT SUM(monto_abono) FROM  {parada}_abonos WHERE abono_a='{abono_a}' "
       suma=db.consultar_db(query) 
       for total in suma: 
         abono_persona=total[0]
   
       query=f"SELECT monto_prestamo FROM  {parada}_prestamos WHERE prestamo_a = '{abono_a}' "
       prestado=db.consultar_db(query) 
       for pres in prestado:
           prestamo=pres[0]           
       
       if prestamo==[] or prestamo== 0:
        query=f"UPDATE {parada}_abonos SET balance_prestamo = 0.0 "
        db.modificar_db(query)
       else:
       
        balance_prestamos=float(prestamo) - float(abono_persona)                
        query=f"UPDATE {parada}_abonos SET balance_prestamo = {balance_prestamos} WHERE abono_a = '{abono_a}' AND fecha = '{hoy}' "
        db.modificar_db(query)   

       query=f"UPDATE tabla_index SET abonos={n_abonos} WHERE nombre='{parada}'"
       db.modificar_db(query)       
       

       return redirect(url_for('data_confirmacion')) 

@app.route("/diario_pdf", methods=['POST'])
def finanza():
    return redirect(url_for('data_confirmacion')) 

@app.route("/list_miembros_pdf", methods=['POST'])
def miembros_pdf():
    miembros=funciones.lista_miembros(parada)
    miembros_pdf(parada,miembros)
    return redirect(url_for('data_confirmacion')) 

@app.route("/data_confirmacion", methods=["POST"])
def data_confirmacion():
         informacion=funciones.info_parada(parada) 
         miembros=funciones.lista_miembros(parada)
         diario=funciones.diario_general(parada)
         datos=funciones.aportacion(parada) 
         hoy = datetime.strftime(datetime.now(),"%Y %m %d - %H:%M:%S")
         cabecera=funciones.info_cabecera(parada)  
         return render_template("/administradores.html",informacion=informacion,miembros=miembros,diario=diario,datos=datos,cabecera=cabecera,fecha={hoy})
        
@app.route("/respuestos", methods=["GET","POST"])
def respuestos():
    return render_template('respuestos.html') 

@app.route("/respuestos", methods=["GET","POST"])
def prestamos():
    return render_template('prestamos.html') 

@app.route("/respuestos", methods=["GET","POST"])
def celulares():
    return render_template('celulares.html') 

@app.route("/respuestos", methods=["GET","POST"])
def electrodomescos():
    return render_template('electrodomesticos.html')       

@app.route("/respuestos", methods=["GET","POST"])
def oferta():
    return render_template('ofertas.html') 

@app.route("/respuestos", methods=["GET","POST"])
def regreso():
    return redirect(url_for('login'))  


@app.route("/respuestos", methods=["GET","POST"])
def msg():
  nombre=request.form['nombre']
  correo=request.form['correo']
  telefono=request.form['telefono']    
  return redirect(url_for('login'))

# bloque de prueba
if __name__ == "__main__":
    app.run(debug=False)
    
