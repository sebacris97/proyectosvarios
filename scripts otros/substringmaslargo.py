
#retorna true si la cadena NO tiene caracteres repetidos
#retorna false si la cadena tiene caracteres repetidos
def valido(cadena):
    dic={}
    for i in cadena:
        if i in dic.keys():
            return False
        else:
            dic[i]=1
    return True


#substring mas largo es el substring de un string que no repite caraceteres
def substringmaslargo(cadena):
    if len(cadena) <= 2:
        return cadena
    maximo = cadena[:0]
    for i in range(len(cadena)):
        for k in range(i,len(cadena)+1):
            aux = cadena[i:k]
            if i==k or not valido(aux):
                continue
            print(str(i)+":"+str(k)+" = "+aux)
            if len(aux)>len(maximo):
                maximo=aux
    return maximo



cadena = input("ingrese una cadena: ")
print(substringmaslargo(cadena))



