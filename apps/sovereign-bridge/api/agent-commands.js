const { app } = require('@azure/functions');

// AI Agent Commands API for Azure Static Web Apps
// Handles POST (create agent tasks) and GET (query task status)

app.http('agent-commands', {
    methods: ['GET', 'POST', 'OPTIONS'],
    authLevel: 'anonymous',
    handler: async (request, context) => {
        context.log('Agent Commands API invoked');

        // Handle CORS preflight
        if (request.method === 'OPTIONS') {
            return {
                status: 204,
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                }
            };
        }

        try {
            // GET: Query task status
            if (request.method === 'GET') {
                const url = new URL(request.url);
                const taskId = url.searchParams.get('taskId');

                if (!taskId) {
                    return {
                        status: 400,
                        jsonBody: {
                            success: false,
                            message: 'taskId parameter is required'
                        },
                        headers: { 'Content-Type': 'application/json' }
                    };
                }

                // Mock task status (replace with actual database query)
                return {
                    status: 200,
                    jsonBody: {
                        success: true,
                        task: {
                            taskId,
                            status: 'pending',
                            agent: 'super_action_ai',
                            createdAt: new Date().toISOString(),
                            message: 'Task status retrieved (mock data)'
                        }
                    },
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    }
                };
            }

            // POST: Create agent task
            if (request.method === 'POST') {
                const body = await request.json();
                const { agent, mode, prompt, targets, context } = body;

                // Validation
                if (!agent || !mode || !prompt) {
                    return {
                        status: 400,
                        jsonBody: {
                            success: false,
                            message: 'Missing required fields: agent, mode, prompt'
                        },
                        headers: { 'Content-Type': 'application/json' }
                    };
                }

                // Generate IDs
                const projectId = `project_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
                const taskId = `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

                // Mock task creation (replace with actual database insert)
                const taskData = {
                    projectId,
                    taskId,
                    agent,
                    mode,
                    prompt,
                    targets: targets || [],
                    context: context || {},
                    status: 'queued',
                    createdAt: new Date().toISOString()
                };

                context.log('Task created:', taskData);

                return {
                    status: 200,
                    jsonBody: {
                        success: true,
                        projectId,
                        taskId,
                        message: `Agent command created successfully for ${agent}`,
                        data: taskData
                    },
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    }
                };
            }

            // Unsupported method
            return {
                status: 405,
                jsonBody: {
                    success: false,
                    message: 'Method not allowed'
                },
                headers: { 'Content-Type': 'application/json' }
            };

        } catch (error) {
            context.log.error('Error in agent-commands API:', error);
            return {
                status: 500,
                jsonBody: {
                    success: false,
                    message: 'Internal server error',
                    error: error.message
                },
                headers: { 'Content-Type': 'application/json' }
            };
        }
    }
});
