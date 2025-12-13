const express = require('express');
const mysql = require('mysql');

const app = express();
const PORT = process.env.PORT || 3000;

// --- MySQL Connection ---
const db = mysql.createConnection({
	host: 'localhost',
	user: 'dominion_user',
	password: 'StrongPasswordHere',
	database: 'codex_dominion',
	port: 3306
});

db.connect((err) => {
	if (err) {
		console.error('❌ Database connection failed:', err.stack);
		return;
	}
	console.log('✅ Database connected as ID:', db.threadId);
});

// --- Routes ---
app.get('/', (req, res) => {
	res.send('Codex Dominion is live!');
});

app.get('/status', (req, res) => {
	res.json({
		message: 'Dominion backend is alive',
		timestamp: new Date(),
		dbStatus: db.state
	});
});

// --- Start Server ---
app.listen(PORT, () => {
	console.log(`🚀 Server running on port ${PORT}`);
});
