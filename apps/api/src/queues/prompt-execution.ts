import { rebuildWebsite, rebuildStore, rebuildSocialChannels } from '@codex/workflow/rebuilders';

export async function handlePromptExecution(job: { promptId: string }) {
  // Lookup prompt intent; in real use, parse body for targets
  await rebuildWebsite('main', 'parchment');
  await rebuildStore('store-alpha');
  await rebuildSocialChannels(['instagram:codex','youtube:codex'], { banner: 'Welcome' });
}
