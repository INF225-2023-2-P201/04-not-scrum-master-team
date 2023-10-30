import spacy

# Cargar el modelo de español
nlp = spacy.load("es_core_news_sm")

#Funcion para verificar si un string es una direccion ip
def es_direccion_ip(cadena):
    partes = cadena.split('.')
    
    if len(partes) != 4:
        return False
    
    for parte in partes:
        valor = int(parte)
        if valor < 0 or valor > 255:
            return False
    return True




# Este diccionario lo hice pensando en guardar una sintaxis con la que trabajeremos, es decir, si en algunas de las peticiones aparece un dispositivo que no existe en el diccionario 'PROPN'
# No se hará la traducción
dict_NL = { "NOUN":['nodo','dispositivo','Computador','Router','Firewall','PC','vlan','VLAN'],
            "PROPN": ['PC_Test_Server', 'Servidor', 'DMZ', 'FW', 'Switch0', 'Usuario', 'Jefe', 'Router0' , 'PC_Test_Internet','Internet','internet','Google', 'google',
                      'FastEthernet0/0','FastEthernet0/1', 'FastEthernet0','FastEthernet1/1', 'FastEthernet2/1','FastEthernet1/0','FastEthernet6/0','GigabitEthernet1/1',
                      'GigabitEthernet1/2','GigabitEthernet1/3'],
            "ADV":['si','no'],
            "VERB" :['acceder','salir','cambiar','bloquear','permitir','enviar','permitir','denegar','crear','editar','agregar','quitar','agregarla','quitarla'],
            "NUM" :["172.23.130.161","172.23.130.162", "172.23.130.163","172.22.130.1","172.22.130.2","172.22.130.3","200.75.19.161","200.75.19.161","8.8.8.1",
                    "8.8.8.8","172.168.130.1","172.168.130.2"]
}

red = [["Jefe","172.22.130.2","255.255.255.0"],["Usuario","172.22.130.3","255.255.255.0"],["PC_Test_Server","172.23.130.163","255.255.255.240"],["Servidor","172.23.130.162","255.255.255.240"],["PC_Test_Internet","172.168.130.2","255.255.255.0"]] 
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
    if es_direccion_ip(token.text):
        cantip+=1
    if token.dep_ == "ROOT":
        intencion = token.text.lower()


start_command = ['enable','configure terminal','show running-config','exit']

#Intrucciones de denegacion o permision de servicios

if intencion in dict_NL.get("VERB", []):
    if intencion == "bloquear" or intencion == "denegar":
        op_deny_permit = "deny"
        instruccion = 1
    elif intencion == "acceder" or intencion == "permitir":
        op_deny_permit = "permit"
        instruccion = 1
    elif intencion == "enviar" or intencion == "mandar" or intencion == "hacer":
        instruccion = 2
    elif intencion == "crear" or intencion == "editar":
        instruccion = 3

    elif intencion == "cambiar":
        instruccion = 4

    if instruccion == 1:
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
                        ip_dest = '8.8.8.8'
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

    # ping o mensaje a otro dispositivo
    elif instruccion == 2:
        i = 0
        for token in doc:
            if token.text in dict_NL.get("PROPN", []) and i==1:
                if (token.text.lower() == "internet" or token.text.lower() == "google"):
                    ip_dest = '8.8.8.8'
                elif token.text == "Servidor":
                    ip_dest="172.23.130.162"
                elif token.text == "PC_Test_Server":
                    ip_dest="172.23.130.163"
                elif token.text == "Jefe":
                    ip_dest="172.22.130.2"
                elif token.text == "Usuario":
                    ip_dest="172.22.130.3"
                elif token.text == "PC_Test_Internet":
                    ip_dest="172.168.130.2"
            elif token.text in dict_NL.get("PROPN", []):
                i+=1      
        print('ping ' + ip_dest)
        
        
    # código de edición de vlan    
    elif instruccion == 3:
        validate = False
        addquit = bool
        interfaces = []
        if intencion in dict_NL.get("VERB", []):
            if intencion == "crear" or intencion == "editar":
                for token in doc:
                    if token.pos_ == "NOUN":
                        if token.text in dict_NL.get("NOUN", []):
                            validate = True
                    if token.pos_ == "PROPN" and validate:
                        if "vlan" in token.text.lower():
                            vlanId = token.text[4:]
                    if token.pos_ == "VERB":
                            if token.text in dict_NL.get("VERB", []):
                                if token.text == "agregar" or token.text == "agregarla":
                                    addquit = True
                                elif token.text == "quitar" or token.text == "quitarla":
                                    addquit = False
                    if "Fast" in token.text or "Gigabit" in token.text:
                            interfaces.append(token.text)
                if validate:
                    vlanInput_command = 'vlan' + vlanId
                    switchportModeAccess_command = 'switchport mode access'
                    switchportModeAccessVlan_command = 'switchport access vlan ' + vlanId
                    print(f'$ {start_command[1]}\n$ vlan {vlanId}')
                    for interface in interfaces:
                        print(f'$ interface {interface}\n$ {switchportModeAccess_command}\n$ {switchportModeAccessVlan_command}')
                    print('$ exit')
    
    # código cambio de ip
    elif instruccion == 4:
        flag = True
        if cantip == 1:
            for token in doc:
                if token.text.count(".") == 3:
                    ip_address = token.text
                elif token.text in dict_NL.get("PROPN", []):
                    for j in red:
                        if j[0] == token.text:
                            nodo = j
            ip = nodo[1].split(".")
            mask = int(nodo[2].split(".")[3])
        elif cantip == 2:
            nodo =[]
            for token in doc:
                if token.text in dict_NL.get("NUM", []):
                    for j in red:
                        if j[1] == token.text:
                            nodo = j
                elif token.text.count(".") == 3:
                    ip_address = token.text
            if len(nodo) == 0:
                print("La ip que se intenta cambiar no existe")
                flag = False
            else:
                ip = nodo[1].split(".")
                mask = int(nodo[2].split(".")[3])
        else:
           flag = False
           print("No se encontraron ips validas en el mensaje proporcionado")
    
        if flag:
            flag2 = True
            partes_ip = ip_address.split(".")

            if  mask < int(partes_ip[3]) < 255 and partes_ip[:3]== ip[:3]:
                for j in red:
                    if ip_address == j[1]:
                        print("La ip ya se encuentra utilizada")
                        flag2 = False
                        break
                if flag2:
                    print(f"Se esta cambiando la ip del nodo {nodo[0]}\n")
                    print(f"${start_command[1]} \n$ip address {ip_address} {nodo[2]}")
            else:
                print("No se puede utilizar la ip entregada")




