import { Incident } from '../../types/Incident';
import styles from './incidentsList.module.css';

export default function IncidentsList({ incidents }: { incidents: Incident[] }) {
  return (
    <>
      <h2>Incidents List</h2>
      <ul className={styles['inc-list']}>
        <li>
          <span>
            <b>ID</b>
          </span>
          <span>
            <b>ID оборудования</b>
          </span>
          <span>
            <b>Тип аномалии</b>
          </span>
          <span>
            <b>Широта</b>
          </span>
          <span>
            <b>Долгота</b>
          </span>
          <span>
            <b>Время</b>
          </span>
        </li>
        {incidents ? (
          incidents.map((incident) => (
            <li key={incident.id + incident.timestamp}>
              <span>{incident.id}</span>
              <span>{incident.device_id}</span>
              <span>{incident.anomaly_type}</span>
              <span>{incident.latitude}</span>
              <span>{incident.longitude}</span>
              <span>{incident.timestamp}</span>
            </li>
          ))
        ) : (
          <div>There are no incidents</div>
        )}
      </ul>
    </>
  );
}
