// recetario-react/src/app.jsx

// IMPORTS
import React, { useEffect, useState } from "react";
import Recetas from "./pages/Recetas";
import Planificador from "./pages/Planificador";
import Estadisticas from "./pages/Estadisticas";
import Login from "./auth/Login";
import Register from "./auth/Register";
import { setAuthHeader } from "./services/api";

export default function App() {
  const [view, setView] = useState("recetas");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) setAuthHeader(token);
  }, []);

  const isLogged = !!localStorage.getItem("token");

  if (!isLogged) {
    return (
      <div className="container py-4">
        <div className="row justify-content-center">
          <div className="col-lg-10 col-xl-8">
            <div className="glass-container p-4">
              <h1 className="text-dark">SmartChef</h1>
              <hr />
              <div style={{ display: "flex", gap: 20 }}>
                <Login />
                <Register />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Si el usuario está logueado, muestra el panel principal
  return (
    <div className="container py-4">
      <div className="row justify-content-center">
        <div className="col-lg-10 col-xl-8">
          <div className="glass-container p-4">
            <h1 className="text-dark">SmartChef👨‍🍳</h1>
            <hr />

            {/* Navegación principal */}
            <div className="d-flex justify-content-between align-items-center mb-3">
              <div className="btn-group">
                <button
                  className={`btn btn-${view === "recetas" ? "dark" : "light"}`}
                  onClick={() => setView("recetas")}
                >
                  Mis Recetas
                </button>
                <button
                  className={`btn btn-${view === "planificador" ? "dark" : "light"}`}
                  onClick={() => setView("planificador")}
                >
                  Planificador
                </button>
                <button
                  className={`btn btn-${view === "estadisticas" ? "dark" : "light"}`}
                  onClick={() => setView("estadisticas")}
                >
                  Estadísticas
                </button>
              </div>

              <button
                className="btn btn-outline-secondary"
                onClick={() => {
                  localStorage.removeItem("token");
                  window.location.reload();
                }}
              >
                Logout
              </button>
            </div>

            {/* Contenido dinámico */}
            <div className="mt-4">
              {view === "recetas" && <Recetas />}
              {view === "planificador" && <Planificador />}
              {view === "estadisticas" && <Estadisticas />}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
