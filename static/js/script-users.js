// VERIFICATION - код проверки для регистрации
document.getElementById('send-code-button').addEventListener('click', function() {
    var email = document.getElementsByName('email')[0].value;

    fetch(sendVerificationCodeUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ 'email': email })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Код отправлен на вашу почту');
        } else {
            alert('Ошибка отправки кода: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
});