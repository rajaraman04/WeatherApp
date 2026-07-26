import { useState } from "react";

function LocationSearchForm() {
  const [location, setLocation]= useState("");
  const [startDate, setStartDate]= useState("");
  const [endDate, setEndDate]= useState("");
  const [temperatureUnit, setTemperatureUnit]= useState("fahrenheit");
  const [formMessage, setFormMessage]= useState("");

  function handleSubmit(event) {
    event.preventDefault();
    if (!location.trim()) {
      setFormMessage("Enter a city, town, landmark, or postal code.",);
      return;
    }
    if (!startDate || !endDate) {
      setFormMessage("Select both start date and an end date.");
      return;
    }
    setFormMessage("The form layout is working. FastAPI integration will be added soon.",);
  }

  function handleCurrentLocation() {
    setFormMessage("Browser geolocation will be connected soon.",);
  }

  return (
    <section className="search-panel" aria-labelledby="weather-search-title">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Weather search</p>
          <h2 id="weather-search-title">
            Check weather for your desired location
          </h2>
        </div>

        <p className="section-heading__description">
          Enter a location and select a date range of up to five days.
        </p>
      </div>

      <form className="weather-form" onSubmit={handleSubmit}>
        <div className="form-field form-field--location">
          <label htmlFor="location">Location</label>

          <input id="location" name="location" onChange={(event) => setLocation(event.target.value)} placeholder="City, town, landmark, or postal code" type="text"
            value={location}/>
        </div>

        <div className="form-field">
          <label htmlFor="start-date">Start date</label>

          <input id="start-date" name="startDate" onChange={(event) => setStartDate(event.target.value)} required
            type="date" value={startDate}/>
        </div>

        <div className="form-field">
          <label htmlFor="end-date">End date</label>

          <input id="end-date" name="endDate" onChange={(event) => setEndDate(event.target.value)} required type="date" value={endDate} />
        </div>

        <div className="form-field">
          <label htmlFor="temperature-unit">
            Temperature unit
          </label>

          <select id="temperature-unit" name="temperatureUnit"onChange={(event) => setTemperatureUnit(event.target.value) } value={temperatureUnit} >
            <option value="fahrenheit">Fahrenheit (°F)</option>
            <option value="celsius">Celsius (°C)</option>
          </select>
        </div>

        <div className="weather-form__actions">
          <button className="button button--primary" type="submit">
            Search Weather
          </button>

          <button className="button button--secondary" onClick={handleCurrentLocation} type="button">
            Use Current Location
          </button>
        </div>
      </form>

      {formMessage && ( <p className="form-message" role="status">
          {formMessage}
        </p>
      )}
    </section>
  );
}

export default LocationSearchForm;