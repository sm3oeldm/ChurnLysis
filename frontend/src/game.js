const ws = new WebSocket('ws://localhost:8080');

const user_id = crypto.randomUUID();
const session_id = crypto.randomUUID();

ws.onopen = () => {
    console.log('Connected to WebSocket server');
    const sessionStartEvent = {
        event_name: "session_start",
        event_version: "v1",
        event_id: crypto.randomUUID(),
        user_id: user_id,
        session_id: session_id,
        timestamp: new Date().toISOString(),
        client_version: "1.0.0",
        platform: "web",
        is_new_user: true,
        entry_point: "lobby"
    };
    ws.send(JSON.stringify(sessionStartEvent));
};

const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    backgroundColor: '#1d1d1d',
    scene: { preload, create, update }
};

const game = new Phaser.Game(config);

let player;

function preload() {
    this.load.image('player', 'https://examples.phaser.io/assets/sprites/phaser-dude.png');
}

function create() {
    player = this.add.sprite(400, 300, 'player');

    this.input.keyboard.on('keydown', (event) => {
        let moved = false;
        switch(event.code) {
            case 'ArrowUp': player.y -= 10; moved = true; break;
            case 'ArrowDown': player.y += 10; moved = true; break;
            case 'ArrowLeft': player.x -= 10; moved = true; break;
            case 'ArrowRight': player.x += 10; moved = true; break;
            case 'KeyM': sendMatchPlayed(); break;
            case 'KeyD': sendDisconnect(); break;
        }

        if(moved) {
            const moveEvent = {
                event_name: "player_moved",
                event_version: "v1",
                event_id: crypto.randomUUID(),
                user_id: user_id,
                session_id: session_id,
                timestamp: new Date().toISOString(),
                x: player.x,
                y: player.y
            };
            ws.send(JSON.stringify(moveEvent));
        }
    });
}

function update() {}

function sendMatchPlayed() {
    const results = ['win', 'loss', 'disconnect'];
    const result = results[Math.floor(Math.random() * results.length)];

    const matchEvent = {
        event_name: "match_played",
        event_version: "v1",
        event_id: crypto.randomUUID(),
        user_id: user_id,
        session_id: session_id,
        timestamp: new Date().toISOString(),
        match_id: crypto.randomUUID(),
        match_duration_sec: Math.floor(Math.random() * 600),
        result: result,
        opponent_type: "human"
    };
    ws.send(JSON.stringify(matchEvent));
    console.log("Match played event sent:", result);
}

function sendDisconnect() {
    const disconnectEvent = {
        event_name: "disconnect",
        event_version: "v1",
        event_id: crypto.randomUUID(),
        user_id: user_id,
        session_id: session_id,
        timestamp: new Date().toISOString(),
        disconnect_reason: "rage_quit",
        time_since_session_start_sec: Math.floor(Math.random() * 600)
    };
    ws.send(JSON.stringify(disconnectEvent));
    console.log("Disconnect event sent");
}