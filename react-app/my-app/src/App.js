import logo from './logo.svg';
import './App.css';
import socketio from "socket.io-client";
import { SOCKET_URL } from "config";

export const socket = socketio.connect(SOCKET_URL);
export const SocketContext = React.createContext();

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
