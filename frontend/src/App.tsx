import "./App.css";

import { BrowserRouter, Route, Routes } from "react-router-dom";

import InteractivePage from "./pages/InteractivePage";
import MonitorOnePage from "./pages/MonitorOnePage";
import MonitorTwoPage from "./pages/MonitorTwoPage";

function App() {
  return (
    <div className="App">
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
          width: "100vw",
        }}
      >
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<InteractivePage />} />
            <Route path="monitor_one" element={<MonitorOnePage />} />
            <Route path="monitor_two" element={<MonitorTwoPage />} />
          </Routes>
        </BrowserRouter>
      </div>
    </div>
  );
}

export default App;
