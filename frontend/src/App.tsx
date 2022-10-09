import "./App.css";
import { Routes, Route } from "react-router";
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
          <Route path="/">
            <InteractivePage />
          </Route>
          <Route path="monitor_one">
            <MonitorOnePage />
          </Route>
          <Route path="monitor_two">
            <MonitorTwoPage />
          </Route>
        </Routes>
      </div>
    </div>
  );
}

export default App;
