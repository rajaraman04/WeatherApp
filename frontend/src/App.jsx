import { Route, Routes } from "react-router";
import Header from "./components/Header.jsx";
import About from "./pages/About.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import NotFound from "./pages/NotFound.jsx";
import SavedRecords from "./pages/SavedRecords.jsx";

function App() {
  return (
    <div className="app-shell">
      <Header />
      <main className="page-container">
        <Routes>
          <Route element={<Dashboard />} path="/" />
          <Route element={<SavedRecords />} path="/saved-records" />
          <Route element={<About />} path="/about" />
          <Route element={<NotFound />} path="*" />
        </Routes>
      </main>

      <footer className="site-footer">
        <p>
          WeatherApp · Developed by Rajaraman Rajagopalan
        </p>
      </footer>
    </div>
  );
}

export default App;