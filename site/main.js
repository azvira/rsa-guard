document.addEventListener('DOMContentLoaded', function() {
    document.querySelector("form").addEventListener("submit", async function(event) {
        event.preventDefault();

        const serviceName = document.getElementById("service-name").value;
        const password = document.getElementById("password").value;
        const secretWord = document.getElementById("secret-word").value;

        const response = await fetch("http://localhost:8000/passwords/encrypt", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                service_name: serviceName,
                password: password,
                secret_word: secretWord
            })
        });

        const result = await response.json();

        if (response.ok) {
            alert("Пароль успешно зашифрован и сохранён!");
            console.log(result);
            document.getElementById('modal').style.display = 'none';

            // Очищаем поля формы
            document.getElementById("service-name").value = "";
            document.getElementById("password").value = "";
            document.getElementById("secret-word").value = "";

            // ДОБАВЛЯЕМ сервис в список
            addServiceToList(serviceName);
        } else {
            alert("Произошла ошибка при сохранении пароля.");
            console.error(result);
        }
    });
});

// Функция для добавления нового сервиса в список
function addServiceToList(serviceName) {
    const servicesList = document.getElementById('services-list');

    const serviceItem = document.createElement('div');
    serviceItem.className = 'service-item';  // ✅ Класс для стилей

    const nameSpan = document.createElement('span');
    nameSpan.textContent = serviceName;

    serviceItem.appendChild(nameSpan);
    servicesList.appendChild(serviceItem);
}

document.getElementById("check-btn").addEventListener("click", async function () {
    const serviceName = document.getElementById("modal-service-name").textContent.trim();
    const secretWord = document.getElementById("check-secret").value;

    if (!secretWord) {
        alert("Введите секретное слово!");
        return;
    }

    try {
        const response = await fetch("http://localhost:8000/passwords/decrypt", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                service_name: serviceName,
                secret_word: secretWord
            })
        });

        const result = await response.json();

        if (response.ok) {
            // Успешно расшифровали
            document.getElementById("decrypted-password").value = result.decrypted_password;
        } else {
            // Ошибка расшифровки
            alert(result.detail || "Ошибка при расшифровке пароля.");
            document.getElementById("decrypted-password").value = "";
        }
    } catch (err) {
        console.error("Ошибка при запросе к серверу:", err);
        alert("Ошибка подключения к серверу.");
    }
});

document.getElementById("delete-btn").addEventListener("click", async function () {
    const serviceName = document.getElementById("modal-service-name").textContent.trim();

    const confirmed = confirm(`Вы точно хотите удалить сервис "${serviceName}"?`);

    if (!confirmed) return;

    try {
        const response = await fetch("http://localhost:8000/passwords/delete", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ service_name: serviceName })
        });

        const result = await response.json();

        if (response.ok) {
            alert("Сервис удалён!");
            // Удаляем элемент из списка
            const items = document.querySelectorAll('.service-item');
            items.forEach(item => {
                if (item.textContent.trim() === serviceName) {
                    item.remove();
                }
            });

            // Закрываем модалку
            document.getElementById("view-modal").style.display = "none";
        } else {
            alert(result.detail || "Не удалось удалить сервис.");
        }
    } catch (err) {
        console.error("Ошибка при удалении:", err);
        alert("Ошибка подключения к серверу.");
    }
});


