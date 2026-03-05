import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import GenerateReport from './pages/GenerateReport';
import ChangeReference from './pages/ChangeReference';
import GetReport from './pages/GetReport';
import './index.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="generate" element={<GenerateReport />} />
          <Route path="reference" element={<ChangeReference />} />
          <Route path="get" element={<GetReport />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;