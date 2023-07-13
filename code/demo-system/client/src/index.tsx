/**
 * @file index.tsx
 * @author Henry Schuler
 */
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './app/App';
import reportWebVitals from './reportWebVitals';
import { config } from "@fortawesome/fontawesome-svg-core";
import "@fortawesome/fontawesome-svg-core/styles.css";
import Chart, { CategoryScale } from 'chart.js/auto';
config.autoAddCss = false;
Chart.register(CategoryScale)

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <header className="App-header">
      <h1>
        Authentifizierung von Benutzern mittels Sprechererkennung
      </h1>
    </header>
    <App />
    <footer className="App-footer">
      Johannes Brandenburger, Lukas Braun, Henry Schuler
    </footer>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
