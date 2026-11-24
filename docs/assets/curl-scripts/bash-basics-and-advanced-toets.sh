#!/usr/bin/env bash

# server.log
cat >server.log <<'EOF'
2026-11-24 08:01:12 user01 login
2026-11-24 08:05:23 user02 login
2026-11-24 08:10:45 user01 download
2026-11-24 08:15:32 user03 login
2026-11-24 08:20:11 user02 upload
2026-11-24 08:25:47 user01 login
2026-11-24 08:30:02 user04 login
2026-11-24 08:35:19 user03 download
2026-11-24 08:40:55 user01 upload
2026-11-24 08:45:21 user02 login
2026-11-24 08:50:36 user04 download
2026-11-24 08:55:08 user01 login
2026-11-24 09:00:42 user03 upload
2026-11-24 09:05:17 user02 download
2026-11-24 09:10:29 user01 logout
2026-11-24 09:15:53 user04 login
2026-11-24 09:20:14 user03 login
2026-11-24 09:25:38 user02 upload
2026-11-24 09:30:06 user01 download
2026-11-24 09:35:49 user04 logout
EOF

# mederwerkers.log
cat >medewerkers.log <<'EOF'
Hanne
Pieter
Sarah
Thomas
Hanne
Sarah
Pieter
Hanne
Thomas
Sarah
Pieter
Hanne
EOF

# FINISHED
echo
echo "Veel succes met de toets!"
