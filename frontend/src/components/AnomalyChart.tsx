import { Line, LineChart, Tooltip, XAxis, YAxis } from 'recharts';
import { Anomaly } from '../types/Anomaly';

export default function AnomalyChart({ data }: { data: Anomaly[] }) {
  return (
    <LineChart width={600} height={300} data={data}>
      <XAxis dataKey={'timestamp'} />
      <YAxis />
      <Tooltip />
      <Line type={'monotone'} dataKey={'anomaly_type'} stroke="#8884d8" />
    </LineChart>
  );
}
