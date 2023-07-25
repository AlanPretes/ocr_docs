import requests
import base64
import re
import time


def encontrar_padrao(lista_strings):
    placas_encontradas = []
    mercosul = re.compile(r'^[A-Z]{3}[0-9][A-Z]{1}[0-9]{2}$')
    mercosul_erro_0_cortado = re.compile(r'^[A-Z]{5}[0-9]{2}$')
    mercosul_erro_i = re.compile(r'^[A-Z]{3}[0-9]{4}$')
    mercosul_erro_B = re.compile(r'^[A-Z]{3}[0-9]{4}$')
    
    ################ SE FOR CARRO/CAMINHAO ##################
    contador = 1
    for string in lista_strings[1:]:
        string = str(string).replace(" ", "")
        string_car = string[0:7]
                
        # Trata erro do 0 cortado:
        if mercosul_erro_0_cortado.match(string_car):
            if string_car[3] == "G":
                string_car = string_car[:3] + "0" + string_car[4:]
            else:
                pass
            
        # Trata erro do B:
        if mercosul_erro_B.match(string_car):
            if string_car[4] == "8":
                string_car = string_car[:4] + "B" + string_car[5:]
            else:
                pass

        # Trata erro do I com 1:
        if mercosul_erro_i.match(string_car):
            if string_car[4] == "1":
                string_car = string_car[:4] + "I" + string_car[5:]
            else:
                pass
            
        # Se achar placa adiciona na lista de placas encontradas
        if mercosul.match(string_car):
            placas_encontradas.append(string_car)
        

        ################ SE FOR MOTO ##################
        limite = len(lista_strings)
        if contador in range(0, limite-1):
            if contador == 0:
                contador += 1
            string_concat = f"{string}{lista_strings[contador+1]}"
            string_concat = str(string_concat).replace(" ", "")
            print(string_concat)
            contador += 1
            
            # Trata erro do 0 cortado
            if mercosul_erro_0_cortado.match(string_concat):
                if string_concat[3] == "G":
                    string_concat = string_concat[:3] + "0" + string_concat[4:]
                else:
                    pass
                
            # Trata erro do B:
            if mercosul_erro_B.match(string):
                if string[4] == "8":
                    string = string[:4] + "B" + string[5:]
                else:
                    pass
            
            # Trata erro do I com 1
            if mercosul_erro_i.match(string_concat):
                if string_concat[4] == "1":
                    string_concat = string_concat[:4] + "I" + string_concat[5:]
                else:
                    pass
                
            # Se achar placa adiciona na lista de placas encontradas
            if mercosul.match(string_concat):
                placas_encontradas.append(string_concat)
                
    placas_encontradas = list(set(placas_encontradas))
    return placas_encontradas