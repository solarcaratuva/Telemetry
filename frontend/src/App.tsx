import "./App.css";

import { Route, Routes } from "react-router";

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
        <Routes>
          <Route path="/" element={<InteractivePage />} />
          <Route path="monitor_one" element={<MonitorOnePage />} />
          <Route path="monitor_two" element={<MonitorTwoPage />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
