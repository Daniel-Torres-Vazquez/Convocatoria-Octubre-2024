#11:20
from collections import defaultdict
from typing import NamedTuple,List,Set,Tuple,Dict,Optional, Counter
from datetime import datetime,date
import csv
 
Commit = NamedTuple("Commit",      
       [("id", str), # Identificador alfanumérico del commit 
        ("mensaje", str), # Mensaje asociado al commit 
        ("fecha_hora", datetime) # Fecha y hora en la que se registró el commit 
       ]) 
Repositorio = NamedTuple("Repositorio",      
      [("nombre", str),  # Nombre del repositorio 
       ("propietario", str), # Nombre del usuario propietario 
       ("lenguajes", Set[str]),  # Conjunto de lenguajes usados 
       ("privado", bool),  # Indica si es privado o público 
       ("commits", List[Commit])  # Lista de commits realizados 
       ]) 


def parsea_commits(commits_str: str) -> List[Commit]:
    res=[]
    if commits_str != "[]":
        commits_str=commits_str.split(";")
        for e in commits_str:
            e=e.strip("[")
            e=e.strip("]")
            e=e.split("#")
            id,msg,fecha=e
            fecha=datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
            res.append(Commit(id,msg,fecha))
    return res

            


def lee_repositorios(csv_filename: str) -> List[Repositorio]:
    res=[]
    with open(csv_filename, encoding="UTF-8")as f:
        datos=csv.reader(f)
        next(datos)
        for repositorio, propietario, lenguajes, privado, commits in datos:
            lenguajes=lenguajes.split(",")
            privado= privado=="True"
            commits=parsea_commits(commits)
            res.append(Repositorio(repositorio, propietario, lenguajes, privado, commits))
    return res
            
#11:53

def total_commits_por_anyo(repositorios:List[Repositorio])->Dict[int, int]:
    res=Counter(i.fecha_hora.year for e in repositorios for i in e.commits if e.privado==False)
    return res

#12:00

def calcular_tasa_crecimiento(repositorio: Repositorio) -> float:
    
    if len(repositorio.commits)<2:
        res = 0
    else:
        rep1=repositorio.commits[len(repositorio.commits)-1]
        rep2=repositorio.commits[0]
        dias_trans=(rep1.fecha_hora - rep2.fecha_hora).days
        if dias_trans==0:
            res = 0
        else:
            res=len(repositorio.commits)/dias_trans
    return res
#12:30 pausa
#15:30
def n_mejores_repos_por_tasa_crecimiento(repositorios: List[Repositorio], n:Optional[int]=3)->List[Tuple[str,float]]:
    res=[]
    for e in repositorios:
        flo=calcular_tasa_crecimiento(e)
        st=e.nombre
        res.append((st, flo))
    return sorted(res, key=lambda x: x[1],reverse=True)[:n]  
#15:40 

def recomendar_lenguajes (repositorios:List[Repositorio], repositorio:Repositorio)->Set[str]:
    res=set()
    for e in repositorios:
        for i in repositorio.lenguajes:
            if i in e.lenguajes:
                for o in e.lenguajes:
                    res.add(o)
    for u in repositorio.lenguajes:
        res.discard(u)
    return res

#16:00

def media_minutos_entre_commits(lista_commits: List[Commit]) -> float:
    """Recibe una lista de tuplas de tipo Commit, y devuelve la media 
    de minutos entre cada dos commits consecutivos en el tiempo, por lo que, previamente, deberá 
    ordenar dichos commits . Si la lista tiene menos de dos elementos, la función devolverá None.  """
    if len(lista_commits)<2:
        return None
    media=[]
    for e, o in zip(lista_commits, lista_commits[1:]):
        dt1,dt2=e.fecha_hora,o.fecha_hora
        tiempo=(dt2-dt1).total_seconds()/60
        media.append(tiempo)
    media=sum(media)/len(media)
    return media


def media_minutos_entre_commits_por_usuario (repositorios:List[Repositorio], fecha_ini:Optional[date]=None, fecha_fin:Optional[date]=None)->Dict[str, float]: 
    """Dada una lista de tuplas de tipo Repositorio, una 
fecha inicial y una fecha final (ambas opcionales con valor por defecto None), devuelve un diccionario en el 
que las claves son los nombres de los propietarios de los repositorios, y los valores la media de minutos entre 
los commits realizados en los repositorios de cada propietario dentro del intervalo de fechas dado por 
[fecha_ini, fecha_fin). Si fecha_ini es None no se restringe el inicio del intervalo, y si fecha_fin es None, no se 
limita el final del intervalo. Si ambas fechas son None, se consideran todos los commits sin restricción 
temporal.  
Es importante tener en cuenta que un mismo propietario puede tener varios repositorios, por lo que los 
cálculos abarcarán todos los commits realizados en los repositorios de ese propietario dentro del intervalo 
especificado.  """
    res=defaultdict(list)
    vamba=[]
    if (fecha_ini==None) & (fecha_fin==None):
        for e in repositorios:
            media=media_minutos_entre_commits(e.commits)
            if media!=None:
                res[e.propietario].append(media)
    elif(fecha_ini==None):
        for e in repositorios:
            if (e.commits[-1]).fecha_hora<fecha_fin:
                media=media_minutos_entre_commits(e.commits)
                res[e.propietario].append(media)
    elif(fecha_fin==None):
        for e in repositorios:
            if e.commits[0].fecha_hora>=fecha_ini:
                media=media_minutos_entre_commits(e.commits)
                res[e.propietario].append(media)
    else:
        for i in repositorios:
            for u in i.commits:
                if fecha_ini<=u.fecha_hora<fecha_fin:
                    vamba.append(u)
                media=media_minutos_entre_commits(vamba)
                if media!=None:
                    res[i.propietario].append(media)
    
    for e in res:
        if len(res[e])>0:
            res[e]= sum(res[e])/len(res[e])
    return res