const { app } = require('@azure/functions');

// AI Agent Commands API for Azure Static Web Apps
// Handles POST (create agent tasks) and GET (query task status)

app.http('agent-commands', {
    methods: ['GET', 'POST', 'OPTIONS'],
    authLevel: 'anonymous',
    route: 'agent-commands',
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
                        headers: {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*'
                        }
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
                            updatedAt: new Date().toISOString(),
                            progress: 0
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

                // Validate required fields
                if (!body.agent || !body.mode || !body.prompt) {
                    return {
                        status: 400,
                        jsonBody: {
                            success: false,
                            message: 'Required fields: agent, mode, prompt'
                        },
                        headers: {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*'
                        }
                    };
                }

                // Generate IDs
                const projectId = `proj_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
                const taskId = `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

                // Create task response
                const taskResponse = {
                    success: true,
                    message: 'Agent task created successfully',
                    data: {
                        projectId,
                        taskId,
                        agent: body.agent,
                        mode: body.mode,
                        prompt: body.prompt,
                        targets: body.targets || [],
                        context: body.context || {},
                        status: 'pending',
                        createdAt: new Date().toISOString()
                    }
                };

                context.log('Created task:', taskId);

                return {
                    status: 201,
                    jsonBody: taskResponse,
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    }
                };
            }

        } catch (error) {
            context.error('Error processing request:', error);
            return {
                status: 500,
                jsonBody: {
                    success: false,
                    message: 'Internal server error',
                    error: error.message
                },
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            };
        }

        // Method not allowed
        return {
            status: 405,
            jsonBody: {
                success: false,
                message: 'Method not allowed'
            },
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        };
    }
});
