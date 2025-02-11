import "./App.css";
import React, { useState } from "react";
import Header from "./components/header";
import Content from "./components/content";

function App() {
  return (
    <>
      <div className="App">
        <Header />
        <Content />
      </div>
    </>
  );
}

export default App;
