import React, { useState } from "react";
import { register } from "../services/api";

export default function Register() {
  const [user, setUser] = useState({ nombre_usuario: "", email: "", password: "" });
  const [msg, setMsg] = useState("");
  const [error, setError] = useState(""); // Estado separado para errores

  async function submit(e) {
    e.preventDefault();
    setError("");
    setMsg("");
    try {
      await register(user);
      setMsg("¡Registrado correctamente! Ya podés iniciar sesión.");
      // Limpiar formulario
      setUser({ nombre_usuario: "", email: "", password: "" });
    } catch (err) {
      setError("Error al registrar. Revisa los datos (quizás el usuario o email ya existe).");
    }
  }

  // --- JSX Actualizado con Bootstrap ---
  return (
    // Usamos flex-fill para que ocupe el espacio disponible
    <div className="flex-fill">
      <h3 className="text-dark">Registro</h3>
      <form onSubmit={submit}>
        
        <div className="mb-3">
          <label className="form-label">Usuario</label>
          <input 
            className="form-control" // Clase de Bootstrap
            placeholder="Usuario" 
            value={user.nombre_usuario} 
            onChange={e=>setUser({...user, nombre_usuario:e.target.value})} 
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Email</label>
          <input 
            className="form-control" // Clase de Bootstrap
            placeholder="Email" 
            value={user.email} 
            onChange={e=>setUser({...user, email:e.target.value})} 
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Contraseña</label>
          <input 
            placeholder="Contraseña" 
            type="password" 
            className="form-control" // Clase de Bootstrap
            value={user.password} 
            onChange={e=>setUser({...user, password:e.target.value})} 
          />
        </div>

        <button type="submit" className="btn btn-success w-100">Registrar</button>
      
      </form>
      
      {msg && (
        <div className="alert alert-success mt-3 p-2">{msg}</div>
      )}
      {error && (
        <div className="alert alert-danger mt-3 p-2">{error}</div>
      )}
    </div>
  );
}
