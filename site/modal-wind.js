// Открытие модального окна
function openModal() {
    const modal = document.getElementById('modal');
    modal.style.display = 'flex';
}

// Закрытие модального окна при клике вне области окна
window.onclick = function(event) {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
};

// Показываем второе модальное окно при клике на сервис
document.addEventListener('click', function(event) {
    const item = event.target.closest('.service-item');
    if (item) {
        const serviceName = item.textContent.trim(); // получаем имя сервиса

        // Устанавливаем заголовок
        document.getElementById('modal-service-name').textContent = serviceName;

        // Очищаем поля
        document.getElementById('check-secret').value = "";
        document.getElementById('decrypted-password').value = "";

        // Показываем модалку
        document.getElementById('view-modal').style.display = 'flex';
    }
});

document.getElementById('view-modal').addEventListener('click', function(event) {
    const modalContent = document.getElementById('view-modal-content');
    if (!modalContent.contains(event.target)) {
        document.getElementById('view-modal').style.display = 'none';
    }
});

