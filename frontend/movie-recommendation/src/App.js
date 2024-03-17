import React, { useState } from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false); 
  const API_URL = 'http://localhost:8000/send_message/';

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
        setSearchResults(results);
      }
    } catch (error) {
      console.error("Failed to fetch: ", error);
      setSearchResults([]);
    } finally {
      setIsSearching(false); 
    }
  };

  const parseResults = (resultsString) => {
    // Split the string by 'index:' to get individual movies
    // Filter out any empty strings that might result from the split
    const movies = resultsString.split('index:').filter(text => text.trim() !== '');
  
    return movies.map((movie, index) => {
      // Further split each movie's details and trim whitespace
      const details = movie.split('\n').map(detail => detail.trim()).filter(detail => detail !== '');
      
      // Convert the details into an object
      const movieObj = {};
      details.forEach(detail => {
        const [key, value] = detail.split(':').map(part => part.trim());
        if (key && value) {
          movieObj[key.toLowerCase()] = value;
        }
      });
  
      // Add an index property for consistency with the original data
      movieObj.index = index;
  
      return movieObj;
    });
  };

  return (
    <div>
      <div>
        <input
          type='text'
          value={text}
          onChange={(e) => setText(e.target.value)}
          style={{ width: '80%', height: '40px', fontSize: '15px', padding: '0 10px' }}
        />
      </div>
      <div>
        <button onClick={handleSearch} disabled={isSearching} style={{ fontSize: '15px', padding: '8px 16px' }}>
          {isSearching ? 'Processing...' : 'Send message'}
        </button>
      </div>
      <div>
        {searchResults.response && <p>Response: {searchResults.response}</p>}
        {searchResults.results && (
          <ul style={{ listStyleType: 'none', padding: 0 }}>
            {parseResults(searchResults.results).map((result, index, array) => (
              <li key={index} style={{
                paddingBottom: '10px',
                marginBottom: '10px',
                borderBottom: '1px dashed #ccc',
                ...(index === array.length - 1 && { borderBottom: 'none' }) // Remove the border for the last item
              }}>
                <strong>Title:</strong> {result.title} <br />
                <strong>Genres:</strong> {result.genres} <br />
                <strong>Overview:</strong> {result.overview}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
  
  
  // return (
  //   <div>
  //     <input type='text' value={text} onChange={(e) => setText(e.target.value)} />
  //     <button onClick={handleSearch} disabled={isSearching}>
  //       {isSearching ? 'Processing...' : 'Send message'}
  //     </button>
  //     <div>
  //       {searchResults.response && <p>Response: {searchResults.response}</p>}
  //       {searchResults.results && (
  //         <ul>
  //           {parseResults(searchResults.results).map((result, index) => (
  //             <li key={index}>
  //               <strong>Title:</strong> {result.title} <br />
  //               <strong>Genres:</strong> {result.genres} <br />
  //               <strong>Overview:</strong> {result.overview}
  //               <strong></strong>
  //             </li>
  //           ))}
  //         </ul>
  //       )}
  //     </div>
  //   </div>
  // );
  

  // return (
  //   <div>
  //     <input type='text' value={text} onChange={(e) => setText(e.target.value)} />
  //     <button onClick={handleSearch} disabled={isSearching}>
  //       {isSearching ? 'Processing...' : 'Send message'}
  //     </button>
  //       <div>
  //         {searchResults.response && <p>Response: {searchResults.response}</p>}
  //         {searchResults.results && (
  //           <pre>{searchResults.results}</pre>
  //         )}
  //       </div>

  //   </div>
  // );
  

  // return (
  //   <div>
  //     <input type='text' value={text} onChange={(e) => setText(e.target.value)} />
  //     <button onClick={handleSearch} disabled={isSearching}>
  //       {isSearching ? 'Processing...' : 'Send message'}
  //     </button>
  //     <div>
  //       {searchResults && searchResults.map((book, index) => (
  //         <div key={index} style={{ padding: '10px', margin: '10px', border: '1px solid black' }}>
  //           <h3>{book.title}</h3>
  //           <p><strong>Authors:</strong> {book.authors}</p>
  //           <p><strong>Description:</strong> {book.description}</p>
  //           <p><strong>Average Rating:</strong> {book.average_rating}</p>
  //           <p><strong>Published Year:</strong> {book.published_year}</p>
  //           <img src={book.thumbnail} alt={book.title} style={{ width: '100px' }} />
  //         </div>
  //       ))}
  //     </div>
  //   </div>
  // );
}

export default App;