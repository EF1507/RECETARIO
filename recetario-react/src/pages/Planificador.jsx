// recetario-react/src/pages/Planificador.jsx

import React, { useEffect, useState } from "react";
import {
  fetchIngredientesSemana,
  addToPlanSemanal,
  fetchRecetas,
} from "../services/api";

const TIPOS_COMIDA = ["Desayuno", "Almuerzo", "Merienda", "Cena", "Aperitivo"];

export default function Planificador() {
  const [plan, setPlan] = useState([]);
  const [recetas, setRecetas] = useState([]);
  const [error, setError] = useState(null);
  const [formError, setFormError] = useState(null);

  const [formData, setFormData] = useState({
    receta_id: "",
    fecha_plan: new Date().toISOString().split("T")[0],
    tipo_comida: "Almuerzo",
  });

  // -----------------------------------------------------------------
  // 👇 AQUÍ ESTÁ LA CORRECCIÓN 👇
  // -----------------------------------------------------------------
  const loadPlan = async () => {
    try {
      setError(null);
      // Borramos el estado anterior para que muestre "Cargando..."
      setPlan([]); 
      const data = await fetchIngredientesSemana();
      setPlan(data);
    } catch (err) {
      console.error("Error en loadPlan:", err);
      
      // ------ ESTA ES LA LÓGICA CORREGIDA ------
      // Si el backend envía un mensaje (como el de "no hay recetas")
      if (err.response && err.response.data && err.response.data.mensaje) {
        setPlan({ mensaje: err.response.data.mensaje });
      } else {
        // Para cualquier otro error (500, red, etc.)
        setPlan({ mensaje: "Error al cargar la lista. Intenta de nuevo." });
      }
    }
  };
  // -----------------------------------------------------------------

  const loadRecetas = async () => {
    try {
      const data = await fetchRecetas();
      setRecetas(data);
      if (data.length > 0) {
        setFormData((prev) => ({ ...prev, receta_id: data[0].id }));
      }
    } catch (err) {
      console.error(err);
      setError("Error al cargar la lista de recetas");
    }
  };

  useEffect(() => {
    loadPlan();
    loadRecetas();
  }, []);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError(null);

    if (!formData.receta_id) {
      setFormError("Debes seleccionar una receta.");
      return;
    }

    try {
      await addToPlanSemanal({
        ...formData,
        receta_id: parseInt(formData.receta_id),
      });
      // ¡Éxito! Recargamos la lista de compras
      loadPlan();
    } catch (err) {
      console.error(err);
      setFormError("Error al agregar la receta. Intenta de nuevo.");
    }
  };

  // --- Renderizado ---

  if (error) return <p className="text-danger">{error}</p>;

  const renderListaCompras = () => {
    // Si 'plan' es un objeto con 'mensaje' (error o "vacío")
    if (plan.mensaje) {
      return <p>{plan.mensaje}</p>;
    }
    // Si 'plan' es un array vacío (estado inicial/cargando)
    if (plan.length === 0) {
      return <p>Cargando lista de compras...</p>;
    }

    // Si 'plan' es un array con datos
    return (
      <table className="table table-striped text-dark align-middle">
        <thead className="table-dark">
          <tr>
            <th>Ingrediente</th>
            <th>Cantidad</th>
          </tr>
        </thead>
        <tbody>
          {plan.map((p, i) => (
            <tr key={i}>
              <td>{p.ingrediente}</td>
              <td>
                {p.cantidad_total} {p.unidad}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  return (
    <div>
      <h3>📅 Planificador Semanal</h3>
      
      <form onSubmit={handleSubmit} className="card p-3 mb-4">
        <h5>Agregar Receta al Plan</h5>
        {formError && <p className="text-danger">{formError}</p>}
        <div className="row">
          <div className="col-md-4 mb-2">
            <label htmlFor="receta_id" className="form-label">Receta</label>
            <select
              name="receta_id"
              id="receta_id"
              className="form-select"
              value={formData.receta_id}
              onChange={handleChange}
            >
              <option value="">-- Selecciona una receta --</option>
              {recetas.map((receta) => (
                <option key={receta.id} value={receta.id}>
                  {receta.titulo}
                </option>
              ))}
            </select>
          </div>

          <div className="col-md-3 mb-2">
            <label htmlFor="fecha_plan" className="form-label">Fecha</label>
            <input
              type="date"
              name="fecha_plan"
              id="fecha_plan"
              className="form-control"
              value={formData.fecha_plan}
              onChange={handleChange}
            />
          </div>

          <div className="col-md-3 mb-2">
            <label htmlFor="tipo_comida" className="form-label">Comida</label>
            <select
              name="tipo_comida"
              id="tipo_comida"
              className="form-select"
              value={formData.tipo_comida}
              onChange={handleChange}
            >
              {TIPOS_COMIDA.map((tipo) => (
                <option key={tipo} value={tipo}>{tipo}</option>
              ))}
            </select>
          </div>

          <div className="col-md-2 d-flex align-items-end mb-2">
            <button type="submit" className="btn btn-primary w-100">
              Agregar
            </button>
          </div>
        </div>
      </form>

      <div className="card p-3">
        <h5>Lista de Compras de la Semana</h5>
        {renderListaCompras()}
      </div>

    </div>
  );
}