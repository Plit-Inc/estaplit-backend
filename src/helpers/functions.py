import math

def get_distance(lat1, lon1, lat2, lon2):
    """
    Calcula a distância em metros entre dois pontos na Terra
    usando a fórmula de Haversine.
    
    Args:
        lat1 (float): Latitude do ponto 1 em graus.
        lon1 (float): Longitude do ponto 1 em graus.
        lat2 (float): Latitude do ponto 2 em graus.
        lon2 (float): Longitude do ponto 2 em graus.
    
    Returns:
        float: Distância entre os pontos em metros.
    """
    # Raio médio da Terra em metros
    earth_radius = 6371000.0

    # Converte graus para radianos
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Diferenças de latitude e longitude
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Fórmula de Haversine
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distância em metros
    distance = earth_radius * c

    return distance
