from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import (BaseModel)
from rsa_guard.rsa import *
from backend.utils import *
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем запросы со всех сайтов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PasswordRequest(BaseModel):  # запрос пароля
    service_name: str
    password: str
    secret_word: str


class EncryptRequest(BaseModel):  # Зашифровать запрос
    password: str
    service_name: str
    secret_word: str


class DecryptRequest(BaseModel):
    service_name: str
    secret_word: str


class DeleteRequest(BaseModel):
    service_name: str


@app.post("/passwords/encrypt")
def encrypt_entered_password(req: EncryptRequest) -> dict[str, list[str]]:
    """
        🔐 Шифрует пароль для указанного сайта с использованием секретного слова.
        Сохраняет результат в базу данных.
        Возвращает зашифрованный пароль.

        Использование:
        - Пользователь хочет сохранить пароль к сайту, но в зашифрованном виде.
        - Пароль никогда не хранится в открытом виде.
        """

    enc_priv_key, public_key = generate_keys(req.secret_word)
    enc_password = encrypt_password(req.password, public_key)
    service_name = req.service_name

    filename = "/Users/irinaazarova/Documents/курсовая/rsa-guard/backend/password.json"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            full_data = json.load(f)
        if service_name in full_data:
            raise HTTPException(status_code=400, detail=f"Сервис '{service_name}' уже существует.")
    else:
        full_data = {}

    data = get_data(service_name, enc_priv_key, enc_password)
    full_data = save_data(data, "/Users/irinaazarova/Documents/курсовая/rsa-guard/backend/password.json")

    return full_data


@app.post("/passwords/decrypt")
def decrypt_entered_password(req: DecryptRequest) -> dict[str, str]:
    """
    🔓 Расшифровывает зашифрованный пароль, используя секретное слово.
    Возвращает оригинальный пароль в открытом виде.

    Использование:
    - Когда нужно восстановить пароль для сайта.
    - Пользователь вводит секретное слово, и сервер расшифровывает пароль.
    """
    filename = "/Users/irinaazarova/Documents/курсовая/rsa-guard/backend/password.json"

    with open(filename, "r", encoding="utf-8") as f:
        full_data = json.load(f)

    if req.service_name not in full_data:
        raise HTTPException(status_code=404, detail="Сервис не найден.")

    service_data = full_data[req.service_name]
    enc_priv_key = service_data[0]
    enc_password = service_data[1]

    try:
        password = decrypt_password(enc_password, enc_priv_key, req.secret_word)
    except Exception:
        raise HTTPException(status_code=403, detail="Неверное секретное слово или ошибка расшифровки.")

    return {"decrypted_password": password}


@app.delete("/passwords/delete")
def delete_password(req: DeleteRequest):
    filename = "/Users/irinaazarova/Documents/курсовая/rsa-guard/backend/password.json"
    with open(filename, "r", encoding="utf-8") as f:
        full_data = json.load(f)

    if req.service_name not in full_data:
        raise HTTPException(status_code=404, detail="Сервис не найден")

    del full_data[req.service_name]

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(full_data, f, ensure_ascii=False, indent=4)

    return {"status": "ok"}


