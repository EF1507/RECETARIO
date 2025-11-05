// src/auth/AuthContext.jsx
import React, { createContext, useState, useContext } from 'react';

// 1. Creamos el contexto (el molde del pase)
const AuthContext = createContext(null);

// 2. Creamos el "Proveedor" (la empresa que da los pases)
// Este componente envolverá toda nuestra aplicación
export const AuthProvider = ({ children }) => {
  // Guardamos el token en el estado de React
  // Intentamos leer el token de localStorage por si ya había iniciado sesión
  const [token, setToken] = useState(localStorage.getItem('accessToken'));

  // Función para "iniciar sesión"
  const login = (newToken) => {
    localStorage.setItem('accessToken', newToken);
    setToken(newToken);
  };

  // Función para "cerrar sesión"
  const logout = () => {
    localStorage.removeItem('accessToken');
    setToken(null);
  };

  // El "pase" tendrá el token y las funciones de login/logout
  const value = {
    token,
    login,
    logout,
    isAuthenticated: !!token // Un booleano rápido para saber si está logueado
  };

  // Ofrecemos este "pase" a todos los componentes hijos
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// 3. Creamos un "Hook" personalizado (la forma fácil de usar el pase)
// En lugar de importar 'useContext' y 'AuthContext' en cada archivo,
// solo importaremos 'useAuth'
export const useAuth = () => {
  return useContext(AuthContext);
};