#!/usr/bin/env python3

import json
import pathlib
import requests


AUTH_TOKEN = '***FILL_ME_IN***' # DigitalOcean API token
PROJECT_ID = '***FILL_ME_IN***' # ID of the project to place the droplet under


def getFileContents(relative_path: str) -> str:
    path = (pathlib.Path(__file__).parent / relative_path).resolve()

    with open(path) as f:
        return f.read()


droplet_config = json.loads(getFileContents('droplet-config.json'))
droplet_config['user_data'] = getFileContents('cloud-config.yml')

r = requests.post(
    'https://api.digitalocean.com/v2/droplets',
    headers={'Authorization': f'Bearer {AUTH_TOKEN}'},
    json=droplet_config
)

response = r.json()
droplet_id = response['droplet']['id']

r = requests.post(
    f'https://api.digitalocean.com/v2/projects/{PROJECT_ID}/resources',
    headers={'Authorization': f'Bearer {AUTH_TOKEN}'},
    json={"resources": [f"do:droplet:{droplet_id}"]}
)

print(r.json())
