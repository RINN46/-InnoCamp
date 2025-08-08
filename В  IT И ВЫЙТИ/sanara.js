document.addEventListener('DOMContentLoaded', function() {
    // Регистрация
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async function(event) {
            event.preventDefault();

            const name = document.getElementById('register-name').value;
            const email = document.getElementById('register-email').value;
            const password = document.getElementById('register-password').value;
            const confirmPassword = document.getElementById('register-confirm-password').value;

            if (password !== confirmPassword) {
                alert('Пароли не совпадают.');
                return;
            }

            try {
                const response = await fetch('/register/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `username=${encodeURIComponent(name)}&email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`
                });
                
                if (response.ok) {
                    // После успешной регистрации перенаправляем на страницу входа
                    window.location.href = 'sanara.html';
                } else {
                    const errorData = await response.json();
                    alert(errorData.detail || 'Ошибка регистрации');
                }
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при регистрации');
            }
        });
    }

    // Вход
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(event) {
            event.preventDefault();

            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;

            try {
                const response = await fetch('/login/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`
                });
                
                if (response.ok) {
                    // После успешного входа перенаправляем на welcome страницу
                    window.location.href = 'welcome.html';
                } else {
                    const errorData = await response.json();
                    alert(errorData.detail || 'Ошибка входа');
                }
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при входе');
            }
        });
    }
});