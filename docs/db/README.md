# Database ERD

Files:
- `erd.puml`: PlantUML source
- `erd.png`: export (optional)

Key entities:
- `users`: accounts with unique username/email
- `scores`: user scores per level with leaderboard indexes
- `game_sessions`: game rounds with mode/status lifecycle

Relationships:
- `scores.user_id -> users.id` (ON DELETE CASCADE)
- `game_sessions.winner_user_id -> users.id` (nullable)

Indexes (high level):
- `users`: unique(username), unique(email)
- `scores`: (user_id), (level), (created_at), (points DESC, created_at DESC), (level, points DESC, created_at DESC)
- `game_sessions`: (status), (started_at DESC)

Generate PNG (requires PlantUML):
```bash
plantuml erd.puml
```
