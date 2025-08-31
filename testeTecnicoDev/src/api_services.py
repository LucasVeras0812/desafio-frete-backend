import requests

def coordenadas_cep(cep: str) -> tuple:
    url = f"https://brasilapi.com.br/api/cep/v2/{cep}"

    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()

        coordenadas = dados.get("location", {}).get("coordinates", {})
        latitude = coordenadas.get("latitude")
        longitude = coordenadas.get("longitude")

        if latitude and longitude:
            return(latitude, longitude)
        else:
            raise ValueError(f"Coordenada digitada ({cep}) não foi encontrada.")
        
    elif response.status_code == 404:
        raise ValueError(f"CEP ({cep}) não foi encontrado.")
    else:
        raise Exception(f"Erro ao buscar valores na API: {response.status_code}")
    
def calcular_distancia_coordenada(lat_origem, lon_origem, lat_destino, lon_destino) -> float:
    url = f"https://router.project-osrm.org/route/v1/driving/{lon_origem},{lat_origem};{lon_destino},{lat_destino}"
    
    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()

        distancia_metros = dados.get("routes", [{}])[0].get("distance")

        if distancia_metros is not None:
            distancia_km = distancia_metros / 1000
            return round(distancia_km, 2)
        else: 
            raise ValueError("Nao foi possivel calcular as rotas.")
    else:
        raise Exception(f"Ërro ao buscar valores na API: {response.status_code}")