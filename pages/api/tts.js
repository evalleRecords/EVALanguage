// api/tts.js
import fetch from "node-fetch";

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.status(405).json({ error: "POST only" });
    return;
  }

  const { text, speaker = "mari", speed = 1 } = req.body;

  try {
    const resp = await fetch("https://api.tartunlp.ai/text-to-speech/v2", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, speaker, speed }),
    });

    if (!resp.ok) {
      const errText = await resp.text();
      res.status(resp.status).send(errText);
      return;
    }

    res.setHeader("Content-Type", "audio/wav");
    const buffer = await resp.arrayBuffer();
    res.send(Buffer.from(buffer));
  } catch (err) {
    res.status(500).send("Proxy error: " + err.message);
  }
}
