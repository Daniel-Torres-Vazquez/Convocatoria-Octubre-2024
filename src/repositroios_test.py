from repositorios import *

def lee_repositorios_test(ruta):
    datos=lee_repositorios(ruta)[:2]
    for e in datos:
        print(e)

def total_commits_por_anyo_test(datos):
    print(total_commits_por_anyo(datos))

def n_mejo_test(datos):
    for e in n_mejores_repos_por_tasa_crecimiento(datos):
        print(e)

def recomendar_lenguajes_test(datos):
    info2=recomendar_lenguajes(datos, datos[30])
    info3=recomendar_lenguajes(datos, datos[4])
    print(info2)
    print(info3)

def media_min_test(datos):
    cla=media_minutos_entre_commits_por_usuario(datos)
    for e in cla:
        print(e,cla[e])

if __name__ == "__main__":
    ruta="./data/repositorios.csv"
    datos=lee_repositorios(ruta)
    #lee_repositorios_test(ruta)
    #total_commits_por_anyo_test(datos)
    #n_mejo_test(datos)
    #recomendar_lenguajes_test(datos)
    media_min_test(datos)