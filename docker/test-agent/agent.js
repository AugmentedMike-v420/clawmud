const net = require('net');
const fs = require('fs');
const path = require('path');

const MUD_HOST = process.env.MUD_HOST || 'host.docker.internal';
const MUD_PORT = parseInt(process.env.MUD_PORT || '4000');
const LOGS_DIR = process.env.LOGS_DIR || '/agent/logs';
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;

// Ensure logs directory exists
if (!fs.existsSync(LOGS_DIR)) fs.mkdirSync(LOGS_DIR, { recursive: true });

const sessionId = Date.now().toString(36);
const logFile = path.join(LOGS_DIR, `${new Date().toISOString().split('T')[0]}-${sessionId}.jsonl`);

function log(type, content) {
  const entry = { ts: new Date().toISOString(), type, content };
  console.log(`[${type}] ${content}`);
  fs.appendFileSync(logFile, JSON.stringify(entry) + '\n');
}

async function callClaude(prompt) {
  if (!ANTHROPIC_API_KEY) {
    log('error', 'No ANTHROPIC_API_KEY set');
    return null;
  }
  
  try {
    const res = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 1024,
        messages: [{ role: 'user', content: prompt }],
      }),
    });
    
    const data = await res.json();
    if (data.content && data.content[0]) {
      return data.content[0].text;
    }
    log('error', `Claude API error: ${JSON.stringify(data)}`);
    return null;
  } catch (err) {
    log('error', `Claude API exception: ${err.message}`);
    return null;
  }
}

class MudClient {
  constructor() {
    this.socket = null;
    this.buffer = '';
    this.responseResolve = null;
    this.responseTimeout = null;
  }

  connect() {
    return new Promise((resolve, reject) => {
      log('action', `Connecting to ${MUD_HOST}:${MUD_PORT}`);
      
      this.socket = net.createConnection({ host: MUD_HOST, port: MUD_PORT }, () => {
        log('result', 'Connected to MUD');
        resolve();
      });

      this.socket.on('data', (data) => {
        const text = data.toString();
        this.buffer += text;
        log('receive', text.trim().substring(0, 200));
        
        // Check if we have a complete response (prompt or specific patterns)
        if (this.responseResolve && (
          this.buffer.includes('prompt>') ||
          this.buffer.includes('?') ||
          this.buffer.includes(':')
        )) {
          clearTimeout(this.responseTimeout);
          const response = this.buffer;
          this.buffer = '';
          this.responseResolve(response);
          this.responseResolve = null;
        }
      });

      this.socket.on('error', (err) => {
        log('error', `Socket error: ${err.message}`);
        reject(err);
      });

      this.socket.on('close', () => {
        log('action', 'Disconnected from MUD');
      });
    });
  }

  send(text) {
    log('send', text);
    this.socket.write(text + '\r\n');
  }

  waitForResponse(timeoutMs = 5000) {
    return new Promise((resolve) => {
      this.buffer = '';
      this.responseResolve = resolve;
      this.responseTimeout = setTimeout(() => {
        const response = this.buffer;
        this.buffer = '';
        this.responseResolve = null;
        resolve(response);
      }, timeoutMs);
    });
  }

  async sendAndWait(text, timeoutMs = 5000) {
    this.send(text);
    return this.waitForResponse(timeoutMs);
  }

  close() {
    if (this.socket) {
      this.socket.end();
    }
  }
}

async function runVerification() {
  const client = new MudClient();
  
  try {
    await client.connect();
    
    // Wait for initial banner
    await client.waitForResponse(3000);
    
    // Create new character
    log('thought', 'Creating a new character for verification test');
    await client.sendAndWait('new', 3000);
    
    const charName = 'TestBot' + Math.floor(Math.random() * 1000);
    log('action', `Using character name: ${charName}`);
    await client.sendAndWait(charName, 3000);
    
    // Password
    await client.sendAndWait('testpass123', 2000);
    await client.sendAndWait('testpass123', 2000);
    
    // Wait for race selection or game entry
    let response = await client.waitForResponse(5000);
    
    // Select race if prompted
    if (response.toLowerCase().includes('race') || response.toLowerCase().includes('select')) {
      log('action', 'Selecting race: human');
      await client.sendAndWait('human', 3000);
    }
    
    // Now in game - start verification
    log('thought', 'Attempting to start AI verification');
    response = await client.sendAndWait('verify start', 5000);
    
    // Process verification challenges
    let challengeCount = 0;
    const maxChallenges = 10;
    
    while (challengeCount < maxChallenges) {
      challengeCount++;
      log('thought', `Processing challenge ${challengeCount}`);
      
      // Check for challenge patterns
      if (response.includes('CHALLENGE') || response.includes('numbers') || response.includes('pattern') || response.includes('code')) {
        log('action', 'Detected challenge, calling Claude for solution');
        
        const solution = await callClaude(
          `You are playing a MUD game and need to solve a verification challenge. Here is what the game shows:\n\n${response}\n\nProvide ONLY the answer to type, nothing else. If it asks for numbers, just give the numbers. If it asks for a pattern, give the pattern. Be concise.`
        );
        
        if (solution) {
          log('thought', `Claude suggests: ${solution}`);
          
          // Send the solution
          if (solution.includes('verify answer')) {
            response = await client.sendAndWait(solution.trim(), 8000);
          } else {
            response = await client.sendAndWait(`verify answer ${solution.trim()}`, 8000);
          }
          
          log('result', `Response: ${response.substring(0, 200)}`);
        } else {
          log('error', 'Failed to get solution from Claude');
          response = await client.sendAndWait('verify next', 5000);
        }
      } else if (response.includes('PASSED') || response.includes('IMMORTAL') || response.includes('verified')) {
        log('result', '🎉 Verification complete!');
        break;
      } else if (response.includes('FAILED') || response.includes('failed')) {
        log('error', 'Verification failed');
        response = await client.sendAndWait('verify next', 5000);
      } else {
        // Request next challenge
        response = await client.sendAndWait('verify next', 5000);
      }
    }
    
    log('action', 'Test complete, disconnecting');
    client.close();
    
  } catch (err) {
    log('error', `Fatal error: ${err.message}`);
    client.close();
  }
}

// Main
log('action', '🤖 Test Agent starting');
log('action', `Session: ${sessionId}`);
log('action', `Log file: ${logFile}`);

runVerification().then(() => {
  log('action', 'Agent finished');
  process.exit(0);
}).catch((err) => {
  log('error', `Agent crashed: ${err.message}`);
  process.exit(1);
});
