from fastapi import HTTPException
import re
import string
def check_username (username: str):
    if " " in username:
        raise HTTPException(status_code=400, detail="Username no debe tener espacios")    
    if len(username) > 25  or len(username)< 4:
        raise HTTPException(status_code=400, detail="Username debe contener entre 4 y 25 caracteres")
    if not username.startswith(tuple(string.ascii_letters)):
        raise HTTPException(status_code=400, detail="Username debe comenzar con una letra")
    if not re.match(r'^[a-zA-Z0-9._]+$', username):
        raise HTTPException(status_code=400, detail="Tiene caracteres incorrectos")
    if username.endswith((".","_")):
        raise HTTPException(status_code=400, detail="Username debe terminar con números o letras")
    if re.search(r"(.)\1{2,}", username):
        raise HTTPException(status_code=400, detail="Los caracteres no pueden repetirse 3 veces o más")
    if username.lower() in ("admin", "user", "superadmin", "player","jugador","usuario","administrador"):
        raise HTTPException(status_code=400, detail="Prohibido uso de palabras reservadas")
    
    return username.lower()

def check_email (email: str):
   char_forbidden = ("á","é","í","ó","ú","ñ", "Á" ,"É","Í" ,"Ó","Ú","Ñ")

   if not "@" in email:
      raise HTTPException(status_code=400, detail="Debe contener un @")   
   fragments = email.split("@")
   parts = fragments[1].split(".")
         
   if " " in email:
        raise HTTPException(status_code=400, detail="Email no debe tener espacios")   

   if not re.match(r'^[a-zA-Z0-9ñÑáéíóúÁÉÍÓÚüÜ._%+-]+@[a-zA-Z0-9ñÑáéíóúÁÉÍÓÚüÜ.-]+\.[a-zA-Z]{2,}$', email):
       raise HTTPException(status_code=400, detail="Email con formato inválido")
   for char in char_forbidden:
       if char in email:
           raise HTTPException(status_code=400, detail=f"Usar {char} no esta permitido")
       
   if len(email) > 50 or len (email) < 8:
       raise HTTPException(status_code=400, detail="Email debe tener entre 8 y 50 caracteres")
   if fragments[0].startswith((".","_","%","+","-" )) :
       raise HTTPException(status_code= 400, detail= "Email debe comenzar con letras o números")
   if fragments[0].endswith((".")):
       raise HTTPException(status_code=400, detail="Formato inválido")
   if fragments[1].startswith((".","-")):
       raise HTTPException(status_code=400, detail="El dominio del email debe comenzar con letras")
   if re.search(r"(.)\1{2,}", fragments[0]) or re.search(r"(.)\1{3,}", fragments[1]):
       raise HTTPException(status_code=400, detail="No puedes repetir tantos caracteres seguidos")
   if re.search(r"\.{2,}", fragments[1]):
       raise HTTPException(status_code=400, detail= "El dominio no puede tener puntos consecutivos" )
   for part in parts:
       if part.startswith("-") or part.endswith("-"):
           raise HTTPException(status_code=400, detail="Dominio con formato inválido")
       if not re.search(r"[a-zA-Z]", part):
           raise HTTPException( status_code=400, detail="Dominio debe tener al menos una letra")
       
   return email.lower()



def check_password (password: str):
    forbidden_chars = ['"', "'", '\\', "`", "<",">","^", "[","]", "=",";"]

    if " " in password:
        raise HTTPException(status_code=400, detail="La contraseña no puede tener espacios en blanco")
    if len(password) > 25 or len(password) < 8 :
        raise HTTPException(status_code=400, detail="La contraseña debe tener entre 8 y 25 caracteres")
    if not re.search(r'[a-záéíóúñ]',password):
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos una letra minúscula")
    if not re.search(r'[A-ZÁÉÍÓÚÑ]', password) :
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos una letra mayúscula")
    if not re.search(r'[0-9]', password):
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos un número")
    for char in forbidden_chars:
        if char in password:
            raise HTTPException(status_code=400, detail= f"La contraseña tiene el siguiente carácter restringido: {char}") 
    if not re.search(r'[!@#$%^&*(),.?":{}|+-]', password):
         raise HTTPException(status_code=400, detail="La contraseña debe tener al menos un carácter especial")
    
    return password