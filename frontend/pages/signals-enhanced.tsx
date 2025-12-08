import dynamic from 'next/dynamic';
import { GetServerSideProps } from 'next';
import styles from '../styles/components.module.css';

// Import the component dynamically with no SSR to avoid React hooks issues
const SignalsEnhancedContent = dynamic(() => import('../components/SignalsEnhancedContent'), {
  ssr: false,
  loading: () => (
    <div className={styles.loadingContainer}>
      <h2>Loading Signals Dashboard...</h2>
    </div>
  ),
});

export default function SignalsEnhancedPage() {
  return <SignalsEnhancedContent />;
}

// Force server-side rendering for the page wrapper
export const getServerSideProps: GetServerSideProps = async () => {
  return { props: {} };
};
