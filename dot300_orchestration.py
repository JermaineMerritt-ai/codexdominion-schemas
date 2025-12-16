"""
DOT300 AI Orchestration System with GPT-4 Integration
Connects 301 specialized agents with OpenAI GPT-4 for intelligent task routing
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# OpenAI Client (uses OPENAI_API_KEY environment variable)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Load agents
def load_agents():
    with open("dot300_agents.json", "r") as f:
        return json.load(f)

# Agent Router - Uses GPT-4 to determine best agent for task
class AgentRouter:
    def __init__(self):
        self.agents_data = load_agents()
        self.agents = self.agents_data["agents"]

    def find_best_agent(self, task_description: str, industry: Optional[str] = None) -> Dict:
        """Use GPT-4 to analyze task and select best agent"""

        # Filter agents by industry if specified
        candidates = self.agents if not industry else [
            a for a in self.agents if a["industry"] == industry
        ]

        # Create agent summary for GPT-4
        agent_summary = "\n".join([
            f"- {a['id']}: {a['name']} - {a['specialization']} (Score: {a['performance_score']:.3f})"
            for a in candidates[:50]  # Limit to top 50 for token efficiency
        ])

        # GPT-4 prompt
        prompt = f"""You are an AI agent router. Analyze the task and select the best agent.

Task: {task_description}

Available Agents:
{agent_summary}

Return only the agent_id of the best match. Consider:
1. Specialization match
2. Performance score
3. Relevant capabilities

Response format: agent_XXXX"""

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert AI agent router."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=50
            )

            agent_id = response.choices[0].message.content.strip()

            # Find the agent
            agent = next((a for a in self.agents if a["id"] == agent_id), None)
            if not agent:
                # Fallback to highest scoring agent
                agent = max(candidates, key=lambda a: a["performance_score"])

            return agent

        except Exception as e:
            print(f"GPT-4 routing error: {e}")
            # Fallback: return highest performing agent
            return max(candidates, key=lambda a: a["performance_score"])

    def execute_task_with_gpt4(self, agent: Dict, task_description: str) -> Dict:
        """Execute task using GPT-4 with agent context"""

        # Build agent context for GPT-4
        context = f"""You are {agent['name']}, a specialized AI agent.

Specialization: {agent['specialization']}
Industry: {agent['industry']}
Performance Score: {agent['performance_score']:.3f}
Success Rate: {agent['success_rate']:.1%}
Tasks Completed: {agent['tasks_completed']}

Capabilities:
{self._format_capabilities(agent['capabilities'])}

Execute this task with your expertise:
{task_description}"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": task_description}
                ],
                temperature=0.7,
                max_tokens=2000
            )

            result = response.choices[0].message.content

            return {
                "agent_id": agent["id"],
                "agent_name": agent["name"],
                "task": task_description,
                "result": result,
                "status": "completed",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "model": "gpt-4o-mini"
            }

        except Exception as e:
            return {
                "agent_id": agent["id"],
                "agent_name": agent["name"],
                "task": task_description,
                "error": str(e),
                "status": "failed",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }

    def _format_capabilities(self, capabilities: List[Dict]) -> str:
        return "\n".join([
            f"- {cap['name']}: Skill {cap['skill_level']:.2f}, {cap['experience_points']} XP"
            for cap in capabilities
        ])

# Task Queue Manager
class TaskQueue:
    def __init__(self):
        self.queue = []
        self.completed = []

    def add_task(self, task: Dict) -> str:
        task_id = f"task_{len(self.queue) + len(self.completed) + 1:04d}"
        task["id"] = task_id
        task["status"] = "queued"
        task["queued_at"] = datetime.utcnow().isoformat() + "Z"
        self.queue.append(task)
        return task_id

    def get_next_task(self) -> Optional[Dict]:
        if self.queue:
            task = self.queue.pop(0)
            task["status"] = "processing"
            task["started_at"] = datetime.utcnow().isoformat() + "Z"
            return task
        return None

    def complete_task(self, task_id: str, result: Dict):
        for task in self.queue:
            if task["id"] == task_id:
                task["status"] = "completed"
                task["completed_at"] = datetime.utcnow().isoformat() + "Z"
                task["result"] = result
                self.completed.append(task)
                self.queue.remove(task)
                break

# Initialize
router = AgentRouter()
task_queue = TaskQueue()

# API Routes
@app.route("/")
def index():
    return jsonify({
        "service": "DOT300 AI Orchestration",
        "status": "operational",
        "gpt4_enabled": bool(OPENAI_API_KEY and OPENAI_API_KEY != ""),
        "endpoints": {
            "route": "/route - Find best agent for task",
            "execute": "/execute - Execute task with GPT-4",
            "queue": "/queue - Add task to queue",
            "status": "/status/<task_id> - Check task status"
        }
    })

@app.route("/route", methods=["POST"])
def route_task():
    """Find best agent for a task using GPT-4"""
    data = request.json
    task = data.get("task")
    industry = data.get("industry")

    if not task:
        return jsonify({"error": "Task description required"}), 400

    agent = router.find_best_agent(task, industry)

    return jsonify({
        "task": task,
        "recommended_agent": {
            "id": agent["id"],
            "name": agent["name"],
            "specialization": agent["specialization"],
            "industry": agent["industry"],
            "performance_score": agent["performance_score"],
            "success_rate": agent["success_rate"]
        }
    })

@app.route("/execute", methods=["POST"])
def execute_task():
    """Execute task with GPT-4"""
    data = request.json
    task = data.get("task")
    agent_id = data.get("agent_id")
    industry = data.get("industry")

    if not task:
        return jsonify({"error": "Task description required"}), 400

    # Find agent
    if agent_id:
        agent = next((a for a in router.agents if a["id"] == agent_id), None)
        if not agent:
            return jsonify({"error": "Agent not found"}), 404
    else:
        agent = router.find_best_agent(task, industry)

    # Execute with GPT-4
    result = router.execute_task_with_gpt4(agent, task)

    return jsonify(result)

@app.route("/queue", methods=["POST"])
def queue_task():
    """Add task to queue for async processing"""
    data = request.json
    task = data.get("task")

    if not task:
        return jsonify({"error": "Task description required"}), 400

    task_id = task_queue.add_task(data)

    return jsonify({
        "task_id": task_id,
        "status": "queued",
        "message": "Task added to queue"
    })

@app.route("/status/<task_id>", methods=["GET"])
def get_task_status(task_id):
    """Check task status"""
    # Check queue
    task = next((t for t in task_queue.queue if t["id"] == task_id), None)
    if task:
        return jsonify(task)

    # Check completed
    task = next((t for t in task_queue.completed if t["id"] == task_id), None)
    if task:
        return jsonify(task)

    return jsonify({"error": "Task not found"}), 404

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "DOT300 Orchestration",
        "gpt4_enabled": bool(OPENAI_API_KEY and OPENAI_API_KEY != ""),
        "agents_loaded": len(router.agents),
        "queue_size": len(task_queue.queue),
        "completed_tasks": len(task_queue.completed)
    })

if __name__ == "__main__":
    print("DOT300 AI Orchestration Server Starting...")
    print(f"Loaded {len(router.agents)} agents")
    print(f"GPT-4 Enabled: {bool(OPENAI_API_KEY and OPENAI_API_KEY != '')}")
    print(f"Server: http://localhost:8400")
    print("Press Ctrl+C to stop")

    # Use Flask development server for now
    app.run(host="0.0.0.0", port=8400, debug=False)
