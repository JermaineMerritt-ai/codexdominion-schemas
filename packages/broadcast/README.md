# Broadcast Package

Multi-channel broadcast system for dispatching ceremonial capsules across email, social channels, and portals.

## Features

- **Email Broadcasting** - Send HTML email capsules to subscribers
- **Channel Integration** - Dispatch to Discord, Slack, Twitter/X, etc.
- **Ceremonial Capsules** - Structured content with banners, scripts, hymns, guides
- **Ledger Integration** - Creates sealed acts for broadcast accountability
- **Scheduling** - Support for daily, seasonal, and epochal cycles

## Usage

```typescript
import { broadcast } from '@codex-dominion/broadcast';

await broadcast.dispatchCapsule({
  targets: [
    'user@example.com',
    'another@example.com',
    'discord:announcements',
    'slack:general'
  ],
  assets: {
    welcomeBanner: 'Welcome to the New Cycle',
    replayAnnouncement: 'Review the previous epoch',
    invocationScript: 'BEGIN CYCLE\nINVOKE SYSTEMS\nSEAL ACTS',
    cycleHymn: 'Verse of the eternal flame...',
    performanceGuide: 'Step 1: Deploy\nStep 2: Monitor\nStep 3: Seal'
  },
  schedule: {
    cycle: 'daily',
    at: '09:00'
  }
});
```

## Integration Points

### Email Providers
- SendGrid
- AWS SES
- Postmark
- Mailgun

### Channel Providers
- Discord Webhooks
- Slack API
- Twitter/X API
- Telegram Bots

## Development

```bash
npm install
npm run build
npm run dev  # watch mode
```
