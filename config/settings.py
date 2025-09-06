import { useState, useEffect } from 'react';
import './App.css';
import ServicioForm from './ServicioForm';

interface Servicio {
  id: number;
  cliente: string;
  fecha: string;
  cantidad: number;
  descripcion_servicio: string;
}

function App() {
  const [servicios, setServicios] = useState<Servicio[]>([]);
  const [csrfToken, setCsrfToken] = useState<string>('');

  useEffect(() => {
    // 1. Pedimos el token de seguridad al cargar la app.
    const fetchCsrfToken = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/get-csrf-token/', {
          // AÑADIMOS ESTA LÍNEA: Le dice al navegador que envíe y reciba cookies.
          credentials: 'include',
        });
        const data = await response.json();
        setCsrfToken(data.csrfToken);
      } catch (error) {
        console.error('Error al obtener el token CSRF:', error);
      }
    };

    fetchCsrfToken();
    fetchServicios();
  }, []);

  // 2. Obtenemos la lista de servicios.
  const fetchServicios = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/servicios/', {
        // AÑADIMOS ESTA LÍNEA TAMBIÉN AQUÍ.
        credentials: 'include',
      });
      const data = await response.json();
      setServicios(data);
    } catch (error) {
      console.error('Error al obtener los datos:', error);
    }
  };

  // 3. Enviamos el nuevo servicio para guardarlo.
  const handleGuardarServicio = async (nuevoServicio: Omit<Servicio, 'id'>) => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/servicios/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        // AÑADIMOS ESTA LÍNEA AQUÍ TAMBIÉN.
        credentials: 'include',
        body: JSON.stringify(nuevoServicio)
      });

      if (response.ok) {
        fetchServicios();
      } else {
        console.error('Error al guardar el servicio');
      }
    } catch (error) {
      console.error('Error de red al intentar guardar:', error);
    }
  };

  return (
    <div className="app-container">
      <ServicioForm onGuardar={handleGuardarServicio} />
      <div className="card">
        <h1 className="title">Bitácora de Servicios - React</h1>
        <ul className="service-list">
          {servicios.map((servicio) => (
            <li key={servicio.id} className="service-item">
              <h3 className="service-client">{servicio.cliente}</h3>
              <p className="service-meta">
                {servicio.fecha} - Cantidad: {servicio.cantidad}
              </p>
              <p className="service-description">{servicio.descripcion_servicio}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;