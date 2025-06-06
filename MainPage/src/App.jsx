import "./App.css";
import Router from "./shared/Router";
import axios from "axios";
axios.defaults.withCredentials = true;  // ✅ 모든 요청에 credentials 포함

function App() {
  return <Router />;
}

export default App;
