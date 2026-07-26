export function getApiErrorMessage(error) {
  const detail = error.response?.data?.detail;

  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    const messages = detail.map((item) => item.msg).filter(Boolean);

    if (messages.length > 0) {
      return messages.join(" ");
    }
  }

  if (error.code==="ECONNABORTED") {
    return "The request took too long. Please try again.";
  }

  if (!error.response) {
    return ("Unable to connect to the WeatherApp server. Confirm that the FastAPI backend is running.");
  }
  return "Something went wrong while processing the request.";
}