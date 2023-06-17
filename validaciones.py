import re

ImportError


def alfabetico(avalidar):
    patron = "^[A-Za-z]*$"

    cadena = avalidar
    if re.match(patron, cadena):
        reg = cadena.upper()
        #print("alfabetico valido", reg)
        return reg

    else:
        reg = False
        #print("alfabetico no valido")


def numerico(avalidar):
    patron = "^[0-9]+$"

    cadena = avalidar

    if re.match(patron, cadena):
        reg = int(cadena)
        #print("validado numerico")

        return reg
    else:
        reg = False
        #print(reg, "REG numerico false")
        return reg


def alfanumerico(avalidar):
    patron = "^[A-Za-z\d ]*$"

    cadena = avalidar

    if re.match(patron, cadena):
        reg = cadena.upper()
        #print("validado")

        return reg

    else:
        reg = False
        #print(reg, "reg alfanumerico no valdidado")
        #print(type(reg))
        return reg


alfanumerico("22")
numerico("2234")
alfabetico("fernando sergio ")
print("''" * 8)
alfanumerico("  22")
alfanumerico("!")
numerico("f")
alfabetico("f ")
