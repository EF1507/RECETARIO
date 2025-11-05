// recetario-react/src/services/api.js

// IMPORTS
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const instance = axios.create({
  baseURL: API_BASE,
});

export function setAuthHeader(token) {
  if (token) {
    instance.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete instance.defaults.headers.common["Authorization"];
  }
}

export async function login(username, password) {
  const form = new URLSearchParams();
  form.append("username", username);
  form.append("password", password);
  const r = await instance.post("/auth/login", form);
  return r.data;
}

export async function register(user) {
  const r = await instance.post("/auth/register", user);
  return r.data;
}

// === RECETAS ===
export async function fetchRecetas() {
  const r = await instance.get("/recetas");
  return r.data;
}

export async function createReceta(data) {
  const r = await instance.post("/recetas", data);
  return r.data;
}

export async function updateReceta(id, data) {
  const r = await instance.put(`/recetas/${id}`, data);
  return r.data;
}

export async function deleteReceta(id) {
  const r = await instance.delete(`/recetas/${id}`);
  return r.data;
}

// === INGREDIENTES ===
export async function fetchIngredientes() {
  const r = await instance.get("/ingredientes");
  return r.data;
}

export async function createIngrediente(data) {
  const r = await instance.post("/ingredientes", data);
  return r.data;
}

// === PLANIFICADOR (CORREGIDO) ===
// 1. Nombre de función y URL corregidos
export async function fetchIngredientesSemana() {
  const r = await instance.get("/planificador/ingredientes-semana");
  return r.data;
}

// (Mantenemos estas aunque no las usemos por ahora)
export async function addToPlanSemanal(data) {
  // data debe ser: { receta_id: 1, fecha_plan: "2025-10-31", tipo_comida: "Cena" }
  const r = await instance.post("/planificador/", data);
  return r.data;
}

export async function deleteFromPlanSemanal(id) {
  const r = await instance.delete(`/planificador/${id}`);
  return r.data;
}

export async function fetchStatsIngredientes() {
  const r = await instance.get("/estadisticas/ingredientes-populares");
  return r.data;
}

export default instance;

