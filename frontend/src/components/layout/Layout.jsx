function Layout({ header, sidebar, children }) {
  return (
    <div className="app-shell">
      <header className="app-header">{header}</header>
      <div className="app-content">
        <aside className="app-sidebar">{sidebar}</aside>
        <main className="app-main">{children}</main>
      </div>
    </div>
  );
}

export default Layout;
