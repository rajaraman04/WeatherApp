class BrowserGeolocationError extends Error {
  constructor(message) {
    super(message);
    this.name = "BrowserGeolocationError";
  }
}

function createGeolocationError(error) {
  switch (error.code) {
    case 1:
      return new BrowserGeolocationError("Location permission was denied. Allow location access in your browser or search by city instead.",);
    case 2:
      return new BrowserGeolocationError("Your location could not be determined. Check your device location settings and try again.",);
    case 3:
      return new BrowserGeolocationError("Location detection took too long. Please try again or search by city.",);
    default:
      return new BrowserGeolocationError("Unable to access your current location.",);
  }
}

export function getCurrentCoordinates() {
  return new Promise((resolve, reject) => {
    if (!("geolocation" in navigator)) {
      reject(new BrowserGeolocationError("Current-location access is not supported by this browser.",),);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {resolve({latitude: position.coords.latitude,longitude: position.coords.longitude,accuracy: position.coords.accuracy,});},
      (error) => {reject(createGeolocationError(error));},
      {enableHighAccuracy: false,timeout: 10000,maximumAge: 300000,},
    );
  });
}