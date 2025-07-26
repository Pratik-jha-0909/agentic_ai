const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
app.use(bodyParser.json());

// Replace with your Gemini API key
const GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY';

app.post('/webhook', async (req, res) => {
  const userQuery = req.body.text || req.body.query || 'No query found';

  // Call Gemini API
  const geminiResponse = await axios.post(
    'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + GEMINI_API_KEY,
    {
      contents: [{ parts: [{ text: userQuery }] }]
    }
  );

  const answer = geminiResponse.data.candidates?.[0]?.content?.parts?.[0]?.text || "Sorry, I couldn't get an answer.";

  res.json({
    fulfillment_response: {
      messages: [{ text: { text: [answer] } }]
    }
  });
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => console.log(`Webhook listening on port ${PORT}`));