# Docker Commands Quick Reference

## Start All Services
```bash
docker-compose up -d
```
- Starts Redis in background
- `-d` = detached mode (runs in background)

## Stop All Services
```bash
docker-compose down
```
- Stops and removes containers
- Volumes (data) are preserved

## View Logs
```bash
# All services
docker-compose logs -f

# Redis only
docker-compose logs -f redis
```

## Check Status
```bash
docker-compose ps
```

## Restart Services
```bash
docker-compose restart
```

## Stop & Remove Everything (including data)
```bash
docker-compose down -v
```
⚠️ This deletes all cached data!

---

## Development Workflow

### 1. Start Redis
```bash
cd D:\QuantForge-terminal
docker-compose up -d
```

### 2. Run Backend Locally
```bash
# In separate terminal
python -m uvicorn backend.main:app --reload --port 8000
```

### 3. When Done
```bash
# Stop Redis
docker-compose down
```

---

## Troubleshooting

### Redis not connecting?
```bash
# Check if Redis is running
docker-compose ps

# Test connection
docker-compose exec redis redis-cli ping
# Should return: PONG
```

### Reset Redis data
```bash
docker-compose down -v
docker-compose up -d
```

### View Redis keys (debug)
```bash
docker-compose exec redis redis-cli KEYS "*"
```
