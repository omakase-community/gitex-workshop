# Agent-led connections, scoped to the chosen task

## Establish the source before requesting content

Read this on entering an account-backed workflow, before its first source request. A request like "write in my email style" is enough to trigger connection guidance; the participant need not know the terms plugin or MCP.

Default to the relevant connected source. Check the actual tool inventory, then lead with the benefit and the specific connection. If the provider is unknown, ask which they use. If a relevant account is already connected, reuse it and clarify the reading scope instead of asking them to reconnect. An absent tool triggers [agent-run setup](agent-setup.md), including native plugin CLI discovery when a setup tool is missing; it is not evidence that browser access is the only route.

Honor a source already chosen by the participant: supplied material, an explicit example request, or a refusal to connect. Otherwise establish the connection route before offering pasted messages or screenshots. An unfamiliar provider or absent tool is a reason to discover a supported integration, not an automatic reason to request manual data entry. If setup is declined or unavailable, offer a sanitized input or the bundled examples as a valid alternative.

Source readiness is reached when either (a) the intended account and usable read capability are verified and the reading scope is agreed, or (b) the participant has chosen an accessible alternative. A displayed setup card alone is not readiness. Keep this conversational, with one unresolved question at a time.

## Establish capability, then guide setup

Use the host's available tools and installed integrations to determine what is accessible. Do not infer account connection from a logo, an installed skill, or this package. If the participant has multiple accounts, establish the intended account before reading private content.

Match the source to the task:

- Email: **Gmail** for Gmail/Google Workspace mail, or **Outlook Email** for Microsoft mail. Ask the provider only if unknown. Check personal Hotmail/Outlook.com support in the actual offered connection; organization Microsoft 365 support does not prove personal-account support.
- Knowledge questions: **Notion**, scoped to a chosen project or pages.
- Team catch-up: **Slack**, scoped to the intended workspace, channel(s), and dates.
- Meeting preparation: the relevant calendar when needed to find the meeting; email or already connected knowledge sources for its context.
- Meeting analysis: the service holding the notes/transcript. Ask where they live and discover the supported integration rather than prescribing an unrelated tool.

Google Workspace is not one universal capability: Gmail, Drive, and Calendar access are separate. Add a second source only when it helps the participant's chosen question.

If access is missing:

1. Explain the benefit and limited task, for example: "Let's connect your email so I can learn from messages you've actually sent." Offer the relevant connection or ask which provider they use. Avoid presenting three equivalent data-entry paths before making the recommended connection clear.
2. Read [agent-run setup](agent-setup.md) before selecting the setup action. Use an actual native setup card when supported, otherwise discover the native plugin CLI or documented direct route. Explain the specific configuration change, obtain consent, and run the supported command yourself. The participant should not have to open a terminal or copy commands. A text link is not a native Connect card.
3. The participant signs in and grants access in the provider's trusted UI. Open or present the authorization URL returned by the real setup operation, not a guessed login URL. Passwords, login codes, API keys and tokens stay out of chat and package files. Follow host approval prompts; do not broaden permissions or silently install a new intermediary service. If setup needs an unprovided developer app or client registration, explain that exact prerequisite and let the participant choose whether to pursue it.
4. Verify the resulting connection with an appropriate read-only check. A real tool may initiate first-use authorization. If it reports authorization accepted and explicitly requests a retry, retry that same safe check once; use the new result as evidence. Follow refusals or unresolved login prompts instead of repeatedly calling. For the requested task, distinguish message search, sent-mail access, full thread reading, drafts, sending, and calendar access. Successful sign-in does not prove every capability.

Keep configuration, OAuth completion and usable tools separate. After authorization, check the current tool inventory and use a supported refresh if available; a documented app-server method is not automatically a callable tool in this chat. Do not attach to private app internals to force a refresh. If the host requires reload/new chat, give a short recap following [delivery](delivery.md), including the same workshop project and selected workflow, then verify access again. Preserve the result rather than restarting intake.

## Keep the participant moving

If setup fails or an organization blocks it, state the observed obstacle and the supported next action. Offer the bundled examples, user-provided sanitized material, or permitted browser access as alternatives the participant can choose. An open browser session alone is not their choice to replace the connector. The participant may keep troubleshooting, but finishing the connection is not a condition for workshop progress. Do not repeatedly launch the same failing authorization flow or imply a sample was fetched from their mailbox.

Read only the agreed scope. For mail voice exploration, a recent sample of relevant sent messages can be proposed; a fixed 30-day/10-message scan is not an automatic first action. Prefer human-written sent text over signatures, forwarded quotations, newsletters, and generated templates. Full thread context may be needed before drafting a reply. For work planning, account, time range, and relevant people/projects should be clear enough to search usefully. Request pagination or additional content as needed; distinguish a bounded selection from the entire inbox.

If the chosen integration cannot send mail, still prepare the draft. If a self-send test is requested and supported, confirm the participant's own address and one message, send once, then check on request. Use the actual returned message/thread identifier where possible. Never imply a background inbox listener was activated; delayed delivery is not success evidence. Sample `.example` addresses cannot be used as real recipients.

For Notion, start with the participant's selected test page/database. Inspect its existing structure before proposing changes. A new small CRM may be created when requested; expansion remains conversational. Confirm the target and proposed changes before writing. Label sample records as fictional inside a demo destination; do not merge them into production contacts.

For Slack, channel access does not authorize reviewing every workspace conversation or posting messages. Establish the intended workspace and channel scope; read thread replies needed to interpret the latest decision. Ask separately before posting or changing anything.

Missing account authorization, an unavailable integration/tool, and a permission-denied tool result are different states. Describe the observed state without guessing a permission fix. Preserve the participant's result while choosing the supported next action.

## Evidence and remaining checks

Official documentation consulted for this package on 2026-09-08:

- [Plugins](https://learn.chatgpt.com/docs/plugins): installation, authorization, and newly available tools are distinct steps.
- [Email workflows](https://learn.chatgpt.com/use-cases/manage-your-inbox): Gmail and Outlook Email provide email-oriented workflows; available operations must still be checked in the host.
- [MCP setup](https://learn.chatgpt.com/docs/extend/mcp): MCP configuration and authentication may be separate.

This package has not signed into attendee accounts. Gmail personal/Workspace, Microsoft organization/personal accounts, organization policies, draft/send permissions, and tools becoming available after authorization remain live rehearsal checks. These notes are not a guarantee of a provider or account tier's support.
