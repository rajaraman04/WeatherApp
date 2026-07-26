import {useEffect,useState,} from "react";
import EditWeatherRecordModal from "../components/EditWeatherRecordModal.jsx";
import SavedRecordCard from "../components/SavedRecordCard.jsx";

import {deleteWeatherRecord,downloadWeatherRecords,getWeatherRecords,updateWeatherRecord, } from "../services/api.js";

import { getApiErrorMessage } from "../utils/apiError.js";

function SavedRecords() {
  const [records, setRecords] = useState([]);
  const [isLoading, setIsLoading] =useState(true);
  const [errorMessage, setErrorMessage] =useState("");
  const [statusMessage, setStatusMessage] =useState(null);
  const [editingRecord, setEditingRecord] =useState(null);
  const [editErrorMessage, setEditErrorMessage] =useState("");
  const [isUpdating, setIsUpdating] =useState(false);
  const [deletingRecordId,setDeletingRecordId,] = useState(null);
  const [exportingFormat, setExportingFormat] =useState(null);

  async function loadRecords() {
    setIsLoading(true);
    setErrorMessage("");
    try {
      const result = await getWeatherRecords({skip: 0,limit: 50,});
      setRecords(result);
    } catch (error) {
      setErrorMessage(getApiErrorMessage(error),);
    } finally {
      setIsLoading(false);
    }
  }
useEffect(()=>{
  let ignoreResult = false;
  async function loadInitialRecords() {
    try {
      const result = await getWeatherRecords({skip: 0,limit: 50,});
      if (!ignoreResult) {
        setRecords(result);
      }
    } catch (error) {
      if (!ignoreResult) {
        setErrorMessage(getApiErrorMessage(error),);
      }
    } finally {
      if (!ignoreResult) {
        setIsLoading(false);
      }
    }
  }
  void loadInitialRecords();
  return () => { ignoreResult = true;};}, []);

  function showStatus(type, message) {
    setStatusMessage({type,message,});
  }

  function handleOpenEdit(record) {
    setEditErrorMessage("");
    setStatusMessage(null);
    setEditingRecord(record);
  }

  function handleCloseEdit() {
    if (!isUpdating) {
      setEditingRecord(null);
      setEditErrorMessage("");
    }
  }

  async function handleUpdateRecord(recordId,requestData,) {
    setIsUpdating(true);
    setEditErrorMessage("");
    try {
      const updatedRecord =await updateWeatherRecord(recordId,requestData,);
      setRecords((currentRecords) => currentRecords.map((record) => record.id === updatedRecord.id ? updatedRecord: record,),);
      setEditingRecord(null);
      showStatus("success","Weather record updated successfully.",);
    } catch (error) {
      setEditErrorMessage(getApiErrorMessage(error),);
    } finally {
      setIsUpdating(false);
    }
  }

  async function handleDeleteRecord(record) {
    const confirmed = window.confirm("Delete this weather record permanently? This action cannot be undone.",);

    if (!confirmed) {
      return;
    }

    setDeletingRecordId(record.id);
    setStatusMessage(null);
    try {
      await deleteWeatherRecord(record.id);

      setRecords((currentRecords) =>currentRecords.filter((currentRecord) =>currentRecord.id !== record.id,),);
      showStatus("success","Weather record deleted successfully.",);
    } catch (error) {
      showStatus("error",getApiErrorMessage(error),);
    } finally {
      setDeletingRecordId(null);
    }
  }

  async function handleExport(exportFormat) {
    setExportingFormat(exportFormat);
    setStatusMessage(null);
    try {
      await downloadWeatherRecords(exportFormat,);
      showStatus("success",`The ${exportFormat.toUpperCase()} export was downloaded successfully.`,);
    } catch (error) {
      showStatus("error",getApiErrorMessage(error),);
    } finally {
      setExportingFormat(null);
    }
  }

  const isExporting = exportingFormat !== null;

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
          {isLoading ? "Loading..." : "Refresh Records"}
        </button>

        <button className="button button--secondary" disabled={isExporting} onClick={() => handleExport("json")} type="button">
          {exportingFormat === "json" ? "Exporting JSON..." : "Export JSON"}
        </button>

        <button className="button button--secondary" disabled={isExporting} onClick={() => handleExport("csv")} type="button">
          {exportingFormat === "csv" ? "Exporting CSV..." : "Export CSV"}
        </button>
      </div>

      {statusMessage && ( <div className={ statusMessage.type === "success" ? "success-alert" : "error-alert" } role="status">
          {statusMessage.message}
        </div>
      )}

      {errorMessage && ( <div className="error-alert" role="alert">
          {errorMessage}
        </div>
      )}

      {isLoading ? ( <div className="loading-state" role="status" >
          <div aria-hidden="true" className="loading-spinner" />
          <p>Loading saved weather records...</p>
        </div>
      ) : records.length > 0 ? (
        <div className="saved-records-grid">
          {records.map((record) => (
            <SavedRecordCard isDeleting={ deletingRecordId === record.id } key={record.id} onDelete={handleDeleteRecord} onEdit={handleOpenEdit} record={record}/>
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <span aria-hidden="true" className="empty-state__icon">
            🗂
          </span>
          <h2>No saved weather records</h2>
          <p>
            Search for weather on the Dashboard and select Save Weather Search.
          </p>
        </div>
      )}

      {editingRecord && ( <EditWeatherRecordModal errorMessage={editErrorMessage} isUpdating={isUpdating} key={editingRecord.id} onClose={handleCloseEdit} onSave={handleUpdateRecord} record={editingRecord}/>)}
    </section>
  );
}
export default SavedRecords;