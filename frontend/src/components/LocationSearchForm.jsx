import { useState } from "react";

import {getDefaultDateRange,getInclusiveDayCount,} from "../utils/date.js";

const defaultDates = getDefaultDateRange();

function LocationSearchForm({isSearching,onSearch,
}) {
  const [location, setLocation] = useState("");
  const [startDate, setStartDate] = useState(defaultDates.startDate,);
  const [endDate, setEndDate] = useState(defaultDates.endDate,);
  const [temperatureUnit, setTemperatureUnit] =useState("fahrenheit");
  const [validationMessage, setValidationMessage] =useState("");

  function handleSubmit(event) {
    event.preventDefault();
    const normalizedLocation = location.trim();
    if (normalizedLocation.length < 2) {
      setValidationMessage("Enter at least two characters for the location.",);
      return;
    }

    if (!startDate || !endDate) {
      setValidationMessage("Select both the start date and an end date.",);
      return;
    }

    if (endDate < startDate) {
      setValidationMessage( "The end date must be the same as or later than the start date.",);
      return;
    }
    const numberOfDays = getInclusiveDayCount(startDate,endDate,);
    if (numberOfDays > 5) {
      setValidationMessage("The selected date range cannot exceed five days.",);
      return;
    }
    setValidationMessage("");

    onSearch({location: normalizedLocation,startDate,endDate,temperatureUnit,});
  }

  return (
    <section className="search-panel" aria-labelledby="weather-search-title">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Weather Search</p>

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

          <input autoComplete="off" id="location" name="location" onChange={(event) =>setLocation(event.target.value)}
            placeholder="City, town, landmark, or postal code" type="text" value={location}/>
        </div>

        <div className="form-field">
          <label htmlFor="start-date">Start date</label>

          <input id="start-date" min={defaultDates.startDate} name="startDate" onChange={(event) => setStartDate(event.target.value)}
            type="date" value={startDate} />
        </div>

        <div className="form-field">
          <label htmlFor="end-date">End date</label>

          <input id="end-date" min={startDate} name="endDate" onChange={(event) => setEndDate(event.target.value)}
            type="date" value={endDate} />
        </div>

        <div className="form-field">
          <label htmlFor="temperature-unit">
            Temperature unit
          </label>

          <select id="temperature-unit" name="temperatureUnit" onChange={(event) => setTemperatureUnit(event.target.value) } value={temperatureUnit}>
            <option value="fahrenheit">
              Fahrenheit (°F)
            </option>

            <option value="celsius">
              Celsius (°C)
            </option>
          </select>
        </div>

        <div className="weather-form__actions">
          <button className="button button--primary" disabled={isSearching} type="submit">
            {isSearching
              ? "Searching Locations..."
              : "Search Weather"}
          </button>

          <button className="button button--secondary" disabled title="Current-location support will be added in Step 15." type="button">
            Use Current Location
          </button>
        </div>
      </form>

      {validationMessage && ( <p className="error-alert" role="alert">
          {validationMessage}
        </p>
      )}
    </section>
  );
}
export default LocationSearchForm;