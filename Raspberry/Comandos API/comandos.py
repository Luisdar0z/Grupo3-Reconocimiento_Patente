import requests
import json

#Agregar Datos
def Agregar(_id, _hora, _day, _month, _year):
    print("imprimiendo desde comandos: ")
    print(_id)
    print(_hora)
    print(_day)
    print(_month)
    print(_year)


    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token 01c8574a530b397e9b20108271b82d3bf8c18906',
    }

    #data = "vehiculo=",_id , "hora="+_hora + "day=",_day, "month=",_month, "year="+_year   

    data = {
        "vehiculo": _id,
        "hora": _hora,
        "day": _day,
        "month": _month,
        "year": _year
    }
    
    data_convert = json.dumps(data)

    response = requests.post('http://localhost:8000/apiregistro/', headers=headers, data=data_convert)