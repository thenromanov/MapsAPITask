import requests


def getScale(*corners):
    lowerCorners = [tuple(map(float, corner[0])) for corner in corners]
    upperCorners = [tuple(map(float, corner[1])) for corner in corners]
    result = (max([upperCorner[0] for upperCorner in upperCorners]) - min([lowerCorner[0] for lowerCorner in lowerCorners]),
              max([upperCorner[1] for upperCorner in upperCorners]) - min([lowerCorner[1] for lowerCorner in lowerCorners]))
    return result


def getCenter(*coords):
    xs = [float(coord[0]) for coord in coords]
    ys = [float(coord[1]) for coord in coords]
    return [sum(xs) / len(xs), sum(ys) / len(ys)]


def getLength(point1, point2):
    lat1, long1 = radians(point1[0]), radians(point1[1])
    lat2, long2 = radians(point2[0]), radians(point2[1])
    cl1, cl2 = cos(lat1), cos(lat2)
    sl1, sl2 = sin(lat1), sin(lat2)
    delta = long2 - long1
    cdelta, sdelta = cos(delta), sin(delta)
    y = sqrt(pow(cl2 * sdelta, 2) + pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    return round(atan2(y, x) * 6372795)


def getAddresses(address):
    geocoderServer = 'http://geocode-maps.yandex.ru/1.x/'
    geocoderParams = {
        'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
        'geocode':  address,
        'format': 'json'}
    response = requests.get(geocoderServer, params=geocoderParams)
    if response:
        return response.json()
    else:
        return None


def getAddressCoords(address):
    try:
        jsonResponse = getAddresses(address)
        toponym = jsonResponse['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        requestCoords = list(map(float, toponym['Point']['pos'].split()))
        toponymCorners = jsonResponse['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['boundedBy']['Envelope']
        lowerCorner = list(map(float, toponymCorners['lowerCorner'].split()))
        upperCorner = list(map(float, toponymCorners['upperCorner'].split()))
        return [requestCoords, lowerCorner, upperCorner]
    except Exception:
        return None


def getAddressDistrict(address):
    try:
        coords = getAddressCoords(address)[0]
        geocoderServer = 'http://geocode-maps.yandex.ru/1.x/'
        geocoderParams = {
            'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
            'geocode':  ','.join(map(str, coords)),
            'kind': 'district',
            'format': 'json'}
        jsonResponse = requests.get(geocoderServer, params=geocoderParams).json()
        return jsonResponse['response']['GeoObjectCollection']
        ['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']
        ['Components'][-1]['name']
    except Exception:
        return None


def getOrganizations(text, coords):
    searchServer = 'https://search-maps.yandex.ru/v1/'
    searchParams = {
        'apikey': 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3',
        'text': text,
        'lang': 'ru_RU',
        'll': '{},{}'.format(coords[0], coords[1]),
        'type': 'biz'
    }
    response = requests.get(searchServer, params=searchParams)
    if response:
        return response.json()
    else:
        return None


def getOrganizationInfo(organization):
    try:
        info = {'name': organization['properties']['CompanyMetaData']['name'],
                'address': organization['properties']['CompanyMetaData']['address'],
                'time': None,
                'coords': organization['geometry']['coordinates'],
                'corners': organization['properties']['boundedBy']}
        if 'Hours' in organization['properties']['CompanyMetaData'].keys():
            info['time'] = organization['properties']['CompanyMetaData']['Hours']['text']
        return info
    except Exception:
        return None


if __name__ == '__main__':
    print('Hello! This is my map module!')
