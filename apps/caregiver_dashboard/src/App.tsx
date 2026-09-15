import React, { useState } from 'react';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'patients' | 'alerts'>('overview');

  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', margin: 0, padding: 24, background: '#f8fafc', minHeight: '100vh' }}>
      <header style={{ borderBottom: '1px solid #e2e8f0', paddingBottom: 16, marginBottom: 24 }}>
        <h1 style={{ color: '#0f172a', margin: 0 }}>MINDCARE NER</h1>
        <p style={{ color: '#64748b', margin: '4px 0 0 0' }}>
          Caregiver Monitoring Portal — Cognitive Support & Memory Assistance (SIH26003)
        </p>
      </header>

      <nav style={{ display: 'flex', gap: 12, marginBottom: 24 }}>
        <button
          onClick={() => setActiveTab('overview')}
          style={{
            padding: '8px 16px',
            borderRadius: 6,
            border: 'none',
            background: activeTab === 'overview' ? '#2563eb' : '#e2e8f0',
            color: activeTab === 'overview' ? '#ffffff' : '#1e293b',
            cursor: 'pointer',
            fontWeight: 600,
          }}
        >
          Daily Overview
        </button>
        <button
          onClick={() => setActiveTab('patients')}
          style={{
            padding: '8px 16px',
            borderRadius: 6,
            border: 'none',
            background: activeTab === 'patients' ? '#2563eb' : '#e2e8f0',
            color: activeTab === 'patients' ? '#ffffff' : '#1e293b',
            cursor: 'pointer',
            fontWeight: 600,
          }}
        >
          Assigned Patients
        </button>
        <button
          onClick={() => setActiveTab('alerts')}
          style={{
            padding: '8px 16px',
            borderRadius: 6,
            border: 'none',
            background: activeTab === 'alerts' ? '#2563eb' : '#e2e8f0',
            color: activeTab === 'alerts' ? '#ffffff' : '#1e293b',
            cursor: 'pointer',
            fontWeight: 600,
          }}
        >
          Attention Alerts
        </button>
      </nav>

      <main>
        {activeTab === 'overview' && (
          <section style={{ background: '#ffffff', padding: 24, borderRadius: 8, boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <h2 style={{ color: '#1e293b' }}>Cognitive Engagement Summary</h2>
            <p style={{ color: '#475569' }}>
              Summary of daily cognitive games and memory assistance interactions across assigned devices.
            </p>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16, marginTop: 16 }}>
              <div style={{ padding: 16, background: '#f1f5f9', borderRadius: 8 }}>
                <div style={{ fontSize: 14, color: '#64748b' }}>Active Patients</div>
                <div style={{ fontSize: 24, fontWeight: 700, color: '#0f172a' }}>1</div>
              </div>
              <div style={{ padding: 16, background: '#f1f5f9', borderRadius: 8 }}>
                <div style={{ fontSize: 14, color: '#64748b' }}>Sessions Completed Today</div>
                <div style={{ fontSize: 24, fontWeight: 700, color: '#0f172a' }}>3</div>
              </div>
              <div style={{ padding: 16, background: '#f1f5f9', borderRadius: 8 }}>
                <div style={{ fontSize: 14, color: '#64748b' }}>Caregiver Attention Status</div>
                <div style={{ fontSize: 24, fontWeight: 700, color: '#16a34a' }}>Normal</div>
              </div>
            </div>
          </section>
        )}

        {activeTab === 'patients' && (
          <section style={{ background: '#ffffff', padding: 24, borderRadius: 8, boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <h2 style={{ color: '#1e293b' }}>Assigned Patient Profiles</h2>
            <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: 16 }}>
              <thead>
                <tr style={{ borderBottom: '2px solid #e2e8f0', textAlign: 'left' }}>
                  <th style={{ padding: 12 }}>Patient Code</th>
                  <th style={{ padding: 12 }}>Language</th>
                  <th style={{ padding: 12 }}>Age</th>
                  <th style={{ padding: 12 }}>Sync Status</th>
                </tr>
              </thead>
              <tbody>
                <tr style={{ borderBottom: '1px solid #f1f5f9' }}>
                  <td style={{ padding: 12, fontWeight: 600 }}>NER-PAT-001</td>
                  <td style={{ padding: 12 }}>Assamese</td>
                  <td style={{ padding: 12 }}>72</td>
                  <td style={{ padding: 12, color: '#16a34a' }}>Online / Synced</td>
                </tr>
              </tbody>
            </table>
          </section>
        )}

        {activeTab === 'alerts' && (
          <section style={{ background: '#ffffff', padding: 24, borderRadius: 8, boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <h2 style={{ color: '#1e293b' }}>Caregiver Attention Recommended</h2>
            <p style={{ color: '#475569' }}>
              Statistical anomaly flags generated by offline activity pattern shifts.
            </p>
            <div style={{ padding: 16, borderLeft: '4px solid #f59e0b', background: '#fffbeb', borderRadius: 4, marginTop: 12 }}>
              <div style={{ fontWeight: 600, color: '#92400e' }}>Unusual performance change detected</div>
              <div style={{ color: '#b45309', fontSize: 14, marginTop: 4 }}>
                Patient NER-PAT-001 exhibited higher response latency than baseline during today's afternoon Memory Match session.
              </div>
            </div>
          </section>
        )}
      </main>
    </div>
  );
};

export default App;
