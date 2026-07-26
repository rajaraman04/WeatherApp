import axios from "axios";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000",
  timeout: 15000,
  headers: { Accept: "application/json", },
});

export async function searchLocations(query) {
  const response = await apiClient.get( "/api/locations/search",
    { params: { q: query, limit: 5,}, },);
  return response.data;
}

export async function getWeather({latitude,longitude,startDate,endDate,temperatureUnit,}) {
  const response = await apiClient.get("/api/weather", {
    params: {latitude,longitude,start_date: startDate,end_date: endDate,temperature_unit: temperatureUnit,},});
  return response.data;
}
export async function createWeatherRecord(requestData) {
  const response = await apiClient.post("/api/weather-records",requestData,);
  return response.data;
}

export async function getWeatherRecords({skip = 0,limit = 50,}={}) {
  const response = await apiClient.get("/api/weather-records",{params: {skip,limit,},},);
  return response.data;
}

export async function updateWeatherRecord(recordId,requestData,) {
  const response = await apiClient.patch(`/api/weather-records/${recordId}`,requestData,);
  return response.data;
}

export async function deleteWeatherRecord(recordId) {
  await apiClient.delete(`/api/weather-records/${recordId}`,);
}

function getExportFilename(contentDisposition,exportFormat,) {
  const fallbackFilename =`weather-records.${exportFormat}`;
  if (!contentDisposition) {
    return fallbackFilename;
  }

  const filenameMatch =contentDisposition.match(/filename="?([^";]+)"?/i,);
  return filenameMatch?.[1] ?? fallbackFilename;
}

export async function downloadWeatherRecords(exportFormat,) {
  const response = await apiClient.get(`/api/weather-records/export/${exportFormat}`,{responseType: "blob",},);
  const filename = getExportFilename(response.headers["content-disposition"],exportFormat,);
  const downloadUrl = URL.createObjectURL(response.data,);
  const downloadLink =document.createElement("a");
  downloadLink.href = downloadUrl;
  downloadLink.download = filename;
  downloadLink.style.display = "none";
  document.body.appendChild(downloadLink);
  downloadLink.click();
  downloadLink.remove();
  window.setTimeout(() => {URL.revokeObjectURL(downloadUrl);}, 0);
}
export default apiClient;