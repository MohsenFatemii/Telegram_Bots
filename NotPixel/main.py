from constants import *
import requests
import random
import authorization_handler

num_pixels_to_click = 2

def set_authorization():
    global HEADERS
    HEADERS['authorization'] = authorization_handler.get_authorization()

    if HEADERS['authorization'] is None:
        print('Failed to get authorization.')
        exit()
    else:
        print('Successfully obtained authorization.')


def paint_pixel(point, color):
    try:
        data = f'{{"pixelId":{point},"newColor":"{color}"}}'
        response = requests.post(f'{BASE_URL}/repaint/start', headers=HEADERS, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return None

def get_pixel_info(point):
    try:
        response = requests.get(f"{BASE_URL}/image/get/{point}", headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return None

if __name__ == '__main__':
    set_authorization()
    for i in range(num_pixels_to_click):
        print(paint_pixel(f"{random.randint(1,1_000_000)}", random.choice(COLORS)))
        