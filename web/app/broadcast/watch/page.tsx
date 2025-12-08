import { BroadcastAudience } from '@/components/broadcast-audience';

export const metadata = {
  title: 'Council Broadcast | Codex Dominion',
  description: 'Live ceremonial broadcast for council members',
};

export default function WatchBroadcastPage() {
  return (
    <BroadcastAudience
      role="council"
      showVideo={true}
      userName="Council Member"
      wsUrl={process.env.NEXT_PUBLIC_WS_RELAY_URL || 'wss://relay.codexdominion.com'}
    />
  );
}
