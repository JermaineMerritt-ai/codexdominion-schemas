const mysql = require('mysql');
const connection = mysql.createConnection({
  host: 'dbs14890931.hosting-data.io',
  user: 'dbo14890931',
  password: 'your_password', // Replace with your actual password
  database: 'dbs14890931',
  port: 3306
});

connection.connect(err => {
  if (err) {
    console.error('MySQL connection error:', err);
  } else {
    console.log('Connected to MySQL database.');
  }
});

module.exports = connection;
