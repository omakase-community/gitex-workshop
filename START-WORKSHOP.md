# Start the workshop

To participate, open this folder as a local project in Codex and send **Start the workshop.** You can also say **Workshop'u başlat.** The project entrypoint in [AGENTS.md](AGENTS.md) routes that request to the workshop guide.

When the user asks to start, read [.agents/skills/workshop-decide/SKILL.md](.agents/skills/workshop-decide/SKILL.md), then begin with the participant. If they already named a goal, follow the router into the matching skill before responding rather than repeating the menu. Keep this folder's relative paths intact. A request only to read this file calls for a summary, not automatic execution.

This version offers seven workflows. The canonical runtime instructions are under `.agents/skills`; `Skills/` and `Examples/` are matching reading copies, not separate installations.

Opening the workshop does not authorize connecting accounts, scheduling work, installing software, saving personal context, or changing external data. Follow the participant's chosen task and the selected skill. Lead account-backed workflows with the relevant connection; use its shared setup procedure to perform supported setup after approval rather than assigning terminal commands to the participant. It covers native plugin discovery/install commands as well as documented direct MCP routes. The participant handles account consent; installation, authorization and usable tools are checked separately. Honor chosen examples or supplied input. Keep feedback and further exploration optional.
