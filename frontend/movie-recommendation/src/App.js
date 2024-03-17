import React, { useState } from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false); 
  const API_URL = 'http://127.0.0.1:8000/search/';

  const handleSearch = async (e) => {
    e.preventDefault();
    setIsSearching(true);
    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text }),
      });

      if (!response.ok) {
        console.log("Error fetching data");
        setSearchResults([]);
      } else {
        const results = await response.json();
        console.log(results);
        setSearchResults(results.results || []);
      }
    } catch (error) {
      console.error("Failed to fetch: ", error);
      setSearchResults([]);
    } finally {
      setIsSearching(false); 
    }
  };

  return (
    <div>
      <input type='text' value={text} onChange={(e) => setText(e.target.value)} />
      <button onClick={handleSearch} disabled={isSearching}>
        {isSearching ? 'Searching...' : 'Search'}
      </button>
      <div>
        {searchResults && searchResults.map((book, index) => (
          <div key={index} style={{ padding: '10px', margin: '10px', border: '1px solid black' }}>
            <h3>{book.title}</h3>
            <p><strong>Authors:</strong> {book.authors}</p>
            <p><strong>Description:</strong> {book.description}</p>
            <p><strong>Average Rating:</strong> {book.average_rating}</p>
            <p><strong>Published Year:</strong> {book.published_year}</p>
            <img src={book.thumbnail} alt={book.title} style={{ width: '100px' }} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;