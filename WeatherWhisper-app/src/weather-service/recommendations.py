def recommendation(temperature, precipitation_probability, wind_speed, uv_index, rain_intensity):
    """Proporciona una recomendación de vestimenta basada en la temperatura, probabilidad de precipitación, velocidad del viento, índice UV e intensidad de lluvia."""
    
    # Recomendaciones basadas en la temperatura
    if temperature == "No disponible":
        temp_recommendation = "No se pudo obtener una recomendación de vestimenta por falta de datos de temperatura."
    elif temperature < 0:
        temp_recommendation = "Usa un abrigo pesado, guantes, una bufanda y ropa térmica."
    elif 0 <= temperature < 15:
        temp_recommendation = "Usa una chaqueta cálida, pantalones largos y un suéter."
    elif 15 <= temperature < 25:
        temp_recommendation = "Una chaqueta ligera o suéter y pantalones largos son adecuados."
    else:
        temp_recommendation = "Vístete con una camiseta ligera y shorts."

    # Recomendaciones basadas en la probabilidad de precipitación e intensidad de lluvia
    if rain_intensity > 0:
        precipitation_recommendation = " Está lloviendo, lleva un impermeable, paraguas y calzado impermeable."
    elif precipitation_probability == "No disponible":
        precipitation_recommendation = ""
    elif precipitation_probability > 70:
        precipitation_recommendation = " Lleva un impermeable o paraguas, ya que es muy probable que llueva."
    elif 30 < precipitation_probability <= 70:
        precipitation_recommendation = " Podría llover, considera llevar una chaqueta impermeable."
    else:
        precipitation_recommendation = " Es poco probable que llueva, pero siempre es bueno estar preparado."

    # Recomendaciones basadas en la velocidad del viento
    if wind_speed == "No disponible":
        wind_recommendation = ""
    elif wind_speed > 30:
        wind_recommendation = " Hace bastante viento, usa una chaqueta cortaviento y considera una bufanda."
    elif 15 < wind_speed <= 30:
        wind_recommendation = " Puede haber algo de viento, una chaqueta ligera cortaviento sería útil."
    else:
        wind_recommendation = " El viento es suave, no se necesita protección adicional contra el viento."

    # Recomendaciones basadas en el índice UV
    if uv_index == "No disponible":
        uv_recommendation = ""
    elif uv_index > 7:
        uv_recommendation = " Usa protector solar de alto SPF, gafas de sol y considera un sombrero de ala ancha."
    elif 4 <= uv_index <= 7:
        uv_recommendation = " Usa protector solar y gafas de sol para protegerte de la radiación UV."
    else:
        uv_recommendation = " La radiación UV es baja, pero es recomendable usar protector solar."

    # Unir todas las recomendaciones
    full_recommendation = (
        temp_recommendation +
        precipitation_recommendation +
        wind_recommendation +
        uv_recommendation
    )

    return full_recommendation
