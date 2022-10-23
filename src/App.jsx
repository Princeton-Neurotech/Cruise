import NavBar from "./components/NavBar";
import FontSettings from "./components/FontSettings";
import 'bootstrap/dist/css/bootstrap.min.css';
import React from "react";
import { initializeApp } from "firebase/app";
// import App from './App';
import Thresholds from "./components/Thresholds";
import DocURL from "./components/DocURL";
import TotalTime from "./components/TotalTime";
const cors = require('cors')

function App() {
  const firebaseConfig = { 
    apiKey: "AIzaSyBbqaOCwIZocSgjT1-Z1JAlWlr5obER7Z0",
    authDomain: "cruise-e8304.firebaseapp.com",
    projectId: "cruise-e8304",
    storageBucket: "cruise-e8304.appspot.com",
    messagingSenderId: "665446251636",
    appId: "1:665446251636:web:4bb27580e5f968c112a521",
    measurementId: "G-4B33G21KR0"
  };

  // const admin = require('firebase-admin');
  initializeApp(firebaseConfig)

  return (
    <div className="App">
      {/* <NavBar /> */}
      { /* <TotalTime /> */ }
      {/* <DocURL /> */}
      {/* <FontSettings /> */}
      <Thresholds />
    </div>
  );
}

export default App;
