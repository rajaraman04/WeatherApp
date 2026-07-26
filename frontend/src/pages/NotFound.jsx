import { Link } from "react-router";

function NotFound() {
  return (
    <section className="empty-state">
      <p className="eyebrow">404 error</p>
      <h1>Page not found</h1>

      <p> The page you requested does not exist in the WeatherApp.
      </p>

      <Link className="button button--primary" to="/">
        Return to Dashboard
      </Link>
    </section>
  );
}

export default NotFound;