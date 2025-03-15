import 'leaflet/dist/leaflet.css';
import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet';
import { GPSData } from '../types/GPSData';

export default function MapComponent({ data }: { data: GPSData[] }) {
  return (
    <MapContainer center={[55.75, 37.61]} zoom={10}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {data.map((point) => (
        <Marker key={point.id} position={[point.latitude, point.longitude]}>
          <Popup>{point.device_id}</Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
