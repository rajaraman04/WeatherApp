function buildLocationLabel(location) {
  return [location.name,location.state,location.country,location.postal_code,].filter(Boolean).join(", ");
}

function LocationResults({isLoadingWeather,locations,onSelect,}) {
  if (locations.length === 0) {
    return null;
  }

  return (
    <section className="location-results" aria-labelledby="location-results-title">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Location validation</p>

          <h2 id="location-results-title">
            Select the correct location
          </h2>
        </div>

        <p className="section-heading__description">
          Multiple locations may share the same name.
        </p>
      </div>

      <div className="location-results__list">
        {locations.map((location) => {
          const label = buildLocationLabel(location);

          return (
            <button className="location-result" disabled={isLoadingWeather} key={`${location.latitude}-${location.longitude}-${label}`} onClick={() => onSelect(location)} type="button">
              <span>
                <strong>{location.name}</strong>
                <span className="location-result__label">
                  {label}
                </span>
              </span>

              <span className="location-result__coordinates">
                {location.latitude.toFixed(4)},{" "}
                {location.longitude.toFixed(4)}
              </span>
            </button>
          );
        })}
      </div>

      {isLoadingWeather && ( <p className="loading-message" role="status">
          Retrieving weather information..
        </p>
      )}
    </section>
  );
}
export default LocationResults;