import { NavLink } from "react-router";

function getNavigationClass({ isActive }) {
  return isActive ? "navigation-link navigation-link--active" : "navigation-link";
}

function Header() {
  return (
    <header className="site-header">
      <div className="site-header__content">
        <NavLink className="brand" to="/">
          <span className="brand__icon" aria-hidden="true">
            ☀
          </span>
          <span>
            <strong className="brand__name">WeatherApp</strong>
            <span className="brand__tagline">
              Weather App
            </span>
          </span>
        </NavLink>

        <nav className="navigation" aria-label="Primary navigation">
          <NavLink className={getNavigationClass} end to="/">
            Dashboard
          </NavLink>

          <NavLink className={getNavigationClass} to="/saved-records">
            Saved Records
          </NavLink>

          <NavLink className={getNavigationClass} to="/about">
            About
          </NavLink>
        </nav>
      </div>
    </header>
  );
}

export default Header;