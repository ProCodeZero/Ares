import axios from 'axios';
import { Incident } from '../types/Incident';

export const incidents_url = 'http://localhost:8002';

export const fetchIncidents = async (
  setIncidents: React.Dispatch<React.SetStateAction<Incident[] | null>>
) => {
  try {
    const response = await axios.get(`${incidents_url}/api/incidents`);
    console.log(response);
    setIncidents(response.data);
  } catch (err) {
    console.error(err);
  }
};
