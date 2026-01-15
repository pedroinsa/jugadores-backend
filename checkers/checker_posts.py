from fastapi import HTTPException


def validate_content_post(content: str):
    
    content_validation = content.strip()
    if len(content_validation) > 300:
        raise HTTPException(status_code=400, detail="El post no debe ser mayor a 300 caracteres")
    if len(content_validation)< 2:
        raise HTTPException(status_code=400, detail= "El post debe ser mayor a 2 caracteres")
    
    return content_validation


