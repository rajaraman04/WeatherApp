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
            WeatherApp is a full-stack weather and travel-planning application that retrieves real weather data using APIs, 
            validates user input locations and date ranges, stores weather requests, and
            supports complete CRUD operations.
          </p>
        </article>

        <article className="content-card">
          <h2>Developer Credits</h2>

          <p>
            <strong>Rajaraman Rajagopalan</strong>
          </p>

          <p>
            Pursuing Master&apos;s in Computer Science at Binghamton University.
          </p>
        </article>

        <article className="content-card">
          <h2>PM Accelerator</h2>

          <p>
            Official PM Accelerator information will be added from the organization&apos;s official company description before final submission.
          </p>
        </article>
      </div>
    </section>
  );
}
export default About;