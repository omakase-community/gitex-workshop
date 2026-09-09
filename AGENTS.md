# Workshop entrypoint

When the user asks to start this workshop (for example, "Start the workshop" or "Workshop'u başlat"), read [.agents/skills/workshop-decide/SKILL.md](.agents/skills/workshop-decide/SKILL.md) and begin the conversation. If they already name a workflow, route directly to it instead of repeating the menu.

When the user asks to resume or switch workshop workflows, use the same router and preserve their known choices. For an account-backed workflow, load the selected skill's connection guidance before requesting source material. The agent handles supported setup; the participant chooses their account and approves access.

A request only to read, summarize or review a file is not a request to run the workshop. Starting the workshop does not itself authorize installations, account connections, external writes, scheduled tasks or saving personal context. Obtain the relevant approval at the actual step.

Canonical skills live in `.agents/skills`; `Skills/` and `Examples/` are reading copies. Keep the full folder together. Use the workshop instructions only for workshop requests, not unrelated project work.
