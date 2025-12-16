const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const axios = require("axios");

const app = express();
app.use(cors());
app.use(bodyParser.json());

const DASHBOARD_URL = process.env.DASHBOARD_URL || "http://dashboard:5555";

app.get("/health", (req, res) => {
  res.json({ status: "healthy", service: "Mobile API Gateway" });
});

// Proxy all dashboard requests
app.all("/api/dashboard/:path(*)", async (req, res) => {
  try {
    const url = `${DASHBOARD_URL}/${req.params.path}`;
    const response = await axios({
      method: req.method,
      url: url,
      data: req.body,
      headers: { 'Content-Type': 'application/json' }
    });
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, "0.0.0.0", () => {
  console.log(`📱 Mobile API Gateway listening on port ${PORT}`);
});
