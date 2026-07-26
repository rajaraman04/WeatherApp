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