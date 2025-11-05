// recetario-react/src/pages/Estadisticas.jsx

// IMPORTS
import React, { useEffect, useState } from "react";
import { fetchStatsIngredientes } from "../services/api";

export default function Estadisticas() {
  // 2. El estado solo guarda el string de la imagen
  const [chartImage, setChartImage] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        // 3. Llamar a la función NUEVA
        const data = await fetchStatsIngredientes();
        
        // 4. Guardar la imagen (si existe)
        if (data.imagen) {
          setChartImage(data.imagen);
        }
      } catch (err) {
        console.error(err);
        setError("Error al cargar estadísticas");
      }
    }
    load();
  }, []);

  if (error) return <p>{error}</p>;

  return (
    <div>
      <h3>📊 Estadísticas de la Semana</h3>
      
      {/* 5. Mostrar la imagen (si existe) */}
      {chartImage ? (
        <div className="mt-3">
          <h5 className="text-dark">Ingredientes más usados</h5>
          <img 
            src={chartImage} 
            alt="Ingredientes más usados" 
            className="img-fluid border rounded" 
          />
        </div>
      ) : (
        <p>No hay datos de ingredientes para mostrar.</p>
      )}
    </div>
  );
}

