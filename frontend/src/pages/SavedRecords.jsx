import {useCallback,useEffect,useState,} from "react";
import SavedRecordCard from "../components/SavedRecordCard.jsx";
import { getWeatherRecords } from "../services/api.js";
import { getApiErrorMessage } from "../utils/apiError.js";

function SavedRecords() {
  const [records, setRecords] =useState([]);
  const [isLoading, setIsLoading] =useState(true);
  const [errorMessage, setErrorMessage] =useState("");
  const loadRecords = useCallback(
    async () => { setIsLoading(true);setErrorMessage("");
      try {
        const result =await getWeatherRecords({skip: 0,limit: 50,});
        setRecords(result);
      } catch (error) {
        setErrorMessage(getApiErrorMessage(error),);
      } finally {
        setIsLoading(false);
      }
    },
    [],
  );

  useEffect(() => {void loadRecords();}, [loadRecords]);

  return (
    <section className="page-section">
      <div className="section-heading">
        <div>
          <p className="eyebrow">
            MongoDB Connection
          </p>

          <h1>Saved Weather Records</h1>
        </div>

        <p className="section-heading__description">
          Review, update, delete, and export previous weather searches.
        </p>
      </div>

      <div className="page-actions">
        <button className="button button--secondary" disabled={isLoading} onClick={loadRecords} type="button">
          {isLoading ? "Loading...":"Refresh Records"}
        </button>
        <button className="button button--secondary" disabled title="Frontend export will be connected in a later step." type="button">
          Export JSON
        </button>

        <button className="button button--secondary" disabled title="Frontend export will be connected in a later step." type="button">
          Export CSV
        </button>
      </div>

      {errorMessage && (<div className="error-alert" role="alert">
          {errorMessage}
        </div>
      )}

      {isLoading ? ( <div className="loading-state" role="status">
          <div className="loading-spinner" aria-hidden="true"/>
          <p>Loading saved weather records...</p>
        </div>
      ) : records.length > 0 ? ( <div className="saved-records-grid">
          {records.map((record) => (<SavedRecordCard key={record.id} record={record} />
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <span className="empty-state__icon" aria-hidden="true">
            🗂
          </span>
          <h2>No saved weather records</h2>
          <p>
            Search for Weather on the Dashboard and Select Save Weather Search.
          </p>
        </div>
      )}
    </section>
  );
}

export default SavedRecords;