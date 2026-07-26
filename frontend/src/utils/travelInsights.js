function convertTemperatureToCelsius(temperature,unit,) {
  if (temperature === null ||temperature === undefined) {
    return null;
  }
  const numericTemperature =Number(temperature);
  if (Number.isNaN(numericTemperature)) {
    return null;
  }
  if (unit === "fahrenheit") {
    return ((numericTemperature - 32) *(5 / 9));
  }
  return numericTemperature;
}

export function buildTravelInsights(weatherData,airQuality,) {
  if (!weatherData) {
    return [];
  }
  const insights=[];
  const forecast=weatherData.forecast ?? [];
  const rainProbabilities = forecast.map((day) =>day.precipitation_probability,).filter((value) =>value !== null && value !== undefined,)
    .map(Number).filter((value) => !Number.isNaN(value),);

  const highestRainChance = rainProbabilities.length > 0 ? Math.max(...rainProbabilities): 0;

  if (highestRainChance>=60) {
    insights.push("Rain is likely. Carry an umbrella or waterproof jacket.",);
  } else if (highestRainChance>=30) {
    insights.push("There is a chance of rain. Keep a compact umbrella available.",);
  }

  const maximumTemperatures = forecast.map((day) =>convertTemperatureToCelsius(day.maximum_temperature,weatherData.temperature_unit,),)
    .filter((value) => value !== null,);

  if (maximumTemperatures.length > 0 &&Math.max(...maximumTemperatures) >= 30) {
    insights.push("Hot conditions are expected. Carry water and plan breaks from the heat.",);
  }
  if (airQuality?.uv_index !== null &&airQuality?.uv_index !== undefined &&Number(airQuality.uv_index) >= 6) {
    insights.push("UV levels are elevated. Consider sunscreen, sunglasses, and shade.",);
  }
  if (airQuality?.us_aqi !== null &&airQuality?.us_aqi !== undefined &&Number(airQuality.us_aqi) >= 101) {
    insights.push("Air quality may affect sensitive travelers. Consider limiting prolonged outdoor activity.",);
  }
  if (insights.length===0) {
    insights.push("Conditions appear generally suitable for normal travel plans.",);
  }
  return insights.slice(0, 4);
}