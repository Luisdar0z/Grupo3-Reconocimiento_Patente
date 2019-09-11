import requests

files = {
	'username': (None, 'servidor'),
	'password': (None, 'Secrect.123'),
}
response = requests.post('http://localhost:8000/api/login', files=files)

headers = {
    'Authorization': 'Token 01c8574a530b397e9b20108271b82d3bf8c18906',
}

response = requests.get('http://localhost:8000/apiregistro/1/', headers=headers)

headers = {
    'Authorization': 'Token 01c8574a530b397e9b20108271b82d3bf8c18906',
}

response = requests.get('http://localhost:8000/apiregistro/', headers=headers)

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token 01c8574a530b397e9b20108271b82d3bf8c18906',
}

data = '{"vehiculo":4,"hora":"14:00","day":16,"month":10,"year":2019}'

response = requests.post('http://localhost:8000/apiregistro/', headers=headers, data=data)