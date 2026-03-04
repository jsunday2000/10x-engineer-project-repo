function SearchBar({ value, onChange, placeholder = "Search prompts..." }) {
  return (
    <label className="search-bar">
      <span className="sr-only">Search prompts</span>
      <input
        type="search"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder}
      />
    </label>
  );
}

export default SearchBar;
