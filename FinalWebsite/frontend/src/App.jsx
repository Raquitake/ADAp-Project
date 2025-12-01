import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Inicio from './pages/Inicio';
import QuienesSomos from './pages/QuienesSomos';
import Contacto from './pages/Contacto';
import Eventos from './pages/Eventos';
import Donar from './pages/Donar';
import Socios from './pages/Socios';
import ComprarEntrada from './pages/ComprarEntrada';
import Login from './pages/Login';
import Register from './pages/Register';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/" element={<Inicio />} />
          <Route path="/quienessomos" element={<QuienesSomos />} />
          <Route path="/contacto" element={<Contacto />} />
          <Route path="/eventos" element={<Eventos />} />
          <Route path="/donar" element={<Donar />} />
          <Route path="/socios" element={<Socios />} />
          <Route path="/comprarentrada" element={<ComprarEntrada />} />
          <Route path="/login" element={<Login />} />
          <Route path="/registro" element={<Register />} />
          {/* Add other routes here as we migrate pages */}
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
