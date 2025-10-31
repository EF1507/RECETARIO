import React, { useState } from "react";
import { login, setAuthHeader } from "../services/api";

export default function Login() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");

  async function handleLogin(e) {
    e.preventDefault();
    try {
      const data = await login(form.username, form.password);
      const token = data.access_token;
      if (token) {
        localStorage.setItem("token", token);
        setAuthHeader(token);
        window.location.reload(); // refresca para mostrar las recetas
      }
    } catch (err) {
      console.error(err);
      setError("Credenciales inválidas o servidor no disponible");
    }
  }

  // --- JSX Actualizado con Bootstrap ---
  return (
    // Usamos flex-fill para que ocupe el espacio disponible
    <div className="flex-fill"> 
      <h3 className="text-dark">Iniciar Sesión</h3>
      <form onSubmit={handleLogin}>
        
        <div className="mb-3">
          <label className="form-label">Usuario</label>
          <input
            className="form-control" // Clase de Bootstrap
            placeholder="Usuario"
            value={form.username}
            onChange={(e) => setForm({ ...form, username: e.target.value })}
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Contraseña</label>
          <input
            type="password"
            className="form-control" // Clase de Bootstrap
            placeholder="Contraseña"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />
        </div>
        
        <button type="submit" className="btn btn-primary w-100">Entrar</button>
      
      </form>
      
      {error && (
        <div className="alert alert-danger mt-3 p-2">
          {error}
        </div>
      )}
    </div>
  );
}
