import spacy

# Cargar el modelo de español
nlp = spacy.load("es_core_news_sm")

# Este diccionario lo hice pensando en guardar una sintaxis con la que trabajeremos, es decir, si en algunas de las peticiones aparece un dispositivo que no existe en el diccionario 'PROPN'
# No se hará la traducción
dict_NL = { "NOUN":['nodo','dispositivo','Computador','Router','Firewall','PC'],
            "PROPN": ['PC_Test_Server', 'Servidor', 'DMZ', 'FW', 'Switch0', 'Usuario', 'Jefe', 'Router0' , 'PC_Test_Internet','Internet','internet','Google', 'google'],
            "ADV":['si','no'],
            "VERB" :['acceder','salir','cambiar','bloquear','permitir','enviar','permitir','denegar'],
            "NUM" :["172.23.130.161","172.23.130.162", "172.23.130.163","172.22.130.1","172.23.130.2","172.23.130.3","200.75.19.161","200.75.19.161","8.8.8.1",
                    "8.8.8.1","172.168.130.1","172.168.130.2"]
}

words_to_change = [word for words in dict_NL.values() for word in words]
text = " ".join(words_to_change)
texto = input("Ingrese la peticion: ")
doc = nlp(texto) # Procesar el texto con spaCy

for token in doc:
    for pos, palabras in dict_NL.items():
        if token.text in palabras:
            token.pos_ = pos  # Cambiar la etiqueta POS a una conveniente

cantip = 0

# Etiquetar partes del discurso
for token in doc:
    if token.pos_ == "NUM":
        cantip+=1
    if token.dep_ == "ROOT":
        intencion = token.text.lower()


start_command = ['enable','configure terminal','show running-config','exit']

#Intrucciones de denegacion o permision de servicios

if intencion in dict_NL.get("VERB", []):
    if intencion == "bloquear" or intencion == "denegar":
        op_deny_permit = "deny"
    elif intencion == "acceder" or intencion == "permitir":
        op_deny_permit = "permit"
    else:
        print("No se puede crear la instrucción, ya que no hay una opción asociada a permitir o denegar servicios")
    interface = "FastEthernet"
    flag = True
    cambio = False
    inout = " in"
    if cantip == 1:
        for token in doc:
            if token.pos_ == "NUM":
                if token.text in dict_NL.get("NUM", []):
                    ip_address = token.norm_
                else:
                    flag = False
                    break
            if token.pos_=="PROPN" :
                if (token.text.lower() == "internet" or token.text.lower() == "google"):
                    access_group = "google"
                    interface = "GigabitEthernet1/3"
                    ip_dest = ' 8.8.8.8'
                elif token.text in dict_NL.get("PROPN", []):
                    access_group = "dmz_to_lan"
                    interface = "GigabitEthernet1/2"
                    if token.text == "Servidor":
                        ip_dest = "172.23.130.162"
                    elif token.text == "PC_Test_Server":
                        ip_dest = "172.23.130.163"
                    elif token.text == "Jefe":
                        ip_dest = "172.22.130.2"
                    elif token.text == "Usuario":
                        ip_dest = "172.22.130.3"
                    elif token.text == "PC_Test_Internet":
                        ip_dest = "172.168.130.2"
                        access_group = "google"
                        interface = "GigabitEthernet1/3"

            if token.pos_=="ADJ" and token.text=="entrante":
                cambio = True

        if cambio:
            aux = ip_address
            ip_address = ip_dest
            ip_dest = aux
            inout = " out"

        if flag:
            pickInterface_command = 'interface ' + interface
            accessListEditDeviceAny_command = 'access-list ' + access_group + " extended " + op_deny_permit + ' ip ' + ip_address +' '+ ip_dest
            changeAccessGroupInterface_command = 'ip access-group ' +  access_group + inout
            print(f'$ {start_command[1]}\n$ {accessListEditDeviceAny_command}\n$ {start_command[3]}\n$ {pickInterface_command}\n$ {changeAccessGroupInterface_command}\n$ {start_command[3]}')
        else:
            print("No se puede crear la instrucción, ya que la IP del dispositivo no existe en la red")
    
    elif cantip == 2:
        ips = []
        for token in doc:
            if token.pos_=="NUM":
                if token.text in dict_NL.get("NUM", []):
                    ips.append(token.text)
                else:
                    flag = False
                    break
            if token.pos_=="ADJ" and token.text=="entrante":
                cambio = True

        if cambio:
            ips.reverse()

        if ips[1] == "8.8.8.8" or ips[1] == "172.168.130.2":        
            access_group = "google"
            interface = "GigabitEthernet1/3"
        elif ips[1] in dict_NL.get("NUM", []):
            access_group = "dmz_to_lan"
            interface = "GigabitEthernet1/2"
        
        if flag:
            pickInterface_command = 'interface ' + interface
            accessListEditDeviceAny_command = 'access-list ' + access_group + " extended " + op_deny_permit + ' ip ' + ips[0] +' '+ ips[1]
            changeAccessGroupInterface_command = 'ip access-group ' +  access_group + inout
            print(f'$ {start_command[1]}\n$ {accessListEditDeviceAny_command}\n$ {start_command[3]}\n$ {pickInterface_command}\n$ {changeAccessGroupInterface_command}\n$ {start_command[3]}')
        else:
            print("No se puede crear la instrucción, ya que la IP del dispositivo no existe en la red")
    
    elif cantip==0:
        propn = []
        for token in doc:
            if token.pos_=="PROPN":
                if token.text in dict_NL.get("PROPN", []):
                    propn.append(token.text)
                else:
                    flag = False
                    break
            if token.pos_=="ADJ" and token.text=="entrante":
                cambio = True
        
        if cambio:
            propn.reverse()
        
        if propn[1].lower() == "internet" or propn[1].lower() == "google":
            access_group = "google"
            interface = "GigabitEthernet1/3"
        else:
            access_group = "dmz_to_lan"
            interface = "GigabitEthernet1/2"
        ips =[]
        for x in propn:
            if x.lower() == "internet" or x.lower() == "google":
                ips.append('8.8.8.8')
            elif x == "Servidor":
                ips.append("172.23.130.162")
            elif x == "PC_Test_Server":
                ips.append("172.23.130.163")
            elif x == "Jefe":
                ips.append("172.22.130.2")
            elif x == "Usuario":
                ips.append("172.22.130.3")
            elif x == "PC_Test_Internet":
                ips.append("172.168.130.2")
        
        if flag:
            pickInterface_command = 'interface ' + interface
            accessListEditDeviceAny_command = 'access-list ' + access_group + " extended " + op_deny_permit + ' ip ' + ips[0] +' '+ ips[1]
            changeAccessGroupInterface_command = 'ip access-group ' +  access_group + inout
            print(f'$ {start_command[1]}\n$ {accessListEditDeviceAny_command}\n$ {start_command[3]}\n$ {pickInterface_command}\n$ {changeAccessGroupInterface_command}\n$ {start_command[3]}')
        else:
            print("No se puede crear la instrucción, ya que la IP del dispositivo no existe en la red")
        
