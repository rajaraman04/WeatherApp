import { useState } from "react";
import {formatDateInput,getInclusiveDayCount,} from "../utils/date.js";

function EditWeatherRecordModal({errorMessage,isUpdating,onClose,onSave,record,}) {
  const [location, setLocation] = useState(record.location_query ?? "",);
  const [startDate, setStartDate] = useState(record.start_date,);
  const [endDate, setEndDate] = useState(record.end_date,);
  const [temperatureUnit, setTemperatureUnit] =useState(record.temperature_unit);
  const [validationMessage, setValidationMessage] =useState("");
  const today = formatDateInput(new Date());
  function handleSubmit(event) {
    event.preventDefault();
    const normalizedLocation = location.trim();
    if (normalizedLocation && normalizedLocation.length < 2) {
      setValidationMessage("Enter at least two characters for the location.",);
      return;
    }
    if (!startDate || !endDate) {
      setValidationMessage("Select both a start date and an end date.",);
      return;
    }

    if (startDate < today) {
      setValidationMessage("Select today or a future start date.",);
      return;
    }
    if (endDate < startDate) {
      setValidationMessage("The end date must be the same as or later than the start date.",);
      return;
    }
    const selectedDays = getInclusiveDayCount(startDate,endDate,);
    if (selectedDays > 5) {
      setValidationMessage("The selected date range cannot exceed five days.",);
      return;
    }

    setValidationMessage("");
    const requestData = {start_date: startDate,end_date: endDate,temperature_unit: temperatureUnit,};

    if (normalizedLocation) {
      requestData.location =normalizedLocation;
    }
    onSave(record.id, requestData);
  }

  function handleOverlayClick(event) {
    if (event.target === event.currentTarget && !isUpdating) {
      onClose();
    }
  }

  return (
    <div className="modal-overlay" onMouseDown={handleOverlayClick} role="presentation">
      <section aria-labelledby="edit-record-title" aria-modal="true" className="edit-modal" role="dialog">
        <div className="edit-modal__header">
          <div>
            <p className="eyebrow">
              Update Weather Record
            </p>

            <h2 id="edit-record-title">
              Edit Saved Weather
            </h2>
          </div>

          <button aria-label="Close edit dialog" className="modal-close-button" disabled={isUpdating} onClick={onClose} type="button">
            ×
          </button>
        </div>

        <p className="muted-text">
          Updating the request retrieves fresh weather information and replaces the stored forecast.
        </p>

        <form className="edit-record-form" onSubmit={handleSubmit}>
          <div className="form-field">
            <label htmlFor="edit-location">
              Location
            </label>

            <input disabled={isUpdating} id="edit-location" onChange={(event) =>setLocation(event.target.value)}
              placeholder="Leave blank to preserve saved coordinates" type="text" value={location}/>

            {!record.location_query && ( <small className="form-help-text">
                This record was created with GPS coordinates. Leave this field blank to preserve those coordinates.
              </small>
            )}
          </div>

          <div className="edit-record-form__dates">
            <div className="form-field">
              <label htmlFor="edit-start-date">
                Start date
              </label>

              <input disabled={isUpdating} id="edit-start-date" min={today} onChange={(event) => setStartDate(event.target.value)}
                type="date" value={startDate} />
            </div>

            <div className="form-field">
              <label htmlFor="edit-end-date">
                End date
              </label>

              <input disabled={isUpdating} id="edit-end-date" min={startDate} onChange={(event) => setEndDate(event.target.value)}
                type="date" value={endDate} />
            </div>
          </div>

          <div className="form-field">
            <label htmlFor="edit-temperature-unit">
              Temperature unit
            </label>

            <select disabled={isUpdating} id="edit-temperature-unit" onChange={(event) => setTemperatureUnit( event.target.value,)} value={temperatureUnit}>
              <option value="fahrenheit">
                Fahrenheit (°F)
              </option>

              <option value="celsius">
                Celsius (°C)
              </option>
            </select>
          </div>

          {validationMessage && ( <div className="error-alert" role="alert">
              {validationMessage}
            </div>
          )}

          {errorMessage && ( <div className="error-alert" role="alert">
              {errorMessage}
            </div>
          )}

          <div className="edit-modal__actions">
            <button className="button button--secondary" disabled={isUpdating} onClick={onClose} type="button">
              Cancel
            </button>
            <button className="button button--primary" disabled={isUpdating} type="submit">
              {isUpdating ? "Updating..." : "Update and Refresh Weather"}
            </button>
          </div>
        </form>
      </section>
    </div>
  );
}
export default EditWeatherRecordModal;