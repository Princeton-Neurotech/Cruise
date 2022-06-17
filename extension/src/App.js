import NavBar from "./components/NavBar";
import FontSettings from "./components/FontSettings";
import 'bootstrap/dist/css/bootstrap.min.css';
import React from "react";
import Thresholds from "./components/Thresholds";
import DocURL from "./components/DocURL";
import TotalTime from "./components/TotalTime";

function App() {
  return (
    <div className="App">
      <NavBar />
      <TotalTime />
      {/* <DocURL /> */}
      <FontSettings />
      <Thresholds />
    </div>
  );
}

export default App;
