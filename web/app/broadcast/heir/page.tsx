import { BroadcastAudience } from '@/components/broadcast-audience';

export const metadata = {
  title: 'Heir Broadcast | Codex Dominion',
  description: 'Live ceremonial broadcast for heirs',
};

export default function HeirBroadcastPage() {
  return (
    <BroadcastAudience
      role="heir"
      showVideo={false}
      userName="Heir"
      wsUrl={process.env.NEXT_PUBLIC_WS_RELAY_URL || 'wss://relay.codexdominion.com'}
    />
  );
}
