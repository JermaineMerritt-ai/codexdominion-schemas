/**
 * 🔥 CODEX DOMINION - WEBSOCKET CLIENT 🔥
 * ==========================================
 * Client-side WebSocket manager for real-time workflow updates.
 * 
 * Features:
 * - Auto-reconnection with exponential backoff
 * - Event subscription management
 * - Progress tracking and visualization
 * - Error handling and notifications
 * 
 * Usage:
 *   const ws = new CodexWebSocketClient('http://localhost:5000');
 *   
 *   ws.on('workflow_progress', (data) => {
 *     console.log(`Progress: ${data.progress_percentage}%`);
 *     updateProgressBar(data.progress_percentage);
 *   });
 *   
 *   ws.joinProject('pic_project_123');
 *   ws.connect();
 */

class CodexWebSocketClient {
    constructor(serverUrl = 'http://localhost:5000', options = {}) {
        this.serverUrl = serverUrl;
        this.socket = null;
        this.connected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = options.maxReconnectAttempts || 5;
        this.reconnectDelay = options.reconnectDelay || 1000;
        this.eventHandlers = {};
        this.currentProject = null;
        this.currentWorkflow = null;
        
        // Load Socket.IO client library dynamically if not already loaded
        if (typeof io === 'undefined') {
            console.error('Socket.IO client library not found. Please include: <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>');
        }
    }
    
    /**
     * Connect to WebSocket server
     */
    connect() {
        if (typeof io === 'undefined') {
            console.error('Socket.IO library not loaded');
            return;
        }
        
        console.log('🔥 Connecting to Codex Dominion WebSocket...');
        
        this.socket = io(this.serverUrl, {
            transports: ['websocket', 'polling'],
            reconnection: true,
            reconnectionDelay: this.reconnectDelay,
            reconnectionAttempts: this.maxReconnectAttempts
        });
        
        // Connection events
        this.socket.on('connect', () => {
            console.log('✅ Connected to Codex Dominion WebSocket');
            this.connected = true;
            this.reconnectAttempts = 0;
            this._trigger('connected', { timestamp: new Date().toISOString() });
            
            // Rejoin rooms if reconnecting
            if (this.currentProject) {
                this.joinProject(this.currentProject);
            }
            if (this.currentWorkflow) {
                this.joinWorkflow(this.currentWorkflow);
            }
        });
        
        this.socket.on('disconnect', () => {
            console.log('🔌 Disconnected from WebSocket');
            this.connected = false;
            this._trigger('disconnected', { timestamp: new Date().toISOString() });
        });
        
        this.socket.on('connect_error', (error) => {
            console.error('❌ Connection error:', error);
            this.reconnectAttempts++;
            this._trigger('connection_error', { error: error.message, attempts: this.reconnectAttempts });
        });
        
        // Server events
        this.socket.on('connection_status', (data) => {
            console.log('📡 Connection status:', data.message);
            this._trigger('connection_status', data);
        });
        
        // Workflow events
        this.socket.on('workflow_started', (data) => {
            console.log(`🚀 Workflow started: ${data.workflow_id}`);
            this._trigger('workflow_started', data);
        });
        
        this.socket.on('workflow_progress', (data) => {
            console.log(`📊 Workflow progress: ${data.step_name} - ${data.progress_percentage}%`);
            this._trigger('workflow_progress', data);
        });
        
        this.socket.on('workflow_complete', (data) => {
            const emoji = data.status === 'complete' ? '✅' : '❌';
            console.log(`${emoji} Workflow ${data.status}: ${data.workflow_id}`);
            this._trigger('workflow_complete', data);
        });
        
        this.socket.on('workflow_error', (data) => {
            console.error(`❌ Workflow error: ${data.error_message}`);
            this._trigger('workflow_error', data);
        });
        
        // Rendering events
        this.socket.on('rendering_progress', (data) => {
            console.log(`🎨 Rendering: ${data.asset_name} - ${data.progress_percentage}%`);
            this._trigger('rendering_progress', data);
        });
        
        // Asset events
        this.socket.on('asset_created', (data) => {
            console.log(`📦 Asset created: ${data.asset_name} (${data.asset_type})`);
            this._trigger('asset_created', data);
        });
        
        // Module events
        this.socket.on('module_update', (data) => {
            console.log(`🔧 Module update: ${data.module_name} - ${data.status}`);
            this._trigger('module_update', data);
        });
        
        // System events
        this.socket.on('system_notification', (data) => {
            console.log(`📢 ${data.title}: ${data.message}`);
            this._trigger('system_notification', data);
        });
        
        // Room events
        this.socket.on('joined_room', (data) => {
            console.log(`📡 Joined room: ${data.room}`);
            this._trigger('joined_room', data);
        });
        
        this.socket.on('left_room', (data) => {
            console.log(`📡 Left room: ${data.room}`);
            this._trigger('left_room', data);
        });
        
        // Ping/pong for keep-alive
        this.socket.on('pong', (data) => {
            this._trigger('pong', data);
        });
    }
    
    /**
     * Disconnect from WebSocket server
     */
    disconnect() {
        if (this.socket) {
            console.log('🔌 Disconnecting from WebSocket...');
            this.socket.disconnect();
            this.connected = false;
        }
    }
    
    /**
     * Join a project room for updates
     */
    joinProject(projectId) {
        if (!this.socket || !this.connected) {
            console.error('❌ Not connected to WebSocket');
            return;
        }
        
        this.currentProject = projectId;
        this.socket.emit('join_project', { project_id: projectId });
    }
    
    /**
     * Leave a project room
     */
    leaveProject(projectId) {
        if (!this.socket || !this.connected) return;
        
        this.socket.emit('leave_project', { project_id: projectId });
        if (this.currentProject === projectId) {
            this.currentProject = null;
        }
    }
    
    /**
     * Join a workflow room for execution updates
     */
    joinWorkflow(workflowId) {
        if (!this.socket || !this.connected) {
            console.error('❌ Not connected to WebSocket');
            return;
        }
        
        this.currentWorkflow = workflowId;
        this.socket.emit('join_workflow', { workflow_id: workflowId });
    }
    
    /**
     * Send ping to server (keep-alive)
     */
    ping() {
        if (!this.socket || !this.connected) return;
        this.socket.emit('ping');
    }
    
    /**
     * Register event handler
     */
    on(eventName, handler) {
        if (!this.eventHandlers[eventName]) {
            this.eventHandlers[eventName] = [];
        }
        this.eventHandlers[eventName].push(handler);
    }
    
    /**
     * Remove event handler
     */
    off(eventName, handler) {
        if (!this.eventHandlers[eventName]) return;
        
        if (handler) {
            this.eventHandlers[eventName] = this.eventHandlers[eventName].filter(h => h !== handler);
        } else {
            this.eventHandlers[eventName] = [];
        }
    }
    
    /**
     * Trigger event handlers
     */
    _trigger(eventName, data) {
        const handlers = this.eventHandlers[eventName] || [];
        handlers.forEach(handler => {
            try {
                handler(data);
            } catch (error) {
                console.error(`Error in ${eventName} handler:`, error);
            }
        });
    }
    
    /**
     * Check if connected
     */
    isConnected() {
        return this.connected;
    }
    
    /**
     * Get current project ID
     */
    getCurrentProject() {
        return this.currentProject;
    }
    
    /**
     * Get current workflow ID
     */
    getCurrentWorkflow() {
        return this.currentWorkflow;
    }
}

// ============================================================================
// UI HELPER FUNCTIONS
// ============================================================================

/**
 * Create a progress bar element
 */
function createProgressBar(containerId, options = {}) {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`Container ${containerId} not found`);
        return null;
    }
    
    const progressBar = document.createElement('div');
    progressBar.className = 'codex-progress-bar';
    progressBar.innerHTML = `
        <div class="progress-label">${options.label || 'Workflow Progress'}</div>
        <div class="progress-container">
            <div class="progress-fill" style="width: 0%"></div>
            <div class="progress-text">0%</div>
        </div>
        <div class="progress-status">${options.status || 'Initializing...'}</div>
    `;
    
    container.appendChild(progressBar);
    
    return {
        element: progressBar,
        update: (percentage, status) => {
            const fill = progressBar.querySelector('.progress-fill');
            const text = progressBar.querySelector('.progress-text');
            const statusEl = progressBar.querySelector('.progress-status');
            
            fill.style.width = `${percentage}%`;
            text.textContent = `${Math.round(percentage)}%`;
            if (status) {
                statusEl.textContent = status;
            }
        },
        remove: () => {
            progressBar.remove();
        }
    };
}

/**
 * Create step indicator
 */
function createStepIndicator(containerId, steps) {
    const container = document.getElementById(containerId);
    if (!container) return null;
    
    const indicator = document.createElement('div');
    indicator.className = 'codex-step-indicator';
    
    steps.forEach((step, index) => {
        const stepEl = document.createElement('div');
        stepEl.className = 'step';
        stepEl.dataset.step = step;
        stepEl.innerHTML = `
            <div class="step-number">${index + 1}</div>
            <div class="step-name">${step}</div>
            <div class="step-status">⏳</div>
        `;
        indicator.appendChild(stepEl);
    });
    
    container.appendChild(indicator);
    
    return {
        element: indicator,
        updateStep: (stepName, status) => {
            const stepEl = indicator.querySelector(`[data-step="${stepName}"]`);
            if (!stepEl) return;
            
            const statusEl = stepEl.querySelector('.step-status');
            const statusMap = {
                'running': '▶️',
                'complete': '✅',
                'error': '❌',
                'pending': '⏳'
            };
            
            statusEl.textContent = statusMap[status] || '⏳';
            stepEl.classList.add(`status-${status}`);
        },
        remove: () => {
            indicator.remove();
        }
    };
}

// Export for use in browser or module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CodexWebSocketClient, createProgressBar, createStepIndicator };
}
