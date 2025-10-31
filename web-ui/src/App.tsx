import { Routes, Route } from 'react-router-dom';
import { Layout } from '@/components/Layout';
import { Dashboard } from '@/pages/Dashboard';
import { ConceptsPage } from '@/pages/ConceptsPage';
import { TimelinePage } from '@/pages/TimelinePage';
import { SnapshotsPage } from '@/pages/SnapshotsPage';
import DhatuDashboard from'@/pages/DhatuDashboard';

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/concepts" element={<ConceptsPage />} />
        <Route path="/timeline" element={<TimelinePage />} />
        <Route path="/snapshots" element={<SnapshotsPage />} />
        <Route path="/dhatu" element={<DhatuDashboard />} />
      </Routes>
    </Layout>
  );
}

export default App;
