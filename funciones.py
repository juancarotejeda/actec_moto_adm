

import bbdd as db

def logger():
    paradas=[]     
    cur = db.cursor()
    # Execute a query
    resultado=cur.execute("SELECT nombre FROM tabla_index")
    for paradax in resultado:
      paradas+=paradax  
    return paradas  

def logger_a(parada,password):
    account=[]
    query=f"SELECT password FROM tabla_index WHERE nombre ='{parada}'"
    accounts =consultar_db(query) 
    for accountx in accounts:
     account += accountx 
    return account


def verificacion1(parada,cedula) :  
  cur = db.connection.cursor()   
  cur.execute(F"SELECT  cedula  FROM  {parada} WHERE nombre = '{cedula}' ")
  result=cur.fetchone()
  print(result) 
  if result != []: 
      return True 
  else:
      return False  
    
def verificacion2(parada,password):  
    clave=[]
    query=f"SELECT password FROM tabla_index  WHERE nombre = '{parada}'" 
    ident=consultar_db(query) 
    for id in ident:
      clave=id[0]      
    if password == clave:  
       return True        

    
def adm_verificacion(parada,adm_d,adm_p):
    clave=[]
    query=f"SELECT adm_password FROM tabla_index  WHERE nombre = '{parada}'" 
    ident=consultar_db(query)
    for dato in ident:
      clave = dato[0]
    if clave == adm_p :
      query=f"SELECT cedula FROM {parada}  WHERE funcion = 'Presidente'" 
      ids=consultar_db(query)
      for idx in ids: 
        id=idx[0] 
      if id == adm_d:
        return True 
    else:
       return False 
   
        
def listado_paradas():
    query="SELECT nombre FROM tabla_index " 
    db_paradas=consultar_db(query)       
    return db_paradas

def info_parada(parada):
    query=f"SELECT * FROM  tabla_index  WHERE nombre='{parada}'" 
    infos=consultar_db(query)      
    return infos

def info_cabecera(parada):
    query=f"SELECT cuota, pago FROM tabla_index WHERE nombre = '{parada}'"
    resp=consultar_db(query)
    for repueta in resp:
      cuota=repueta[0]  
      pago=repueta[1]
      return(cuota,pago) 
    
def num_miembros(parada):        
    query=f'SELECT nombre FROM {parada}'
    seleccion=consultar_db(query)
    cant=len(seleccion)
    return cant
    
def fun_miembros_p(parada): 
    presidente = []       
    query=f'SELECT nombre FROM {parada}  WHERE funcion = "Presidente"'   
    press=consultar_db(query)
    for pres in press:
      presidente=pres[0] 
    return presidente 

def fun_miembro_v(parada):  
    veedor = []
    query=f'SELECT nombre FROM {parada}  WHERE funcion = "Veedor"'   
    presd=consultar_db(query)
    for prex in presd:
      veedor=prex[0] 
    return veedor               
     

def lista_miembros(parada):
    listas=[]
    query=f"SELECT codigo, nombre, cedula, telefono, funcion FROM {parada}"
    miembros=consultar_db(query)
    for miembro in miembros: 
        listas+=miembro
    lista=dividir_lista(listas,5)    
    return lista
    
def diario_general(parada):
    prestamos=[]
    ingresos=[]
    gastos=[]
    aporte=[]
    pendiente=[]
    abonos=[]
    balance_bancario=[]
    query = f"SELECT  prestamos, ingresos, gastos, aporte, pendiente, abonos, balance_banco FROM tabla_index WHERE nombre='{parada}' "   
    consult=consultar_db(query)
    for valor in consult:
      prestamos=valor[0]
      ingresos=valor[1]
      gastos=valor[2]
      aporte=valor[3]
      pendiente=valor[4]
      abonos=valor[5]
      balance_bancario=valor[6]
    balance=(aporte + ingresos + abonos )-(gastos+prestamos)
    data=(balance,prestamos,ingresos,gastos,aporte,pendiente,abonos,balance_bancario)   
    return data

def dividir_lista(lista,lon) : 
    return [lista[n:n+lon] for n in range(0,len(lista),lon)]     


def aportacion(parada):                
    query=f"SELECT codigo, nombre, cedula, telefono, funcion FROM {parada}"
    data=consultar_db(query)
    return data
  
def modificar_db(query): 
  cursor= db.connection.cursor() 
  cursor.execute(query)     
  db.connection.commit()
  return

def consultar_db(query):
    cursor= db.connection.cursor()
    cursor.execute(query)
    Result= cursor.fetchall() 
    return Result    