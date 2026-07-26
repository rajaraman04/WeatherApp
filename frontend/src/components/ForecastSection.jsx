import ForecastCard from "./ForecastCard.jsx";

const placeholderDays = ["Day 1","Day 2","Day 3","Day 4","Day 5",];

function ForecastPlaceholders() {
  return (
    <div className="forecast-grid">
      {placeholderDays.map((day) => (
        <article className="forecast-card" key={day}>
          <strong>{day}</strong>
          <span className="forecast-card__icon" aria-hidden="true">
            ◌
          </span>
          <span>High: --°</span>
          <span>Low: --°</span>
        </article>
      ))}
    </div>
  );
}

function ForecastSection({ weatherData }) {
  const forecast = weatherData?.forecast ?? [];
  const hasForecast = forecast.length > 0;

  return (
    <section className="content-card forecast-section">
      <div className="section-heading">
        <div>
          <p className="eyebrow">
            Upcoming conditions
          </p>

          <h2>Five Day forecast</h2>
        </div>

        <p className="section-heading__description">
          {hasForecast ? `Daily weather in ${ weatherData.timezone ?? "the selected location"}.` : ( "Search for a location to display daily weather information.")}
        </p>
      </div>

      {hasForecast ? (
        <div className="forecast-grid forecast-grid--real">
          {forecast.map((forecastDay) => (
            <ForecastCard forecastDay={forecastDay} key={forecastDay.forecast_date}
              precipitationUnit={ weatherData.precipitation_unit }
              temperatureUnit={ weatherData.temperature_unit}
              windSpeedUnit={ weatherData.wind_speed_unit}
            />
          ))}
        </div>
      ) : (
        <ForecastPlaceholders />
      )}
    </section>
  );
}

export default ForecastSection;