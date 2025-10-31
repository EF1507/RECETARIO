// 1. Importar funciones de la API
import React, { useState, useEffect } from "react";
import { fetchIngredientes, createIngrediente } from "../services/api"; 

// 2. Definir estado inicial limpio
const initialState = {
  titulo: "",
  instrucciones: "",
  tiempo_preparacion: "",
  tiempo_coccion: "",
  url_imagen: ""
};

export default function RecetaForm({ onSubmit, initial = null, onCancel }) {
  const [form, setForm] = useState(initialState);
  
  // 3. Nuevos estados para la lógica de ingredientes
  const [allIngredientes, setAllIngredientes] = useState([]); // Para el dropdown
  const [selectedIngredientes, setSelectedIngredientes] = useState([]); // Para la lista
  const [nuevoIngrediente, setNuevoIngrediente] = useState(""); // Para el input '+'

  // 4. Cargar todos los ingredientes (para el dropdown) al iniciar
  useEffect(() => {
    async function loadAllIngredientes() {
      try {
        const data = await fetchIngredientes();
        setAllIngredientes(data);
      } catch (err) {
        console.error("Error al cargar ingredientes", err);
      }
    }
    loadAllIngredientes();
  }, []); // Cargar solo una vez

  // 5. Cargar datos de la receta si estamos en modo "Editar"
  useEffect(() => {
    if (initial) {
      setForm(initial);
      // Asume que el backend devuelve 'initial.ingredientes' como un array de objetos
      setSelectedIngredientes(initial.ingredientes || []); 
    } else {
      setForm(initialState);
      setSelectedIngredientes([]);
    }
  }, [initial]);

  // 6. Manejador para el dropdown (select)
  function handleSelectIngrediente(e) {
    const idSeleccionado = parseInt(e.target.value);
    if (!idSeleccionado) return;

    // Evitar duplicados
    if (selectedIngredientes.find(ing => ing.id === idSeleccionado)) return;

    const ingrediente = allIngredientes.find(ing => ing.id === idSeleccionado);
    setSelectedIngredientes([...selectedIngredientes, ingrediente]);
  }
  
  // 7. Manejador para el botón '+' (crear ingrediente al vuelo)
  async function handleCrearNuevoIngrediente() {
    if (!nuevoIngrediente) return;
    try {
      const data = await createIngrediente({ nombre: nuevoIngrediente });
      setAllIngredientes([...allIngredientes, data]); // Actualizar dropdown
      setSelectedIngredientes([...selectedIngredientes, data]); // Añadir a la receta
      setNuevoIngrediente(""); // Limpiar input
    } catch (err) {
      console.error("Error al crear ingrediente", err);
    }
  }
  
  // 8. Manejador del submit (enviar todo el formulario)
  function submit(e) {
    e.preventDefault();
    onSubmit({
      ...form, // titulo, instrucciones, etc.
      tiempo_preparacion: parseInt(form.tiempo_preparacion) || null,
      tiempo_coccion: parseInt(form.tiempo_coccion) || null,
      
      // Enviar solo la lista de IDs de ingredientes
      ingredientes: selectedIngredientes.map(ing => ing.id)
    });
    
    // Limpiar formulario si era "Crear"
    if (!initial) {
      setForm(initialState);
      setSelectedIngredientes([]);
    }
  }

  return (
    <form onSubmit={submit}>
      {/* --- Título --- */}
      <div className="mb-3">
        <label className="form-label">Título</label>
        <input className="form-control" placeholder="Título" value={form.titulo} onChange={e => setForm({ ...form, titulo: e.target.value })} />
      </div>

      {/* --- Instrucciones --- */}
      <div className="mb-3">
        <label className="form-label">Instrucciones</label>
        <textarea className="form-control" placeholder="Instrucciones" value={form.instrucciones} onChange={e => setForm({ ...form, instrucciones: e.target.value })} />
      </div>

      {/* --- Sección de Ingredientes --- */}
      <div className="mb-3">
        <label className="form-label">Ingredientes</label>
        
        {/* 9. Dropdown de ingredientes existentes */}
        <select className="form-select" onChange={handleSelectIngrediente} value="">
          <option value="">-- Seleccionar ingrediente --</option>
          {allIngredientes.map(ing => (
            <option key={ing.id} value={ing.id}>{ing.nombre}</option>
          ))}
        </select>
        
        {/* 10. Lista de ingredientes seleccionados (con botón de borrar) */}
        <ul className="list-group list-group-flush mt-2">
          {selectedIngredientes.length === 0 ? (
             <li className="list-group-item" style={{backgroundColor: 'transparent', color: '#000'}}>
               No hay ingredientes seleccionados.
             </li>
          ) : (
            selectedIngredientes.map(ing => (
              <li key={ing.id} className="list-group-item d-flex justify-content-between align-items-center" style={{backgroundColor: 'transparent', color: '#000'}}>
                {ing.nombre}
                <button 
                  type="button" 
                  className="btn-close" 
                  aria-label="Remove"
                  onClick={() => setSelectedIngredientes(selectedIngredientes.filter(i => i.id !== ing.id))}
                ></button>
              </li>
            ))
          )}
        </ul>
      </div>

      {/* 11. Input para "Nuevo ingrediente" con botón '+' */}
      <div className="mb-3">
        <label className="form-label">Nuevo ingrediente</label>
        <div className="input-group">
          <input 
            type="text"
            className="form-control"
            placeholder="Ej: Tomate"
            value={nuevoIngrediente}
            onChange={e => setNuevoIngrediente(e.target.value)}
          />
          <button 
            className="btn btn-outline-primary" 
            type="button" 
            onClick={handleCrearNuevoIngrediente}
          >
            +
          </button>
        </div>
      </div>
      
      {/* --- Tiempos --- */}
      <div className="row">
        <div className="col-md-6 mb-3">
          <label className="form-label">Tiempo preparación (min)</label>
          <input className="form-control" placeholder="Ej: 15" type="number" value={form.tiempo_preparacion} onChange={e => setForm({ ...form, tiempo_preparacion: e.target.value })} />
        </div>
        <div className="col-md-6 mb-3">
          <label className="form-label">Tiempo cocción (min)</label>
          <input className="form-control" placeholder="Ej: 30" type="number" value={form.tiempo_coccion} onChange={e => setForm({ ...form, tiempo_coccion: e.target.value })} />
        </div>
      </div>

      {/* --- URL Imagen --- */}
      <div className="mb-3">
        <label className="form-label">URL Imagen</label>
        <input className="form-control" placeholder="https://ejemplo.com/imagen.jpg" value={form.url_imagen} onChange={e => setForm({ ...form, url_imagen: e.target.value })} />
      </div>

      {/* --- Botones --- */}
      <div className="d-flex gap-2">
        <button type="submit" className="btn btn-primary">{initial ? "Guardar Cambios" : "Crear Receta"}</button>
        {onCancel && <button type="button" className="btn btn-secondary" onClick={onCancel}>Cancelar</button>}
      </div>
    </form>
  );
}
