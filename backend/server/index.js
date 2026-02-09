const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');

const PORT = 8080;
// Resolve absolute path to data/raw directory relative to this file
const RAW_DATA_DIR = 'C:\\churn_analysis-';

const wss = new WebSocket.Server({ port: PORT });

console.log(`WebSocket server running on ws://localhost:${PORT}`);

// Make sure raw data directory exists
try {
  if (!fs.existsSync(RAW_DATA_DIR)) {
    fs.mkdirSync(RAW_DATA_DIR, { recursive: true });
  }
  console.log(`Raw data directory: ${RAW_DATA_DIR}`);
} catch (err) {
  console.error('Failed to ensure raw data directory exists:', err);
}

wss.on('connection', ws => {
  console.log('New client connected');

  ws.on('message', message => {
    // Ensure message is a string (handle Buffer on Node.js ws)
    const raw = Buffer.isBuffer(message) ? message.toString('utf8') : String(message);

    let event;
    try {
      event = JSON.parse(raw);
    } catch (err) {
      console.error('Failed to parse incoming message as JSON:', err);
      return;
    }

    const sanitizeForFilename = (str) => {
      return String(str || '')
        .replace(/[<>:"/\\|?*\x00-\x1F]/g, '_') // illegal on Windows
        .replace(/\s+/g, '_')
        .slice(0, 100);
    };

    // Build a unique filename for each event
    const ts = new Date().toISOString().replace(/[:.]/g, '-');
    const eventName = sanitizeForFilename(event.event_name || 'event');
    const userId = sanitizeForFilename(event.user_id || 'anon');
    const unique = `${process.pid}-${Math.floor(Math.random() * 1e9)}`;
    const filename = `${ts}_${eventName}_${userId}_${unique}.json`;
    const filepath = path.join(RAW_DATA_DIR, filename);

    // Write event to disk
    fs.writeFile(filepath, JSON.stringify(event, null, 2), (err) => {
      if (err) {
        console.error('Failed to save event:', err);
        return;
      }
      console.log(`Saved event to: ${filepath}`);
    });

    // Broadcast to other clients
    wss.clients.forEach(client => {
      if (client !== ws && client.readyState === WebSocket.OPEN) {
        try {
          client.send(JSON.stringify(event));
        } catch (err) {
          console.error('Failed to broadcast to a client:', err);
        }
      }
    });
  });

  ws.on('close', () => {
    console.log('Client disconnected');
  });
});
