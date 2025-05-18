document.getElementById('generate-btn').addEventListener('click', async () => {
    const prompt = document.getElementById('prompt').value.trim();
    const suggestionsDiv = document.getElementById('suggestions');
    const suggestionsList = document.getElementById('suggestions-list');
    const errorMessage = document.getElementById('error-message');

    if (!prompt) {
        errorMessage.textContent = 'Please enter a gift idea.';
        errorMessage.classList.remove('hidden');
        suggestionsDiv.classList.add('hidden');
        return;
    }

    errorMessage.classList.add('hidden');
    suggestionsList.innerHTML = '<li>Loading...</li>';
    suggestionsDiv.classList.remove('hidden');

    try {
        const response = await fetch('/suggestion/generate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ prompt }),
        });

        const data = await response.json();
        suggestionsList.innerHTML = '';

        if (response.ok) {
            data.suggestions.forEach(suggestion => {
                const li = document.createElement('li');
                li.textContent = suggestion;
                suggestionsList.appendChild(li);
            });
        } else {
            errorMessage.textContent = data.error || 'An error occurred.';
            errorMessage.classList.remove('hidden');
            suggestionsDiv.classList.add('hidden');
        }
    } catch (error) {
        errorMessage.textContent = 'Network error. Please try again.';
        errorMessage.classList.remove('hidden');
        suggestionsDiv.classList.add('hidden');
    }
});

function getCSRFToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}