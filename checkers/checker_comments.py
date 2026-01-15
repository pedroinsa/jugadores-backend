from fastapi import HTTPException


def validate_content_comment(content: str):
    
    content_validation = content.strip()
    if len(content_validation) > 200:
        raise HTTPException(status_code=400, detail="El comentario no debe ser mayor a 200 caracteres")
    if len(content_validation)< 2:
        raise HTTPException(status_code=400, detail= "El comentario debe ser mayor a 2 caracteres")
    
    return content_validation


