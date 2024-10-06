import urllib3
import json

# Utworzenie instancji PoolManager
http = urllib3.PoolManager()

# Wykonanie żądania GET na podany URL
response = http.request('GET', "http://api.open-notify.org/iss-now.json")

# Wczytanie odpowiedzi jako JSON
obj = json.loads(response.data.decode('utf-8'))

# Wydrukowanie obiektu JSON
print(obj)
print(obj['timestamp'])
print(obj['iss_position']['latitude'], obj['iss_position']['longitude'])