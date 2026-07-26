import {formatForecastDate,} from "../utils/date.js";

import {formatWeatherNumber,getTemperatureSymbol,getWeatherIcon,} from "../utils/weather.js";

function getLocationLabel(record) {
  const resolvedLocation = record.resolved_location ?? {};
  const locationParts = [resolvedLocation.name,resolvedLocation.state,resolvedLocation.country,].filter(Boolean);

  if (locationParts.length > 0) {
    return locationParts.join(", ");
  }

  if (record.location_query) {
    return record.location_query;
  }

  const latitude =resolvedLocation.latitude;
  const longitude =resolvedLocation.longitude;
  if (latitude !== undefined && longitude !== undefined) {
    return `${Number(latitude).toFixed(4)}, ${Number(longitude,).toFixed(4)}`;
  }
  return "Unknown location";
}

function formatCreatedAt(timestamp) {
  if (!timestamp) {
    return "Date unavailable";
  }
  const date = new Date(timestamp);
  if (Number.isNaN(date.getTime())) {
    return "Date unavailable";
  }
  return new Intl.DateTimeFormat("en-US", {dateStyle: "medium",timeStyle: "short",}).format(date);
}

function SavedRecordCard({isDeleting,onDelete,onEdit,record,}) {
  const currentWeather =record.current_weather;
  const temperatureSymbol =getTemperatureSymbol(record.temperature_unit,);
  const startDate= formatForecastDate(record.start_date,);
  const endDate= formatForecastDate(record.end_date,);

  return (
    <article className="saved-record-card">
      <div className="saved-record-card__header">
        <div>
          <p className="eyebrow">
            {record.weather_source ??
              "Weather record"}
          </p>

          <h2>{getLocationLabel(record)}</h2>

          <p className="muted-text">
            {startDate.dateLabel}
            {" – "}
            {endDate.dateLabel}
          </p>
        </div>

        <span className="saved-record-card__icon" aria-hidden="true">
          {getWeatherIcon( currentWeather?.weather_code,)}
        </span>
      </div>

      <div className="saved-record-card__summary">
        <div>
          <span>Temperature</span>

          <strong>
            {currentWeather ? `${formatWeatherNumber(currentWeather.temperature,)}${temperatureSymbol}` : "Not available"}
          </strong>
        </div>

        <div>
          <span>Condition</span>
          <strong>
            {currentWeather?.condition ?? "Not available"}
          </strong>
        </div>

        <div>
          <span>Forecast days</span>

          <strong>
            {record.forecast?.length ?? 0}
          </strong>
        </div>
      </div>
        <div className="saved-record-card__actions">
        <button className="button button--secondary" disabled={isDeleting} onClick={() => onEdit(record)} type="button">
            Edit
        </button>

        <button className="button button--danger" disabled={isDeleting} onClick={() => onDelete(record)} type="button">
            {isDeleting ? "Deleting..." : "Delete"}
        </button>
        </div>

      <div className="saved-record-card__footer">
        <span>
          Saved {formatCreatedAt(record.created_at)}
        </span>

        <span>
          {record.temperature_unit === "celsius" ? "Metric units" : "US customary units"}
        </span>
      </div>
    </article>
  );
}
export default SavedRecordCard;