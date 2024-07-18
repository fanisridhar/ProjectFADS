import React, { useState } from 'react';
import axios from 'axios';

function SearchForm() {
  const [keyword, setKeyword] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.get('/search', { params: { keyword } });
      setResults(response.data.urls);
    } catch (error) {
      console.error('There was an error with the search!', error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSearch}>
        <input
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="Search keyword"
        />
        <button type="submit">Search</button>
      </form>
      <ul>
        {results.map((url, index) => (
          <li key={index}>
            <a href={url} target="_blank" rel="noopener noreferrer">{url}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SearchForm;
