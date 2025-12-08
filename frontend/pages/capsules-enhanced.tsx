import React, { useEffect, useState } from 'react';
import { GetServerSideProps } from 'next';
import Link from 'next/link';
import styles from '../styles/components.module.css';

interface Capsule {
  slug: string;
  name: string;
  description: string;
  schedule: string;
  archive_type: string;
}

export default function CapsulesWithLinks() {
  const [capsules, setCapsules] = useState<Capsule[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadCapsules() {
      try {
        setLoading(true);
        // Try local API first, fallback to external service
        const response = await fetch('/api/capsules');

        if (!response.ok) {
          throw new Error('Local API unavailable');
        }

        const data = await response.json();
        setCapsules(data.capsules || []);
      } catch (localError) {
        console.log('Local API unavailable, trying external service...');
        try {
          const externalResponse = await fetch('http://localhost:8080/api/capsules');
          const externalData = await externalResponse.json();

          // Map external data to our format
          const mappedCapsules = externalData.map((c: any) => ({
            slug: c.slug,
            name: c.title || c.slug,
            description: `External capsule: ${c.kind} mode ${c.mode}`,
            schedule: c.schedule || 'Not scheduled',
            archive_type: 'external',
          }));

          setCapsules(mappedCapsules);
        } catch (externalError) {
          console.error('Both APIs failed:', { localError, externalError });
          setError('Unable to load capsules from any source');
        }
      } finally {
        setLoading(false);
      }
    }

    loadCapsules();
  }, []);

  if (loading) {
    return (
      <div className={styles.loadingContainerFlex}>
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading capsules...</p>
        </div>
        <style jsx>{`
          .loading-container {
            display: flex;
            flex-direction: column;
            align-items: center;
          }
        `}</style>
      </div>
    );
  }
  // ...existing code for rendering capsules and error handling...
}

// Force server-side rendering to avoid static generation with React hooks
export const getServerSideProps: GetServerSideProps = async () => {
  return { props: {} };
};
