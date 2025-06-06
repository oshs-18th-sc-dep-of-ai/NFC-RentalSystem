import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import axios from "axios";
axios.defaults.withCredentials = true;  // ✅ 모든 요청에 credentials 포함


createRoot(document.getElementById("root")).render(<App />);
