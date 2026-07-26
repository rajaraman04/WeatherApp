const MILLISECONDS_PER_DAY = 24*60*60*1000;

export function formatDateInput(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth()+1).padStart(2,"0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

export function addCalendarDays(date, numberOfDays) {
  const result = new Date(date);
  result.setDate(result.getDate()+numberOfDays);
  return result;
}

export function getDefaultDateRange() {
  const today = new Date();

  return {
    startDate: formatDateInput(today),
    endDate: formatDateInput(addCalendarDays(today, 4)),
  };
}

export function getInclusiveDayCount(startDate, endDate) {
  const startTimestamp = Date.parse(`${startDate}T00:00:00Z`,);
  const endTimestamp = Date.parse(`${endDate}T00:00:00Z`,);
  return (Math.floor((endTimestamp - startTimestamp) / MILLISECONDS_PER_DAY,)+1);
}

export function formatForecastDate(dateString) {
  if (!dateString) {
    return {weekday: "Unknown",dateLabel: "Date unavailable",};
  }
  const date = new Date(`${dateString}T00:00:00`,);
  if (Number.isNaN(date.getTime())) {
    return {weekday: "Unknown",dateLabel: dateString,};
  }
  const weekdayFormatter = new Intl.DateTimeFormat("en-US", {weekday: "long",});
  const dateFormatter =new Intl.DateTimeFormat("en-US", {month: "short",day: "numeric",});
  return {weekday: weekdayFormatter.format(date),dateLabel: dateFormatter.format(date),};
}

export function formatWeatherTime(dateTimeString) {
  if (!dateTimeString) {
    return "Not available";
  }
  const date = new Date(dateTimeString);
  if (Number.isNaN(date.getTime())) {
    return "Not available";
  }
  return new Intl.DateTimeFormat("en-US", {hour: "numeric",minute: "2-digit",}).format(date);
}