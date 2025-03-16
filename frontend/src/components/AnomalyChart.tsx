import { Line, LineChart, Tooltip, XAxis, YAxis } from 'recharts';
import { Incident } from '../types/Incident';

export default function AnomalyChart({ incidents }: { incidents: Incident[] }) {
  return (
    <LineChart width={600} height={300} data={incidents}>
      <XAxis dataKey={'timestamp'} />
      <YAxis />
      <Tooltip />
      <Line type={'monotone'} dataKey={'anomaly_type'} stroke="#8884d8" />
    </LineChart>
  );
}
