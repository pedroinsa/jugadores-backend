from fastapi import HTTPException
from datetime import datetime, date
import schemas
import re

#Capitalize each word in the string except for certain prepositions
def enhanced_capitalizer (text: str):
    initial_words = text.split(" ")
    prepositions = ("de","la","del", "y")
    final_words = []
    for i,value in enumerate(initial_words):
        if i == 0:
            final_words.append(value.capitalize())
        elif value in  prepositions:
            final_words.append(value)
        else:
            final_words.append(value.capitalize()) 

    return " ".join(final_words)           
#Validates that there are no consecutive white spaces
def validate_separated_string(field,value):
    if re.search(r'\s{2,}', value):
         raise HTTPException(status_code=400, detail=f"El campo {field } no puede tener espacios en blanco consecutivos")
     
#Validates that there are no white spaces    
def validate_non_separated_string (field, value):
    if " " in value:
        raise HTTPException(status_code=400, detail=f"el campo {field} no puede tener espacios en blanco")     


#Validate strings that contain letters, spaces, periods(.), and numbers

def validate_letters_spaces_dots_numbers(field: str ,value:str):
    if not re.search (r"^[a-zA-Z0-9ñÑáéíóúÁÉÍÓÚüÜ.]+(?: [a-zA-Z0-9ñÑáéíóúÁÉÍÓÚüÜ.]+)*$", value ):
        raise HTTPException(status_code=400, detail=f"El campo {field} tiene formato inválido")
    if value.startswith("."):
        raise HTTPException(status_code=400, detail=f"El campo {field} no puede comenzar con un punto")
    if value.endswith("."):
        raise HTTPException(status_code=400, detail=f"El campo {field} no puede terminar con un punto")
    if ".." in value:
        raise HTTPException(status_code=400, detail= f"El campo {field} no puede tener puntos consecutivos ")

 #Validates strings that contain lettes numbers and dot
def validate_letters_spaces_dots(field: str, value: str):
    if not re.search (r"^[a-zA-Z0-9ñÑáéíóúÁÉÍÓÚüÜ.]+(?: [a-zA-Z0-9ñÑáéíóúÁÉÍÓÚüÜ.]+)*$", value ):
        raise HTTPException(status_code=400, detail=f"El campo {field} tiene formato inválido")
    if value.startswith("."):
        raise HTTPException(status_code=400, detail=f"El campo {field} no puede comenzar con un punto")
    if ".." in value:
        raise HTTPException(status_code=400, detail= f"El campo {field} no puede tener puntos consecutivos")
    if re.search(r"\d{5,}"):
        raise HTTPException(status_code=400, detail= f"El campo {field} no puede contener tantos números seguidos")


 #Validates strings that contain letters and numbers
def validate_letters_spaces(field: str, value: str):
     if not re.search( r"^[a-zA-ZñÑáéíóúÁÉÍÓÚüÜ ]+$", value):
         raise HTTPException(status_code=400, detail=f"El campo {field} tiene formato inválido")
#validates a string that contains only letters."
def validate_letters (field: str, value: str):
      if not re.search(r"^[a-zA-ZñÑáéíóúÁÉÍÓÚüÜ]+$", value):
         raise HTTPException(status_code=400, detail=f"El campo {field} tiene formato inválido")

def validate_numbers_season(field: str, value: str):
      if not re.search(r"^[0-9/]*$", value) :
          raise HTTPException(status_code=400, detail=f"El campo {field} tiene formato inválido")
      if not value.startswith("2"):
          raise HTTPException(status_code=400, detail=f"El campo {field} tiene formato inválido ")  
      if "//" in  value:
          raise HTTPException(status_code=400, detail= f"El campo {field} no puede tener barras consecutivas")
      if value.startswith("/") or value.endswith("/"):
          raise HTTPException(status_code=400, detail= f"El campo {field} no puede comenzar ni terminar con barra")
      
# validates that the age is over 15                   

def validate_datetime_birth(field: str, birthday: date):

    
    today = date.today()
    age = today.year - birthday.year - ((today.month,today.day)< (birthday.month, birthday.day))
    if age >= 15:
        return True
    else:
        raise HTTPException(status_code=400, detail=f"En el campo {field} debe ingresar una edad mínima de 15 años")
    
##################################### main functions ####################
#capitalize and strip function   
def capitalize_and_strip(player: schemas.PlayerPostData | schemas.PlayerUpdate, capitalize_fields: tuple ):
     key_values = {}
     for key, value in player.model_dump().items():
         if key in capitalize_fields:
            key_values[key] = enhanced_capitalizer(value.strip().lower())
         elif isinstance(value, str):
             key_values[key] = value.strip().lower().capitalize()
         else:
            key_values[key] = value

     return key_values     

#The function handles whitespace in different ways.  
def check_white_spaces(key_values: dict, separated_string_fields: tuple):
     for key, value in key_values.items():
        if key in separated_string_fields:
            validate_separated_string(key,value)
        elif isinstance(value, str):
            validate_non_separated_string(key,value) 

# The function validates each field individually
def field_validation (key_values: dict, validate_functions: dict):
       
        for key, value in key_values.items():
           validator = validate_functions.get(key)
           if validator:
                validator(key, value)
            
#The function validates the maximum and minimum length

def length_validator(key_values: dict, max_length_group: dict, min_length_group: dict):
    for key, max_length in max_length_group.items():
         value = key_values.get(key)
         if isinstance(value, str) and len(value) > max_length:
             raise HTTPException(status_code=400, detail= f"El campo {key} no puede tener más de {max_length} caracteres" )   
    for key, min_length in min_length_group.items():
         value = key_values.get(key)
         if isinstance(value, str) and len(value) < min_length:
             raise HTTPException(status_code=400, detail=f"El campo {key} no puede tener menos de {min_length} caracteres")            