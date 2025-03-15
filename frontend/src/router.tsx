import { createBrowserRouter } from 'react-router-dom';
import MenuLayout from './layouts/MenuLayout';

export const router = createBrowserRouter([{ path: '/', element: <MenuLayout /> }]);
