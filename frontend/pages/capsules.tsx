// pages/capsules.tsx
import React from 'react';
import styles from './capsules.module.css';


interface Capsule {
  slug: string;
  title: string;
  kind: string;
  mode: string;
  version: string;
  status: string;
  entrypoint: string;
  schedule?: string;
  created_at: string;
  updated_at: string;
}

interface CapsuleRun {
  id: number;
  capsule_slug: string;
  actor: string;
  status: string;
  started_at: string;
  artifact_uri?: string;
  checksum?: string;
}

interface CapsulesProps {
  capsules: Capsule[];
  runs: CapsuleRun[];
  error?: string;
}

export default function Capsules({ capsules = [], runs = [], error }: CapsulesProps) {
  const formatDateTime = (dateStr: string) => {
    return new Date(dateStr).toLocaleString();
  };

  const getModeClass = (mode: string) => {
    switch (mode) {
      case 'automated':
        return styles.modeAutomated;
      case 'custodian':
        return styles.modeCustodian;
      case 'manual':
        return styles.modeManual;
      default:
        return styles.modeManual;
    }
  };

  const getStatusClass = (status: string) => {
    switch (status) {
      case 'success':
        return styles.statusSuccess;
      case 'error':
        return styles.statusError;
      case 'running':
        return styles.statusRunning;
      default:
        return styles.statusDefault;
    }
  };

  if (error) {
    return (
      <div className={styles.container}>
        <h1>Codex Capsules</h1>
        <div className={styles.error}>
          <strong>Error:</strong> {error}
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>🏛️ Codex Capsules Registry</h1>
        <p className={styles.subtitle}>
          Operational sovereignty tracking for ceremonial and technical operations
        </p>
      </div>
      {/* Capsules Section */}
      <section className={styles.section}>
        <h2 className={styles.sectionTitle}>📦 Registered Capsules ({capsules.length})</h2>
        {capsules.length === 0 ? (
          <p className={styles.italic}>No capsules registered yet.</p>
        ) : (
          <div className={styles.grid}>
            {capsules.map((c) => (
              <div key={c.slug} className={styles.capsuleCard}>
                <div className={styles.capsuleHeader}>
                  <h3 className={styles.capsuleTitle}>{c.title}</h3>
                  <span
                    className={
                      c.status === 'active'
                        ? styles.capsuleStatusActive
                        : styles.capsuleStatusInactive
                    }
                  >
                    {c.status.toUpperCase()}
                  </span>
                </div>
                <div className={styles.capsuleGrid}>
                  <div>
                    <strong>Slug:</strong> <code className={styles.capsuleSlug}>{c.slug}</code>
                  </div>
                  <div>
                    <strong>Kind:</strong> {c.kind}
                  </div>
                  <div>
                    <strong>Mode:</strong>
                    <span className={`${styles.capsuleMode} ${getModeClass(c.mode)}`}>
                      {c.mode}
                    </span>
                  </div>
                  <div>
                    <strong>Version:</strong> {c.version}
                  </div>
                  <div>
                    <strong>Schedule:</strong> {c.schedule || '—'}
                  </div>
                </div>
                {c.entrypoint && (
                  <div className={styles.capsuleEntrypoint}>
                    <strong>Entrypoint:</strong>
                    <code className={styles.capsuleEntrypointCode}>{c.entrypoint}</code>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </section>
      {/* Recent Runs Section */}
      <section>
        <h2 className={styles.sectionTitle}>🚀 Recent Execution Runs ({runs.length})</h2>
        {runs.length === 0 ? (
          <p className={styles.italic}>No execution runs recorded yet.</p>
        ) : (
          <div className={styles.runGrid}>
            {runs.slice(0, 20).map((r, i) => (
              <div key={i} className={styles.runCard}>
                <div className={styles.runHeader}>
                  <div>
                    <strong>{r.capsule_slug}</strong> executed by <em>{r.actor}</em>
                  </div>
                  <div className={styles.flexRow}>
                    <span className={`${styles.runStatus} ${getStatusClass(r.status)}`}>●</span>
                    <span className={styles.runDate}>{formatDateTime(r.started_at)}</span>
                  </div>
                </div>
                {r.artifact_uri && (
                  <div className={styles.runArtifact}>
                    📦 Artifact:
                    <a
                      href={r.artifact_uri}
                      className={styles.runArtifactLink}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      {r.artifact_uri.split('/').pop()}
                    </a>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
