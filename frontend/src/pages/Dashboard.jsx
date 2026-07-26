import LocationSearchForm from "../components/LocationSearchForm.jsx";

const forecastPlaceholders = ["Day 1","Day 2","Day 3","Day 4","Day 5",];

function Dashboard() {
  return (
    <>
      <section className="hero">
        <div>
          <p className="eyebrow">Real-time Weather Planning App </p>

          <h1>Plan confidently with weather that matters.</h1>

          <p className="hero__description">
            Search any location, review current conditions, and compare a five-day forecast before making travel plans.
          </p>
        </div>

        <div className="hero__summary" aria-label="Project capabilities">
          <div>
            <strong>5-day</strong>
            <span>forecast</span>
          </div>

          <div>
            <strong>Live</strong>
            <span>weather data</span>
          </div>

          <div>
            <strong>CRUD</strong>
            <span>saved records</span>
          </div>
        </div>
      </section>
      <LocationSearchForm />

      <section className="dashboard-grid" aria-label="Weather result placeholders" >
        <article className="content-card current-weather-card">
          <p className="eyebrow">Current conditions</p>
          <h2>No weather selected</h2>

          <p className="muted-text">
            Search for a location to view temperature, humidity, wind speed, precipitation, and current conditions.
          </p>

          <div className="weather-placeholder">
            <span aria-hidden="true">☁</span>
            <strong>--°</strong>
          </div>
        </article>

        <article className="content-card">
          <p className="eyebrow">Travel guidance</p>
          <h2>Smart travel insights</h2>

          <p className="muted-text">
            Weather-based recommendations for rain, UV exposure, air quality, wind, heat, and cold will appear here.
          </p>

          <ul className="insight-list">
            <li>Umbrella recommendation</li>
            <li>Clothing guidance</li>
            <li>Outdoor-activity suitability</li>
          </ul>
        </article>
      </section>

      <section className="content-card forecast-section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Upcoming conditions</p>
            <h2>Five-day forecast</h2>
          </div>

          <p className="section-heading__description">
            Daily temperatures and weather conditions will appear after a successful search.
          </p>
        </div>

        <div className="forecast-grid">
          {forecastPlaceholders.map((day) => (
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
      </section>
    </>
  );
}

export default Dashboard;