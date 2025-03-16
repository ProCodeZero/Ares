import 'leaflet/dist/leaflet.css';
import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet';
import { Incident } from '../types/Incident';

export default function IncidentsMap({ incidents }: { incidents: Incident[] }) {
  return (
    <MapContainer center={[55.75, 37.61]} zoom={10}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {incidents
        ? incidents.map((incident) => (
            <Marker key={incident.id} position={[incident.latitude, incident.longitude]}>
              <Popup>{incident.device_id}</Popup>
            </Marker>
          ))
        : null}
    </MapContainer>
  );
}
