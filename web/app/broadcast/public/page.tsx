import { BroadcastAudience } from '@/components/broadcast-audience';

export const metadata = {
  title: 'Public Broadcast | Codex Dominion',
  description: 'Public ceremonial broadcast view',
};

export default function PublicBroadcastPage() {
  return (
    <BroadcastAudience
      role="observer"
      showVideo={false}
      wsUrl={process.env.NEXT_PUBLIC_WS_RELAY_URL || 'wss://relay.codexdominion.com'}
    />
  );
}
