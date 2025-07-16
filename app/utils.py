"""
Funciones utilitarias para respuestas estándar de la API.
Permiten devolver respuestas uniformes de éxito o error.
"""

def success_response(data=None, message="Success"):
    """
    Devuelve una respuesta de éxito estándar.
    :param data: Datos a incluir en la respuesta
    :param message: Mensaje opcional
    :return: Diccionario con estado, mensaje y datos
    """
    return {
        "status": "success",
        "message": message,
        "data": data
    }

def error_response(message="Error", status_code=400):
    """
    Devuelve una respuesta de error estándar.
    :param message: Mensaje de error
    :param status_code: Código de estado HTTP
    :return: Diccionario con estado, mensaje y código
    """
    return {
        "status": "error",
        "message": message,
        "code": status_code
    }