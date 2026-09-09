# Provider Routes — Checked September 8, 2026

Read the selected provider's row and any corresponding notes. Reuse verified task access first; for missing access follow [agent-run setup](agent-setup.md). Native names below are lookup aliases, not permission to install a guessed ID: the helper resolves an actual official catalog entry.

| Selected source | Native plugin lookup | Direct route / boundary |
| --- | --- | --- |
| Gmail / Google Workspace mail | `gmail` | Native plugin setup first. A fresh Google CLI route needs Cloud-project/OAuth-client prerequisites. |
| Google Calendar | `google-calendar` | Separate from Gmail; connect only if the task needs calendar access. |
| Google Drive / Docs | `google-drive` | Separate from Gmail; covers the selected files, not all workspace data. |
| Outlook / Hotmail email | `outlook-email` | Verify personal-account support in the offered connection; organizational access is not proof. |
| Outlook calendar | `outlook-calendar` | Verify the selected account and calendar capability separately. |
| Notion | `notion` | `https://mcp.notion.com/mcp`, OAuth. Default helper route retains the tested direct setup; reuse existing configuration. |
| Slack | `slack` | Native plugin CLI setup is supported. Direct Slack MCP requires an eligible registered app and is not a turnkey substitute. |
| Fireflies meeting notes | `fireflies` | `https://api.fireflies.ai/mcp`, OAuth; active provider account required. |
| Apollo enrichment | `apollo` | `https://mcp.apollo.io/mcp`, OAuth. Confirm client data controls first; preserve a deliberately disabled plugin. |
| Instantly outreach | Discover if offered | `https://mcp.instantly.ai/mcp`, API v2 bearer key, **not OAuth**. Requires secure key provisioning. |

## Native Install and First Use

The supported native CLI can discover the catalog with `plugin list --available --json` and install an exact returned ID with `plugin add <pluginId> --json`. The helper checks the actual executable/help and catalog before proposing those commands. Gmail, Drive, Calendar, Outlook Email/Calendar, Slack, Notion, Fireflies and Apollo have native lookup routes; account availability remains host-dependent.

Installation, account authorization and tool readiness are separate. In a live rehearsal, Slack installation completed first; tools became available later, and the first read-only call requested authentication. After the provider reported authentication accepted, a single retry succeeded. This verifies that route in the tested account, not that all participants will see an immediate same-chat card. Follow [readiness handling](agent-setup.md) for a required new chat or remaining account connection.

## Notion

[Notion setup](https://developers.notion.com/guides/mcp/get-started-with-mcp) documents its endpoint and Codex OAuth; the [client guide](https://developers.notion.com/guides/mcp/build-mcp-client) covers client registration. The participant selects the account/workspace. Agree narrower reading scope before using access; broad OAuth consent is not permission to scan every page. A minimal current-user check succeeded in live rehearsal after the tools became available.

## Google and Microsoft

Native plugins are the beginner route. The [Google Workspace CLI](https://github.com/googleworkspace/cli) requires Google Cloud project/client setup for fresh OAuth and is not an officially supported Google product. Reuse an approved provisioned setup if useful; creation of new developer infrastructure is a separate choice.

[Microsoft organizational tooling](https://learn.microsoft.com/en-us/microsoft-agent-365/tooling-servers-overview) has product and licensing prerequisites. It does not establish personal Hotmail support. Use the actual Outlook plugin's account flow; explain an observed account restriction instead of substituting a different service.

## Slack

Use the native plugin route unless a separately provisioned direct connection is already approved. The [direct MCP server](https://docs.slack.dev/ai/slack-mcp-server/) requires an eligible registered app; [PKCE](https://docs.slack.dev/authentication/using-pkce/) does not remove that registration requirement. A registered app belonging to another client is not a workshop credential.

## Fireflies and Apollo

[Fireflies](https://docs.fireflies.ai/getting-started/mcp-configuration) documents a remote OAuth server. The helper's direct route combines that documented protocol with Codex's supported HTTP/OAuth commands; fresh Fireflies authorization has not been live-tested in this package. Prefer native installation when available and read only the selected meeting.

[Apollo](https://docs.apollo.io/docs/apollo-mcp) documents remote OAuth without a standalone-server API key. Before connecting, confirm the client's model-training/data controls satisfy Apollo's requirements; `--training-off-confirmed` records that confirmation, not a settings change. Check plan restrictions and approve credit-consuming research/enrichment separately. Keep company-only public research available when enrichment is not wanted. Sending or enrolling contacts is not part of connection approval.

## Instantly

[Instantly authentication](https://developer.instantly.ai/mcp/authentication) requires an API v2 key. It is not a sign-in-card flow. The supported command references a key environment variable with `--bearer-token-env-var`; the key must already be securely provisioned in the host that will run MCP. A variable in one temporary shell is not proof the desktop app inherits it.

Use the planner's `--token-env INSTANTLY_API_KEY --credentials-provisioned` only after secure provisioning is confirmed. Never request the value in chat, store it in workshop files or expose it in command arguments. Ask before any credential setup outside that scope. Use least-privilege scopes for the chosen task and keep sending approval separate. If no key is available, continue drafting without claiming Instantly is connected.
