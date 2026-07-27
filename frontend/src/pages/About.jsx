function About() {
  return (
    <section className="page-section">
      <div className="section-heading">
        <div>
          <p className="eyebrow">About the project</p>
          <h1>Weather App</h1>
        </div>
      </div>

      <div className="about-grid">
        <article className="content-card">
          <h2>Project</h2>

          <p>
            WeatherApp is a full-stack weather and travel-planning application. Users can search for a location or use their current
            location, retrieve current conditions and a one-to-five-day forecast, review air quality and travel recommendations, and save weather searches to database.
          </p>
        </article>

        <article className="content-card">
          <h2>Developer Credits</h2>

          <p>
            <strong>Rajaraman Rajagopalan</strong>
          </p>

          <p>
            Master&apos;s in Computer Science at Binghamton University.
          </p>
        </article>

        <article className="content-card">
          <h2>PM Accelerator</h2>

          <p>
          Product Manager Accelerator supports product-management professionals through different stages of their careers by providing product-management training, career development,
          mock interviews, leadership development, and AI product-management programs.          
          </p>
        </article>
      </div>
    </section>
  );
}
export default About;