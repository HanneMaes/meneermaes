---
title: Installatie
created: 2026-06-09 10:05:52 +0200
last_modified: 2026-06-09 10:28:28 +0200
---

# Setup-up 

[Installatie & 1e gevecht](https://robocode.dev/tutorial/getting-started.html)

# Errors & Fixes
## ModuleNotFoundError: No module named 'robocode_tank_royale'
Python kan de module `robocode_tank_royale` niet vinden.

**Fix:** installeerd de `robocode_tank_royale` package.
1. Open **PowerShell** en voor dit command uit: `pip install robocode-tank-royale`
2. `python -c "from robocode_tank_royale.bot_api.bot import Bot; print('OK')"`, als je `OK` ziet is de package geinstalleerd
3. **Herstart** Robocode
