import { useEffect, useState } from 'react';
import AnomalyChart from '../components/AnomalyChart';
import IncidentsList from '../components/IncidentsList/IncidentsList';
import IncidentsMap from '../components/MapComponent';
import { Incident } from '../types/Incident';
import styles from './menuLayout.module.css';

export default function MenuLayout() {
  const [incidents, setIncidents] = useState<Incident[]>([]);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8002/ws/incidents');

    ws.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      const newIncident = JSON.parse(event.data);
      setIncidents((prev) => [...prev, newIncident]);
    };

    ws.onerror = (error) => {
      console.error('WebSocket Error:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <>
      {incidents.length > 0 ? (
        <>
          <div>
            <IncidentsList incidents={incidents} />
          </div>
          <div className={styles['map-wrapper']}>
            <IncidentsMap incidents={incidents} />
          </div>
          <div>
            <AnomalyChart incidents={incidents} />
          </div>
        </>
      ) : (
        <div>Инциденты не получены</div>
      )}
    </>
  );
}
