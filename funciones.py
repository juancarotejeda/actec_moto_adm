

import bbdd as db
          
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
  cur= db.connection.cursor() 
  cur.execute(query)     
  db.connection.commit()
  cur.close()
  return

def consultar_db(query):
    cur= db.connection.cursor()
    cur.execute(query)
    Result= cur.fetchall() 
    cur.close()
    return Result    