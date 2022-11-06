import "./App.css";

import { BrowserRouter, Route, Routes } from "react-router-dom";

import InteractivePage from "./pages/InteractivePage";
import MonitorOnePage from "./pages/MonitorOnePage";
import MonitorTwoPage from "./pages/MonitorTwoPage";
import { ThemeProvider } from "@emotion/react";

function App() {
  return (
    <div className="App">
      <div
        style={{
          height: "100vh",
          width: "100vw",
          overflow: "hidden",
        }}
      >
        <ThemeProvider theme={{}}>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<InteractivePage />} />
              <Route path="monitor_one" element={<MonitorOnePage />} />
              <Route path="monitor_two" element={<MonitorTwoPage />} />
            </Routes>
          </BrowserRouter>
        </ThemeProvider>
      </div>
    </div>
  );
}

export default App;
