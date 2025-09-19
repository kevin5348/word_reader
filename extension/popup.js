document.getElementById("login").addEventListener("click", async () => {
    const loginButton = document.getElementById("login");
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    loginButton.disabled = true;
    loginButton.textContent = "Logging in...";

    // check if email and password are provided
    if (!email || !password) {
        alert('Please enter both email and password');
        return;
    }
    // send login request to server
    try {
        const response = await fetch('http://localhost:5000/login', {
            method: 'Post',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        if (response.ok) {
            // Save the token in localStorage
            chrome.storage.local.set({ 'auth_token': data.token }, () => {
                console.log('Token stored successfully');
                showLoggedInView();
            });

        } else {
            console.error('Login failed:', data.error);
            alert('Login failed: ' + data.error);
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred during login. Please try again.');
    } finally {
        loginButton.disabled = false;
        loginButton.textContent = "Login";
    }
});
//refresh token function
async function refreshToken() {
    const result = await chrome.storage.local.get(['auth_token']);
    if (result.auth_token) {
        try {
            const response = await fetch('http://localhost:5000/refresh', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ token: result.auth_token })
            });

            const data = await response.json();
            if (response.ok) {
                chrome.storage.local.set({ 'auth_token': data.token });
                return data.token;
            } else {
                chrome.storage.local.remove('auth_token');
                return null;
            }
        } catch (error) {
            console.error('Token refresh failed:', error);
            return null;
        }
    }
}
// Check if the token is valid when popup opens
document.addEventListener("DOMContentLoaded", async () => {
    const result = await chrome.storage.local.get(['auth_token']);
    if (result.auth_token) {
        const newToken = await refreshToken();
        if (newToken) {
            showLoggedInView();
        } else {
            showLoginView();
        }
    }
});
// two different views for logged in and login
function showLoggedInView() {
    document.getElementById('login-view').style.display = 'none';
    document.getElementById('logged-in-view').style.display = 'block';
}
function showLoginView() {
    document.getElementById('login-view').style.display = 'block';
    document.getElementById('logged-in-view').style.display = 'none';
}
// Logout functionality
document.getElementById("logout").addEventListener("click", async () => {
    const { auth_token } = await chrome.storage.local.get(['auth_token']);
    try {
        await fetch('http://localhost:5000/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...(auth_token ? { 'Authorization': 'Bearer ' + auth_token } : {})
            },
            body: JSON.stringify({ logged_out: true })
        });
    }
    catch (e) {
        console.error('logout failed')
    }
    finally {
        chrome.storage.local.remove('auth_token', () => {
            console.log('Logged out successfully');
            showLoginView();
        });
    }
});