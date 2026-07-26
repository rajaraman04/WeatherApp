import { buildTravelInsights } from "../utils/travelInsights.js";
import { formatWeatherNumber } from "../utils/weather.js";

function getAqiClass(category) {
  switch (category) {
    case "Good":
      return "aqi-badge aqi-badge--good";
    case "Moderate":
      return "aqi-badge aqi-badge--moderate";
    case "Unhealthy for sensitive groups":
      return "aqi-badge aqi-badge--sensitive";
    case "Unhealthy":
    case "Very unhealthy":
    case "Hazardous":
      return "aqi-badge aqi-badge--unhealthy";
    default:
      return "aqi-badge";
  }
}

function TravelExtras({airQuality,location,weatherData,}) {
  if (!location || !weatherData) {
    return null;
  }
  const insights = buildTravelInsights(weatherData,airQuality,);
  const latitude =Number(location.latitude);
  const longitude =Number(location.longitude);
  const mapQuery= encodeURIComponent(`${latitude},${longitude}`,);

  const googleMapsUrl="https://www.google.com/maps/search/" +`?api=1&query=${mapQuery}`;
  const locationLabel = [location.name,location.state,location.country,].filter(Boolean).join(", ");
  return (<>
    <article className="content-card travel-recommendations-card">
      <p className="eyebrow">Travel assistance</p>
      <h2>Travel Recommendations</h2>
      <ul className="travel-recommendations">
        {insights.map((insight) => (<li key={insight}><span aria-hidden="true">✓</span><p>{insight}</p></li>))}
      </ul>
      <div className="maps-section">
        <div>
          <strong>{locationLabel || "Selected location"}</strong>
          <span>
            {latitude.toFixed(4)},{" "}
            {longitude.toFixed(4)}
          </span>
        </div>
        <a className="button button--secondary" href={googleMapsUrl} rel="noreferrer" target="_blank">
          Open Google Maps
        </a>
      </div>
    </article>
    <article className="content-card air-quality-card">
      <div className="air-quality-heading">
        <div>
          <p className="eyebrow">
            Additional API
          </p>
          <h2>Current Air Quality</h2>
        </div>
        {airQuality && (
          <span className={getAqiClass(airQuality.category,)}>
            {airQuality.category}
          </span>
        )}
      </div>

      {airQuality ? (
        <>
          <div className="air-quality-primary">
            <span>U.S. AQI</span>
            <strong>
              {formatWeatherNumber(airQuality.us_aqi,0,)}
            </strong>
          </div>
          <div className="air-quality-values">
            <div>
              <span>PM2.5</span>
              <strong>
                {formatWeatherNumber(airQuality.pm2_5,)}{" "}
                µg/m³
              </strong>
            </div>
            <div>
              <span>PM10</span>
              <strong>
                {formatWeatherNumber(airQuality.pm10,)}{" "}
                µg/m³
              </strong>
            </div>
            <div>
              <span>UV index</span>
              <strong>
                {formatWeatherNumber(airQuality.uv_index,)}
              </strong>
            </div>
          </div>
          <p className="data-attribution">
            Air-quality data provided by Open-Meteo and CAMS ENSEMBLE API.
          </p>
        </>
      ) : (
        <p className="muted-text"> Air-quality data is temporarily unavailable. Weather information is still available.</p>
      )}
    </article>
  </>
);
}
export default TravelExtras;