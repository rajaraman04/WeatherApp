function SavedRecords() {
  return (
    <section className="page-section">
      <div className="section-heading">
        <div>
          <p className="eyebrow">MongoDB Display Page</p>
          <h1>Saved Weather Records</h1>
        </div>
        <p className="section-heading__description">
          Review, update, delete, and export previous weather searches.
        </p>
      </div>
      <div className="page-actions">
        <button className="button button--secondary" type="button">
          Export JSON
        </button>
        <button className="button button--secondary" type="button">
          Export CSV
        </button>
      </div>

      <div className="empty-state">
        <span className="empty-state__icon" aria-hidden="true">
          🗂
        </span>

        <h2>No records loaded yet</h2>

        <p>
          The MongoDB READ, UPDATE, DELETE, and export endpoints will be connected to this page soon.
        </p>
      </div>
    </section>
  );
}

export default SavedRecords;