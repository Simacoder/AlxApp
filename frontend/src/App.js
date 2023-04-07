
import './App.css';
import {useState, useEffect} from 'react';

function App() {
  const [reports, setReports]= useState([])

  useEffect(() => {
    fetch(() => {

      fetch('http://127.0.0.1:5000/get', {
        'methods':'GET',
        headers:{
          'Content-Type': 'application/json'
        }
      })
      .then(res => res.json())
      .then(res => setReports(res))
      .catch(error => console.log(error))

    }, [])

  }, [])
  return (
    <div className="App">
      <h1>eDustbin: Your pocket dustbin</h1>
      {reports.map(report => {
        return (
          <div key = {report.id}>
           <h2>{report.title}</h2>
           <p>{report.body}</p>
           <p>{report.date}</p>

          </div>
        )
      })}
    </div>
  );
}

export default App;
