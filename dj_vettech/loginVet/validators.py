from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re

NAME_REGEX = r'^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s\-]+$'
name_validator = RegexValidator(regex=NAME_REGEX,message='Ingrese solo letras, espacios y guiones. Ej: José María')
PHONE_REGEX = r'^3\d{2}\s?\d{3}\s?\d{4}$'
phone_validator = RegexValidator(regex=PHONE_REGEX,message='Teléfono celular inválido. Formato: 300 123 4567')
CEDULA_REGEX = r'^\d{6,10}$'
cedula_validator = RegexValidator(regex=CEDULA_REGEX,message='Cédula inválida. Ingrese sin puntos ni espacios (6-10 dígitos).')
CURRENCY_REGEX = r'^\d{1,18}([\.,]\d{1,2})?$'
currency_validator = RegexValidator(regex=CURRENCY_REGEX,message='Formato de moneda inválido. Ej: 1234567 o 1234567.89')
def calculate_nit_dv(nit_body: str) -> int:
    weights = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]
    reversed_digits = list(map(int, nit_body[::-1]))
    total = sum(d * weights[i] for i, d in enumerate(reversed_digits) if i < len(weights))
    remainder = total % 11
    dv = 11 - remainder
    if dv == 11:
        return 0
    if dv == 10:
        return 1
    return dv
def validate_nit(value):
    v = re.sub(r'[^0-9]', '', str(value))
    if len(v) < 2:
        raise ValidationError('NIT inválido.')
    nit_body = v[:-1]
    try:
        dv = int(v[-1])
    except ValueError:
        raise ValidationError('Dígito de verificación inválido.')
    calc = calculate_nit_dv(nit_body)
    if calc != dv:
        raise ValidationError('Dígito de verificación del NIT no coincide.')
