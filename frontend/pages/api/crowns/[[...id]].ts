/**
 * 👑 CROWNS API ENDPOINT
 * Manages Crowns (Products/Bundles)
 */

import type { NextApiRequest, NextApiResponse } from 'next';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { method } = req;
  const { id } = req.query;

  try {
    switch (method) {
      case 'GET':
        if (id) {
          return await getCrown(id as string, res);
        } else {
          return await listCrowns(res);
        }

      case 'POST':
        return await forgeCrown(req, res);

      case 'PUT':
        return await updateCrown(id as string, req, res);

      case 'DELETE':
        return await deleteCrown(id as string, res);

      default:
        res.setHeader('Allow', ['GET', 'POST', 'PUT', 'DELETE']);
        return res.status(405).json({ error: `Method ${method} Not Allowed` });
    }
  } catch (error) {
    console.error('Crowns API Error:', error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}

async function listCrowns(res: NextApiResponse) {
  // Call Python orchestrator
  const { stdout } = await execAsync(
    'python -c "from codex_sovereign_orchestrator import CodexSovereignOrchestrator; import json; o = CodexSovereignOrchestrator(); print(json.dumps(o.list_crowns()))"'
  );

  const crowns = JSON.parse(stdout);
  return res.status(200).json(crowns);
}

async function getCrown(id: string, res: NextApiResponse) {
  const { stdout } = await execAsync(
    `python -c "from codex_sovereign_orchestrator import CodexSovereignOrchestrator; import json; o = CodexSovereignOrchestrator(); crowns = o.list_crowns(); crown = next((c for c in crowns if c['id'] == '${id}'), None); print(json.dumps(crown))"`
  );

  const crown = JSON.parse(stdout);

  if (!crown) {
    return res.status(404).json({ error: 'Crown not found' });
  }

  return res.status(200).json(crown);
}

async function forgeCrown(req: NextApiRequest, res: NextApiResponse) {
  const { name, type, price, description, features } = req.body;

  if (!name || !type || !price || !description) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  const pythonCommand = `
from codex_sovereign_orchestrator import CodexSovereignOrchestrator, CrownType
import json
o = CodexSovereignOrchestrator()
crown = o.forge_crown(
    name="${name}",
    crown_type=CrownType.${type.toUpperCase()},
    price=${price},
    description="${description}",
    features=${JSON.stringify(features)}
)
print(json.dumps(crown.to_dict()))
  `.trim();

  const { stdout } = await execAsync(`python -c "${pythonCommand}"`);
  const crown = JSON.parse(stdout);

  return res.status(201).json(crown);
}

async function updateCrown(id: string, req: NextApiRequest, res: NextApiResponse) {
  // Simplified: In production, implement proper update logic
  return res.status(200).json({ message: 'Crown updated', id });
}

async function deleteCrown(id: string, res: NextApiResponse) {
  // Simplified: In production, implement proper delete logic
  return res.status(200).json({ message: 'Crown deleted', id });
}
