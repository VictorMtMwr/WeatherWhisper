const OPENCAGE_API_KEY = "097aba7edfda4d57b2810b642abd29f1";

window.onload = function () {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            console.log("Coordenadas obtenidas:", { latitude, longitude });

            const geocodeUrl = `https://api.opencagedata.com/geocode/v1/json?q=${latitude}+${longitude}&key=${OPENCAGE_API_KEY}`;

            fetch(geocodeUrl)
                .then(response => response.json())
                .then(geoData => {
                    if (geoData.results && geoData.results.length > 0) {
                        const city = geoData.results[0].components.city || geoData.results[0].components.town || geoData.results[0].components.village;

                        if (city) {
                            console.log("Ciudad obtenida de las coordenadas:", city);
                            document.getElementById("city-input").value = city;
                            fetchWeatherByCity(city); // Llamada para cargar los datos de clima al inicio
                        } else {
                            console.error("No se pudo determinar la ciudad a partir de las coordenadas.");
                        }
                    } else {
                        console.error("Error al obtener el nombre de la ciudad desde OpenCage.");
                    }
                })
                .catch(error => {
                    console.error("Error al realizar la geocodificación inversa:", error);
                });
        }, error => {
            console.error("Error de geolocalización:", error);
        });
    } else {
        console.error("La geolocalización no está soportada por este navegador.");
    }
};

document.getElementById("city-search-form").addEventListener("submit", function (event) {
    event.preventDefault();
    const city = document.getElementById("city-input").value;
    console.log(`Formulario enviado con la ciudad: ${city}`);
    fetchWeatherByCity(city);
});

function fetchWeatherByCity(city) {
    document.getElementById("city-name").textContent = "Cargando...";
    document.getElementById("temperature").textContent = "-- °C";

    const query = `/api/weather?city=${city}`;
    fetch(query)
        .then(response => {
            if (!response.ok) {
                throw new Error("Error en la respuesta de la API");
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                updateWeatherUI(data);
            }
        })
        .catch(error => {
            console.error("Error al obtener los datos del clima:", error);
        });
}

function updateWeatherUI(data) {
    // Actualización de los elementos de UI con la información del clima
    document.getElementById("city-name").textContent = data.city || "---------";
    document.getElementById("temperature").textContent = `${data.temperature || "--"} °C`;
    document.getElementById("humidity").textContent = `${data.humidity || "--"} %`;
    document.getElementById("precipitation").textContent = `${data.precipitation_probability || "--"} %`;
    document.getElementById("rainIntensity").textContent = `${data.rainIntensity || "--"} %`;
    document.getElementById("recommendation").textContent = data.recommendation || "Sin recomendación";
    document.getElementById("uvIndex").textContent = `${data.uv_index || "--"}`;
    document.getElementById("windSpeed").textContent = `${data.wind_speed || "--"} km/h`;
    document.getElementById("visibility").textContent = `${data.visibility || "--"} km`;
    document.getElementById("cloudCover").textContent = `${data.cloud_cover || "--"} %`;
    const coordinates = data.coordinates ? `Lat: ${data.coordinates[0]}, Lon: ${data.coordinates[1]}` : "--";
    document.getElementById("coordinates").textContent = coordinates;

    // Obtener la hora actual
    const currentHour = new Date().getHours();

    if (data.rainIntensity > 0.10) {
        document.body.style.backgroundImage = "url('/static/images/rain.jpg')";
    } else if (currentHour >= 18) {
        document.body.style.backgroundImage = "url('/static/images/night.jpg')";
    } else {
        document.body.style.backgroundImage = "url('/static/images/sky-background.jpg')";
    }

    updateWeatherIconAndDescription(data);
}


function updateWeatherIconAndDescription(data) {
    const icon = document.getElementById("weather-icon");
    const weatherDescription = document.getElementById("weather-description");
    const rainIntensity = data.rainIntensity || 0;
    const cloudCover = data.cloud_cover || 0;

    // Obtener la hora actual
    const currentHour = new Date().getHours();

    // Asignar el icono y la descripción de clima
    if (currentHour >= 18) {
        icon.className = "fas fa-moon"; // Luna
        weatherDescription.textContent = "Noche"; // Descripción para la noche
    } else {
        if (rainIntensity > 0 && cloudCover > 0) {
            icon.className = "fas fa-cloud-showers-heavy"; // Lluvia y nublado
            weatherDescription.textContent = "Lluvia y nublado"; // Descripción lluvia y nublado
        } else if (rainIntensity > 0) {
            icon.className = "fas fa-cloud-showers-heavy"; // Solo lluvia
            weatherDescription.textContent = "Lluvia"; // Descripción solo lluvia
        } else if (cloudCover > 20) {
            icon.className = "fas fa-cloud-sun"; // Nublado con sol
            weatherDescription.textContent = "Nublado con sol"; // Descripción nublado con sol
        } else if (data.description.toLowerCase() === "clear") {
            icon.className = "fas fa-sun"; // Soleado
            weatherDescription.textContent = "Soleado"; // Descripción soleado
        } else if (data.description.toLowerCase() === "partly cloudy") {
            icon.className = "fas fa-cloud-sun"; // Parcialmente nublado
            weatherDescription.textContent = "Parcialmente nublado"; // Descripción parcialmente nublado
        } else if (data.description.toLowerCase() === "cloudy" || data.description.toLowerCase() === "overcast") {
            icon.className = "fas fa-cloud"; // Nublado
            weatherDescription.textContent = "Nublado"; // Descripción nublado
        } else if (data.description.toLowerCase() === "thunderstorm") {
            icon.className = "fas fa-bolt"; // Tormenta
            weatherDescription.textContent = "Tormenta"; // Descripción tormenta
        } else if (data.description.toLowerCase() === "snow") {
            icon.className = "fas fa-snowflake"; // Nieve
            weatherDescription.textContent = "Nieve"; // Descripción nieve
        } else {
            icon.className = "fas fa-question"; // Desconocido
            weatherDescription.textContent = "Estado desconocido"; // Descripción desconocida
        }
    }
}
