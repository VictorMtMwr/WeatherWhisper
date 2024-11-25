document.getElementById('city-search-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar recargar la página

    const city = document.getElementById('city-input').value;

    // Hacer la solicitud a la API
    fetch(`http://localhost:5002/recommendation?city=${city}`)
    .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error); // Mostrar un mensaje de error si hay problemas con la API
            } else {
                // Actualizar los elementos HTML con los datos de la API
                document.getElementById('city-name').innerText = data.city;
                document.getElementById('weather-description').innerText = "Descripción del clima"; // Puedes ajustar según lo que devuelva la API
                document.getElementById('temperature').innerText = `${data.temperature}°`;
                document.getElementById('recommendation').innerText = data.recommendation;
                document.getElementById('humidity').innerText = `${data.humidity}%`;
                document.getElementById('uv-index').innerText = `UV: ${data.uv_index}`;

                // Actualizar más datos según la estructura de la respuesta de la API
                // Ejemplo para la humedad y el índice UV (si están disponibles en la API)
                // document.getElementById('humidity').innerText = `${data.humidity}%`;
                // document.getElementById('uv-index').innerText = `UV: ${data.uv_index}`;
            }
        })
        .catch(error => console.error('Error al obtener los datos del clima:', error));
});