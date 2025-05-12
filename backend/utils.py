from rsa_guard.rsa import *
import os
import json


def get_data(service: str, enc_priv_key: str, enc_password: str) -> dict[str, str]:
    data = {
        "service": service,
        "enc_priv_key": enc_priv_key,
        "enc_password": enc_password
    }
    return data


def save_data(data: dict[str,list], filename: str) -> dict[str, list[str]]:
    service = data["service"]
    enc_priv_key = data["enc_priv_key"]
    enc_password = data["enc_password"]

    entry = [enc_priv_key, enc_password]

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            full_data = json.load(f)
    else:
        full_data = {}

    full_data[service] = entry

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(full_data, f, indent=4)

    return full_data






    



