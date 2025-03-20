document.addEventListener('DOMContentLoaded', function() {
    // Your code here
});

document.addEventListener('DOMContentLoaded', function() {
    const weatherForm = document.getElementById('weatherForm');
    weatherForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting the traditional way
        const city = document.getElementById('cityInput').value;
        fetchWeatherData(city);
    });
});

function fetchWeatherData(city) {
    fetch(`/weather?city=${encodeURIComponent(city)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                displayError(data.error);
            } else {
                displayWeather(data);
            }
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
            displayError('Failed to retrieve weather data.');
        });
}

function displayWeather(data) {
    const weatherContainer = document.getElementById('weatherContainer');
    weatherContainer.innerHTML = `
        <h2>Weather in ${data.city}</h2>
        <p>Temperature: ${data.temperature}°C</p>
        <p>Condition: ${data.condition}</p>
        <p>Humidity: ${data.humidity}%</p>
        <p>Wind Speed: ${data.wind_speed} km/h</p>
    `;
}

function displayError(message) {
    const weatherContainer = document.getElementById('weatherContainer');
    weatherContainer.innerHTML = `<p class="error">${message}</p>`;
}

