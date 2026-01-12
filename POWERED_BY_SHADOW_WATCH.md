# Powered by Shadow Watch Badge

Add this badge to your README or documentation:

## Markdown Badge

```markdown
[![Powered by Shadow Watch](https://img.shields.io/badge/Powered%20by-Shadow%20Watch-9d4edd?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIvPgo8Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSI1IiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)](https://github.com/Tanishq1030/Shadow_Watch)
```

## HTML Badge

```html
<a href="https://github.com/Tanishq1030/Shadow_Watch">
  <img src="https://img.shields.io/badge/Powered%20by-Shadow%20Watch-9d4edd?style=for-the-badge" alt="Powered by Shadow Watch">
</a>
```

## Simple Text Badge (for Terminal/CLI)

```
🌑 Powered by Shadow Watch v0.3.0
https://pypi.org/project/shadowwatch/
```

## ASCII Art Badge (for CLI apps)

```
╔═══════════════════════════════════════╗
║  🌑  Powered by Shadow Watch v0.3.0  ║
║     pypi.org/project/shadowwatch/    ║
╚═══════════════════════════════════════╝
```

## Where to Display

1. **API Root Endpoint** ✅ DONE
   - GET http://localhost:8000/ now shows Shadow Watch info

2. **TUI Status Bar** ✅ DONE
   - Bottom right corner shows "🌑 Powered by Shadow Watch"

3. **README.md** (Add this)
   ```markdown
   ## Powered By
   
   [![Shadow Watch](https://img.shields.io/badge/Powered%20by-Shadow%20Watch-9d4edd?style=for-the-badge)](https://github.com/Tanishq1030/Shadow_Watch)
   
   QuantForge Terminal uses Shadow Watch for behavioral intelligence and security.
   ```

4. **Startup Logs** (Add to main.py)
   ```python
   log.info("=" * 60)
   log.info("🌑 Powered by Shadow Watch v0.3.0")
   log.info("   https://pypi.org/project/shadowwatch/")
   log.info("=" * 60)
   ```

5. **API Documentation** (Swagger/OpenAPI)
   - Add to FastAPI description

6. **About Page** (if you have one in TUI)
   - Show Shadow Watch attribution

## Example Usage in Your README

```markdown
# QuantForge Terminal

A Bloomberg-style financial intelligence platform.

## Features
- Real-time market data
- Advanced charting
- Paper trading
- **Behavioral biometrics powered by Shadow Watch** 🌑

## Security & Personalization

QuantForge Terminal uses [Shadow Watch](https://github.com/Tanishq1030/Shadow_Watch) 
for intelligent user behavior tracking and security:

- Silent activity tracking
- Behavioral fingerprinting
- Trust score calculation
- Auto-generated interest profiles

[![Shadow Watch](https://img.shields.io/badge/Powered%20by-Shadow%20Watch-9d4edd?style=for-the-badge)](https://pypi.org/project/shadowwatch/)
```

---

**Your branding is now live in:**
✅ API root endpoint (http://localhost:8000/)
✅ TUI status bar (bottom right)
🎉 First production client badge earned!
