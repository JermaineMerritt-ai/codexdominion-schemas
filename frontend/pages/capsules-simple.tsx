// pages/capsules-simple.tsx
import dynamic from 'next/dynamic';
import styles from './capsules-simple.module.css';
const Capsules = dynamic(() => import('../components/CapsulesSimple'), {
  ssr: false,
});
export default Capsules;
