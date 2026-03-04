import Button from "../shared/Button";
import SearchBar from "../shared/SearchBar";

function Header({
  searchQuery,
  onSearchChange,
  onCreatePrompt,
  onRefresh,
  isRefreshing,
}) {
  return (
    <div className="header-inner">
      <div className="header-title-group">
        <h1>PromptLab</h1>
        <p>Manage prompts and collections with full CRUD operations.</p>
      </div>

      <div className="header-actions">
        <SearchBar value={searchQuery} onChange={onSearchChange} />
        <Button variant="secondary" onClick={onRefresh} isLoading={isRefreshing}>
          Refresh
        </Button>
        <Button variant="primary" onClick={onCreatePrompt}>
          New Prompt
        </Button>
      </div>
    </div>
  );
}

export default Header;
