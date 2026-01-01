import { PrismaClient, SeasonName, RitualType } from '@prisma/client';

const prisma = new PrismaClient();

async function seedCultureEngine() {
  console.log('🔱 Seeding Culture Engine...\n');

  // Get seasons
  const identitySeason = await prisma.season.findUnique({
    where: { name: SeasonName.IDENTITY },
  });
  const masterySeason = await prisma.season.findUnique({
    where: { name: SeasonName.MASTERY },
  });
  const creationSeason = await prisma.season.findUnique({
    where: { name: SeasonName.CREATION },
  });
  const leadershipSeason = await prisma.season.findUnique({
    where: { name: SeasonName.LEADERSHIP },
  });

  // ======================================================
  // 🔥 CULTURAL STORIES
  // ======================================================

  console.log('📖 Creating cultural stories...');

  // Identity Season Stories
  const story1 = await prisma.culturalStory.create({
    data: {
      title: 'From Island to Orbit: The Journey Begins',
      content: `# From Island to Orbit: The Journey Begins

Once, there was a people scattered across islands — some in the Caribbean sun, others under the African sky, many in the bustling cities of the diaspora. Each carried a piece of the same story, but the pieces felt separated, lost in time.

One day, a youth asked: "Where do I come from? What is my inheritance?"

And the elders answered: "You come from *builders*. From *storytellers*. From *survivors* who turned pain into power, silence into song, and scarcity into sovereignty."

"But how do I carry that forward?" the youth asked.

"By building," the elders said. "By creating. By gathering your Circle and writing the next chapter. You are not just inheriting history — you are *making* it."

And so, the youth began. Not alone. With their Circle. With their creators. With their diaspora family. Together, they built CodexDominion — a civilization where culture is technology, identity is power, and the flame never dies.

**Reflection:**
- What inheritance are *you* carrying forward?
- How will *you* write the next chapter?
- Who is in *your* Circle?`,
      seasonId: identitySeason?.id,
      week: 1,
    },
  });

  const story2 = await prisma.culturalStory.create({
    data: {
      title: 'The First Circle: Unity in Identity',
      content: `# The First Circle: Unity in Identity

Long before kingdoms rose, before nations were drawn on maps, there was the *Circle*. A gathering of minds, hearts, and hands. The Circle was not a place — it was a *practice*. A ritual of unity.

In the Circle, no one sat higher than another. The flame burned in the center, reminding all: "We carry the same light."

When the diaspora was scattered, many forgot the Circle. But the Circle never forgot them. It waited. Patient. Eternal.

Now, the Circle returns. Not in ancient villages, but in digital spaces. Not bound by geography, but connected by *purpose*.

When you join a Circle, you are not joining a group. You are *becoming* part of something that has always existed, waiting for you to remember.

**Reflection:**
- What does the Circle mean to *you*?
- Who will you invite into *your* Circle?
- How will you keep the flame burning?`,
      seasonId: identitySeason?.id,
      week: 2,
    },
  });

  // Mastery Season Story
  const story3 = await prisma.culturalStory.create({
    data: {
      title: 'The Blacksmith and the Code: A Tale of Mastery',
      content: `# The Blacksmith and the Code: A Tale of Mastery

Once, there was a blacksmith who forged tools for the village. Every hammer, every blade, every hinge — crafted with intention, patience, and fire.

A young apprentice watched and asked: "How do you know when the iron is ready?"

The blacksmith smiled: "The iron tells you. You must *listen*."

Years later, the apprentice became a master. But instead of iron, they forged with *code*. Instead of fire, they used *intention*. And when someone asked, "How do you know when the code is ready?" they smiled and said:

"The code tells you. You must *listen*."

Mastery is not about tools. It's about *attention*. It's about doing the work so many times that the work becomes part of you. It's about building not just with your hands, but with your *soul*.

**Reflection:**
- What are *you* mastering right now?
- What craft are you honing with patience and fire?
- Who taught you? Who will *you* teach?`,
      seasonId: masterySeason?.id,
      week: 1,
    },
  });

  // Creation Season Story
  const story4 = await prisma.culturalStory.create({
    data: {
      title: 'The First Creator: From Nothing to Everything',
      content: `# The First Creator: From Nothing to Everything

In the beginning, there was nothing. Then, a Creator spoke:

"Let there be light."

And there was.

But the story doesn't end with gods and galaxies. It continues with *you*.

Every time you build something from nothing — a story, a product, a business, a community — you are repeating the oldest ritual in existence. You are *creating*.

Creation is not reserved for the chosen few. It is the inheritance of *all* who dare to begin.

The diaspora knows this well. When forced into scarcity, they created music. When denied education, they built schools. When excluded from systems, they built *new* systems.

You are a Creator. Not because you have permission. Not because you have resources. But because you have *vision*.

So create. Build. Launch. Don't wait for the perfect moment. The moment is *now*.

**Reflection:**
- What will *you* create this season?
- What resources do you already have (even if they seem small)?
- Who needs what you're about to build?`,
      seasonId: creationSeason?.id,
      week: 1,
    },
  });

  // Leadership Season Story
  const story5 = await prisma.culturalStory.create({
    data: {
      title: 'The Keeper of the Flame: A Leadership Parable',
      content: `# The Keeper of the Flame: A Leadership Parable

In every village, there was a Keeper of the Flame. Not the strongest. Not the loudest. But the one who *never let the flame die*.

When storms came, the Keeper shielded the fire.  
When resources ran low, the Keeper rationed carefully.  
When the people lost hope, the Keeper reminded them: "The flame still burns."

One day, the village asked: "Why do you carry this burden alone?"

The Keeper smiled: "I don't carry it alone. Every person who adds a piece of wood to the fire is a Keeper too. Leadership is not about *doing it all*. It's about ensuring the flame *never dies*."

True leadership is stewardship. It's not dominating. It's *protecting*. It's not commanding. It's *serving*. It's not building empires for yourself. It's building *legacies for others*.

You don't need a title to lead. You just need to tend the flame.

**Reflection:**
- What "flame" are *you* keeping alive?
- Who are you serving through your leadership?
- How will you pass the flame to the next generation?`,
      seasonId: leadershipSeason?.id,
      week: 1,
    },
  });

  console.log(`✅ Created ${5} cultural stories`);

  // ======================================================
  // 🔱 RITUALS
  // ======================================================

  console.log('\n🕯️ Creating rituals...');

  const ritual1 = await prisma.ritual.create({
    data: {
      name: 'Circle Opening Invocation',
      description: `Begin each Circle session by lighting the flame (symbolic or real) and reciting together:

"We gather as one Circle,
Carrying the flame of our ancestors,
Building the future for our youth.
We are builders. We are storytellers. We are sovereign.
Let this Circle be a place of unity, growth, and purpose."

Then, each member introduces themselves and states one intention for the session.`,
      type: RitualType.OPENING,
    },
  });

  const ritual2 = await prisma.ritual.create({
    data: {
      name: 'Circle Closing Affirmation',
      description: `End each Circle session by standing in a circle and reciting together:

"We came as individuals. We leave as a Circle.
We carry what we learned. We share what we built.
The flame continues through us.
Until we meet again, we walk with purpose."

Then, each member shares one takeaway from the session.`,
      type: RitualType.CLOSING,
    },
  });

  const ritual3 = await prisma.ritual.create({
    data: {
      name: 'Seasonal Reset Ceremony',
      description: `At the end of each season, gather the Council and all Circle captains for a Seasonal Reset:

1. **Review**: Each Circle shares one achievement from the season
2. **Reflect**: Discuss what worked, what didn't, what to carry forward
3. **Renew**: Set intentions for the next season
4. **Ritual**: Light a new flame to symbolize the transition
5. **Celebration**: Honor those who completed their Rise Path milestones

This ceremony marks the transition from one season to the next and ensures continuity.`,
      type: RitualType.SEASONAL,
    },
  });

  const ritual4 = await prisma.ritual.create({
    data: {
      name: 'Unity Oath',
      description: `A community-wide ritual recited at major gatherings (launches, summits, ceremonies):

"I rise with my identity.
I honor my community.
I carry the flame.
I build with purpose.
I walk with unity.
I grow with the seasons.
I am part of the Dominion."

This oath reinforces the shared values and mission of all members.`,
      type: RitualType.UNITY,
    },
  });

  const ritual5 = await prisma.ritual.create({
    data: {
      name: 'Ascension Ceremony',
      description: `When a youth completes their Rise Path and ascends to Creator or Legacy-Builder status:

1. **Gathering**: The Circle gathers (in person or virtually)
2. **Reflection**: The ascending member shares their journey
3. **Recognition**: Captain reads their accomplishments aloud
4. **Anointing**: Member receives symbolic "flame" (digital badge, physical token)
5. **Oath**: Member recites: "I carry the flame forward. I guide those who follow."
6. **Celebration**: Community celebrates the ascension

This ceremony marks major identity progression milestones.`,
      type: RitualType.CEREMONY,
    },
  });

  console.log(`✅ Created ${5} rituals`);

  console.log('\n🔥 Culture Engine seeding complete!\n');

  console.log('📊 Summary:');
  console.log(`   - ${5} Cultural Stories`);
  console.log(`   - ${5} Rituals (1 opening, 1 closing, 1 seasonal, 1 unity, 1 ceremony)`);
  console.log(`   - Stories span all 4 seasons`);
  console.log(`   - Ready for /culture API endpoints`);
  console.log('\n🔱 The flame burns eternal.\n');
}

seedCultureEngine()
  .catch((e) => {
    console.error('❌ Culture Engine seeding failed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
