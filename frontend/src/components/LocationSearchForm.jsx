import { useState } from "react";

import {getDefaultDateRange,getInclusiveDayCount,} from "../utils/date.js";

const defaultDates = getDefaultDateRange();

function LocationSearchForm({isLocating,isSearching,onSearch,onUseCurrentLocation,}) {
  const [location, setLocation] = useState("");
  const [startDate, setStartDate] = useState(defaultDates.startDate,);
  const [endDate, setEndDate] = useState(defaultDates.endDate,);
  const [temperatureUnit, setTemperatureUnit] =useState("fahrenheit");
  const [validationMessage, setValidationMessage] =useState("");

  function validateDates() {
    if (!startDate || !endDate) {
      return "Select both a start date and an end date.";
    }
    if (endDate < startDate) {
      return ("The end date must be the same as or later than the start date.");
    }

    const numberOfDays = getInclusiveDayCount(startDate,endDate,);

    if (numberOfDays > 5) {
      return ("The selected date range cannot exceed five days.");
    }

    return "";
  }

  function getWeatherCriteria() {
    return {startDate,endDate,temperatureUnit,};
  }

  function handleSubmit(event) {
    event.preventDefault();
    const normalizedLocation = location.trim();
    if (normalizedLocation.length < 2) {
      setValidationMessage("Enter at least two characters for the location.",);
      return;
    }

    const dateError = validateDates();
    if (dateError) {
      setValidationMessage(dateError);
      return;
    }
    setValidationMessage("");
    onSearch({location: normalizedLocation, ...getWeatherCriteria(),});
  }

  function handleCurrentLocation() {
    const dateError = validateDates();
    if (dateError) {
      setValidationMessage(dateError);
      return;
    }
    setValidationMessage("");
    onUseCurrentLocation(getWeatherCriteria(),);}

  const isBusy = isSearching || isLocating;

  return (
    <section className="search-panel" aria-labelledby="weather-search-title">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Weather Search</p>

          <h2 id="weather-search-title">
            Check weather for your destination
          </h2>
        </div>

        <p className="section-heading__description">
          Enter a location or use your current location. Select a date range of up to five days.
        </p>
      </div>

      <form className="weather-form" onSubmit={handleSubmit} >
        <div className="form-field form-field--location">
          <label htmlFor="location">Location</label>

          <input autoComplete="off" disabled={isBusy} id="location" name="location" onChange={(event) => setLocation(event.target.value)}
            placeholder="City, town, landmark, or postal code" type="text" value={location}/>
        </div>

        <div className="form-field">
          <label htmlFor="start-date">Start date</label>

          <input disabled={isBusy} id="start-date" min={defaultDates.startDate} name="startDate" onChange={(event) =>setStartDate(event.target.value)}
            type="date" value={startDate} />
        </div>

        <div className="form-field">
          <label htmlFor="end-date">End date</label>

          <input disabled={isBusy} id="end-date" min={startDate} name="endDate" onChange={(event) => setEndDate(event.target.value)}
            type="date" value={endDate}/>
        </div>

        <div className="form-field">
          <label htmlFor="temperature-unit">
            Temperature unit
          </label>

          <select disabled={isBusy} id="temperature-unit" name="temperatureUnit" onChange={(event) => setTemperatureUnit(event.target.value)} value={temperatureUnit} >
            <option value="fahrenheit">
              Fahrenheit (°F)
            </option>

            <option value="celsius">
              Celsius (°C)
            </option>
          </select>
        </div>

        <div className="weather-form__actions">
          <button className="button button--primary" disabled={isBusy} type="submit" >
            {isSearching ? "Searching Locations..." : "Search Weather"}
          </button>

          <button className="button button--secondary" disabled={isBusy} onClick={handleCurrentLocation} type="button">
            {isLocating ? "Detecting Location..." : "Use Current Location"}
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