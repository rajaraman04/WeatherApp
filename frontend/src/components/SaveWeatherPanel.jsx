import { Link } from "react-router";

function SaveWeatherPanel({isSaving,onSave,savedRecordId,saveMessage,}) {
  return (
    <article className="content-card save-weather-panel">
      <div>
        <p className="eyebrow">MongoDB Connection</p>
        <h2 id="save-weather-title">Save this weather search</h2>

        <p className="muted-text">
          Store the location, selected date range, current conditions, and daily forecast.
        </p>
      </div>

      <div className="save-weather-panel__actions">
        <button className="button button--primary" disabled={isSaving || Boolean(savedRecordId)} onClick={onSave} type="button">
          {isSaving ? "Saving..." : savedRecordId ? "Saved" : "Save Weather Search"}
        </button>

        {savedRecordId && (<Link className="button button--secondary" to="/saved-records" >
            View Saved Records
          </Link>
        )}
      </div>

      {saveMessage && ( <p className={ savedRecordId ? "success-alert" : "error-alert"} role="status">
          {saveMessage}
        </p>
      )}
    </article>
  );
}
export default SaveWeatherPanel;