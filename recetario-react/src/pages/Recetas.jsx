// src/pages/Recetas.jsx
import React, { useEffect, useState } from "react";
import { fetchRecetas, createReceta, updateReceta, deleteReceta } from "../services/api";
import RecetaForm from "../components/RecetaForm";

export default function Recetas() {
  const [recetas, setRecetas] = useState([]);
  const [editing, setEditing] = useState(null);

  // Cargar recetas
  async function load() {
    const r = await fetchRecetas();
    setRecetas(r);
  }
  useEffect(()=>{ load(); }, []);
  async function handleCreate(data) {
    await createReceta(data);
    load();
  }
  async function handleUpdate(id, data) {
    await updateReceta(id, data);
    setEditing(null);
    load();
  }
  async function handleDelete(id) {
    if (!confirm("Eliminar receta?")) return;
    await deleteReceta(id);
    load();
  }

  return (
    <div>

      
      <h2 className="text-dark mt-4">Mis Recetas</h2>
      
      <RecetaForm onSubmit={handleCreate} />
      
      <hr className="my-4" /> 

      {/* --- Tabla de Recetas --- */}
      <div className="table-responsive">
        <table className="table table-striped text-dark align-middle">
          <thead className="table-dark">
            <tr>
              <th>Título</th>
              <th>Preparación (min)</th>
              <th>Cocción (min)</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {recetas.map(r=>(
              <tr key={r.id}>
                <td>{r.titulo}</td>
                <td>{r.tiempo_preparacion}</td>
                <td>{r.tiempo_coccion}</td> 
                <td>
                  <button 
                    className="btn btn-warning btn-sm me-2" 
                    onClick={()=>setEditing(r)}>
                    Editar
                  </button>
                  <button 
                    className="btn btn-danger btn-sm"
                    onClick={()=>handleDelete(r.id)}>
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Formulario de Edición */}
      {editing && (
        <div className="mt-5 p-3 border rounded bg-light">
          <h3>Editar receta #{editing.id}</h3>
          <RecetaForm 
            initial={editing} 
            onSubmit={(data)=>handleUpdate(editing.id, data)} 
            onCancel={()=>setEditing(null)} 
          />
        </div>
      )}
    </div>
  );
}