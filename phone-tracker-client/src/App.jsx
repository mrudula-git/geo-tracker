import React, { useState } from "react";
import axios from "axios";
import Header from "./Header";
import "./App.css";

function App() {
  const [number, setNumber] = useState("");
  const [info, setInfo] = useState(null);
  const [error, setError] = useState("");

  const handleTrack = async () => {
    setError("");
    setInfo(null);

    try {
      const res = await axios.post("http://localhost:8080/track", { number });
      if (res.data.error) {
        setError(res.data.error);
      } else {
        setInfo(res.data);
      }
    } catch (err) {
      console.log(err);
      setError("Something went wrong. Check backend or phone number.");
    }
  };

  return (
    <>
      <Header />
      <div className="container-fluid">
        <div className="input-wrapper">
          <input
            type="text"
            placeholder="+14155552671"
            value={number}
            onChange={(e) => setNumber(e.target.value)}
          />
          <button onClick={handleTrack}>Track</button>
        </div>

        {error && <p className="error">❌ {error}</p>}

        {info && (
          <div className="result-container">
            <div className="info">
              <p>
                🌍 Location: <strong>{info.location}</strong>
              </p>
              <p>
                📡 Carrier: <strong>{info.carrier}</strong>
              </p>
              <p>
                🌐 Map URL:{" "}
                <a href={info.map_url} target="_blank" rel="noreferrer">
                  {info.map_url}
                </a>
              </p>
            </div>
            <iframe src={info.map_url} title="Map" className="map"></iframe>
          </div>
        )}
      </div>
    </>
  );
}

export default App;
