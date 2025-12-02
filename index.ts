export interface CouncilSeal {
  flame: boolean;
  infinityKnot: boolean;
  scrolls: string[];
  shield: boolean;
  balanceScales: boolean;
}

export const councilSeal: CouncilSeal = {
  flame: true,
  infinityKnot: true,
  scrolls: ["memory", "commerce", "healing", "observability", "compliance", "archives"],
  shield: true,
  balanceScales: true,
};
