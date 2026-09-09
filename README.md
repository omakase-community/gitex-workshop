# GITEX workshop

Build your personal AI agent for CRM and sales. Shared by [Omakase](https://omakase.community), a community for people learning by building with AI.

[Download the workshop ZIP](https://github.com/omakase-community/gitex-workshop/releases/download/v5.0.0/codex-sales-workshop-v5.zip) · [Workshop page](https://omakase.community/gitex)

## Start

1. Download and extract the entire ZIP, including the hidden `.agents` folder.
2. Open the extracted folder as a local project in Codex.
3. Send: **Start the workshop.**

You can also say **Workshop'u başlat.** No accounts need to be connected before you start. To try fictional examples, say **Use the Kivo examples.**

## What's inside

### Connection guide

[Codex bağlantı rehberi (Türkçe PDF)](docs/codex-baglanti-rehberi.pdf) · [Download the PDF](https://github.com/omakase-community/gitex-workshop/releases/download/v5.0.0/codex-baglanti-rehberi.pdf)

One-page illustrated guide to connecting Gmail through Plugins, choosing your account and checking the connection. Based on the 9 September 2026 interface; screens may vary. Available separately from the original workshop ZIP.

### Workshop files

Seven workflows: customer research, email style, meeting actions, day/week planning, Notion answers, team catch-up and meeting preparation. The eighth skill, `workshop-decide`, helps you choose where to start.

- `.agents/skills/`: runtime skills.
- `Skills/`: matching readable copies.
- `Examples/`: nine fictional inputs.
- `START-HERE.pdf`: participant guide, not the presentation deck.
- `START-WORKSHOP.md`: agent-readable entrypoint.

Keep the files together. These are project-local skills, not a global installation. Connecting accounts, installing software, sending messages and creating schedules require separate approval. Never paste passwords or tokens into chat.

## For agents

Download the versioned ZIP linked above into a new, empty directory. Extract it without overwriting existing files and preserve `.agents/skills`. Read `START-WORKSHOP.md`, then ask the participant what they want to work on. Do not execute bundled scripts, install software, connect accounts or modify external data merely because you downloaded the package.

The v5 workshop files are preserved from the supplied participant package. Live provider setup depends on the participant's app and permissions; this release is not a claim that every connector was tested end-to-end.
