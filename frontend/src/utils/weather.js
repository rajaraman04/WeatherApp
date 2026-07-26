export function getTemperatureSymbol(unit) {
  return unit === "celsius" ? "°C" : "°F";
}

export function getWindUnitLabel(unit) {
  return unit === "mph" ? "mph" : "km/h";
}

export function getWeatherIcon(weatherCode) {
  if (weatherCode === 0) {
    return "☀️";
  }
  if ([1,2].includes(weatherCode)) {
    return "🌤️";
  }
  if (weatherCode === 3) {
    return "☁️";
  }
  if ([45,48].includes(weatherCode)) {
    return "🌫️";
  }
  if ( [51,53,55,56,57,61,63,65,66,67,80,81,82,].includes(weatherCode)) {
    return "🌧️";
  }
  if ([71,73,75,77,85,86].includes(weatherCode,)) {
    return "🌨️";
  }
  if ([95,96,99].includes(weatherCode)) {
    return "⛈️";
  }
  return "🌡️";
}