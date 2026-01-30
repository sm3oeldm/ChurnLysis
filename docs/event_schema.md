Event Schema (v1)
Overview

This document defines the event schema used to capture user behavior in a real-time multiplayer game.
Events are emitted from the client and ingested by the backend via WebSockets.

The schema is designed to support:

Session-level analytics

Feature engineering for churn prediction

Time-based behavioral analysis

Model explainability

Design Principles

Append-only: Events are immutable once emitted

Time-aware: Every event includes a timestamp

User-centric: Events are tied to users and sessions

Versioned: Schema supports backward compatibility

Common Event Fields

All events include the following base fields:

Field	Type	Description
event_name	string	Name of the event
event_version	string	Schema version (e.g. v1)
event_id	string (UUID)	Unique event identifier
user_id	string (UUID)	Unique user identifier
session_id	string (UUID)	Unique session identifier
timestamp	string (ISO 8601)	Client-side event time
client_version	string	Game client version
platform	string	web
Event: session_start

Emitted when a user starts a new game session.

Fields
Field	Type	Description
event_name	string	session_start
is_new_user	boolean	Whether the user is new
entry_point	string	lobby / matchmaking / invite
Example
{
  "event_name": "session_start",
  "event_version": "v1",
  "event_id": "uuid",
  "user_id": "uuid",
  "session_id": "uuid",
  "timestamp": "2026-01-30T18:12:45Z",
  "client_version": "1.0.0",
  "platform": "web",
  "is_new_user": false,
  "entry_point": "lobby"
}

Event: match_played

Emitted when a match ends (win, loss, or disconnect).

Fields
Field	Type	Description
event_name	string	match_played
match_id	string (UUID)	Unique match identifier
match_duration_sec	integer	Match duration in seconds
result	string	win / loss / disconnect
opponent_type	string	human / bot
Example
{
  "event_name": "match_played",
  "event_version": "v1",
  "event_id": "uuid",
  "user_id": "uuid",
  "session_id": "uuid",
  "timestamp": "2026-01-30T18:27:10Z",
  "client_version": "1.0.0",
  "platform": "web",
  "match_id": "uuid",
  "match_duration_sec": 312,
  "result": "disconnect",
  "opponent_type": "human"
}

Event: disconnect

Emitted when a user disconnects unexpectedly.

Fields
Field	Type	Description
event_name	string	disconnect
disconnect_reason	string	network / quit / crash
time_since_session_start_sec	integer	Time before disconnect
Example
{
  "event_name": "disconnect",
  "event_version": "v1",
  "event_id": "uuid",
  "user_id": "uuid",
  "session_id": "uuid",
  "timestamp": "2026-01-30T18:30:02Z",
  "client_version": "1.0.0",
  "platform": "web",
  "disconnect_reason": "network",
  "time_since_session_start_sec": 185
}

Data Quality Considerations

Client timestamps may drift; backend will add ingestion time

Events may arrive out of order

Duplicate events must be deduplicated using event_id

Churn Modeling Notes

This schema enables:

Session-based aggregation

Detection of inactivity gaps

Identification of rage quits

Time-windowed feature engineering

Explainable churn drivers