import React from 'react';
import UploadForm from './UploadForm';
import SearchForm from './SearchForm';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Research Paper Data Management</h1>
      </header>
      <UploadForm />
      <SearchForm />
    </div>
  );
}

export default App;
