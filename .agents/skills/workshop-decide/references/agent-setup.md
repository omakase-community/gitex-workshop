# Own Setup; Let the Participant Approve Access

Use after [connections](connections.md) when the selected source needs setup. This procedure applies to every covered connector; only the chosen provider's requirements vary. Completion means usable task access, not just an installed plugin.

## Discover, Approve, Execute, Verify

1. **Discover.** Reuse actual callable tools when available. If the account still needs authorization, use its supported connection action. Otherwise search for a native setup tool and follow its own instructions. Descriptions of unavailable tools do not make them callable. Read the selected row in [provider routes](provider-routes.md) before new setup, including its prerequisites.
2. **Preflight.** When no native setup action is callable, run [connection_plan.py](../scripts/connection_plan.py) with the selected provider using the host's existing Python. This read-only helper discovers a working Codex executable, checks existing configuration and the native plugin catalog, and returns a proposed action. It supports native installation commands as well as documented direct MCP routes. An absent setup tool is not the end of discovery.
3. **Approve.** Explain the specific installation/configuration change and ask to proceed, unless the participant has already approved that setup. For example: "I can set up the Slack connection in Codex. You'll choose your workspace and approve access with Slack. Shall I start?" Choosing a workflow alone is not approval to install. Ask separately before developer-app registration, extra services or purchases.
4. **Execute.** After approval, rerun preflight and execute its returned `command` with the shell tool, respecting filesystem/network approvals. Run it yourself; a command printed as participant homework is not execution. Retain the process/session ID. Allow one active setup process per provider; inspect it before retrying. Preserve disabled, conflicting or customized configurations for an explicit user decision.
5. **Authorize.** Inspect the real result. Present an actual returned authorization URL or connection card and let the participant complete consent. If a process is waiting, say so and resume that process after consent. Installation can finish before any account connection occurs; `ON_INSTALL` metadata alone does not prove authorization. Stop on cancellation or an actionable failure rather than relaunching repeatedly.
6. **Verify.** Inspect the current tool inventory. Use a minimal read-only account/workspace check or the participant's chosen test item. An on-use authentication result that says accepted and asks for a retry permits one retry of that safe check. Verify task-specific capabilities and scope before reading content. Missing tools after setup lead to the readiness procedure below, not another installation.

## Run the Preflight

Agent example: `python3 <path-to-connection_plan.py> slack`. Resolve the real script/interpreter paths; the participant need not run this. Accepted provider keys:

`notion`, `gmail`, `outlook`, `google-calendar`, `google-drive`, `outlook-calendar`, `slack`, `fireflies`, `apollo`, `instantly`.

Default routing reuses existing configuration. Notion retains its tested direct route; other providers prefer the exact matching official native plugin when available. `--route native` or `--route direct` selects a supported route explicitly, but does not override conflicts or policies. `--codex` can select a verified executable when discovery needs help.

- **`approval_required`:** A proposed `command` is available. `install_plugin` installs the catalog's exact plugin ID; `add_then_authorize` adds a direct OAuth server; `authorize_existing` logs into an existing server; `add_bearer_server` configures a securely provisioned bearer environment variable. Execute only after the matching approval.
- **`installed_readiness_unknown` / `configured_auth_reported` / `configured_credentials_unverified`:** Configuration exists. Check tools and account access; do not reinstall. For bearer credentials, also check availability in the actual running host without printing values. Reported authorization is still not usable-tool proof.
- **`configured_auth_unknown`:** Unknown does not mean logged out. This occurred after successful Notion OAuth in a live rehearsal. Reuse the observed success; a conditional login command is only for an authorization that still needs to happen, never an automatic repeat.
- **`discovery_incomplete`:** Catalog discovery failed or was partial. A CLI can exit 0 while reporting remote-catalog failure. Use an allowed network retry once when that is the actual issue; empty partial output cannot establish plugin absence.
- **`provider_prerequisite` / `credential_required`:** Explain the provider-specific requirement. Apollo's training/data-control confirmation must be real; Instantly requires an already securely provisioned key environment variable. Neither flag is a substitute for participant consent.
- **`native_setup_unavailable`:** This executable cannot inspect the native catalog. Locate a compatible installed CLI or actual host setup tool; it does not establish provider absence.
- **`unavailable` / `blocked`:** Follow the specific supported next step. Preserve existing state; do not remove a disabled plugin, replace a custom server or add a duplicate to get around the result.

The helper never installs, authenticates or reads private account content. It emits command arguments, not shell scripts; credentials and custom endpoint strings stay out of its output.

## Finish Native Plugin Connection and Readiness

Native plugin installation is only one stage. Some providers authorize on first use; others need the provider connection step in their installed plugin details.

When tools appear, perform the approved minimal check and follow the provider's actual connection prompt. When tools do not appear, use a supported reload if exposed. Otherwise provide a short [continuation recap](delivery.md) for a new chat in the same workshop project. Include the selected workflow, provider, last verified setup state, and next safe check. The participant should not repeat intake or install again.

If no in-chat connection action appears even after the supported readiness step, guide the participant to **Plugins > the installed provider's details** and its actual connection control. Use observed labels or the [official plugin guide](https://learn.chatgpt.com/docs/plugins); do not fabricate a button, deep link, OAuth URL or Connect directive. This is the remaining account-consent step after agent-owned setup, not the default response to every missing tool. Return to the same workflow once access is verified.

If this is still unavailable or the participant declines, explain the obstacle briefly and let them choose a permitted browser session, supplied input or fictional examples. Keep their progress. Do not attach to private app internals or change security settings to force a refresh.

## Additional Providers

For an explicitly selected provider outside the helper's ten keys, use the host's actual plugin search/setup tools or verified native catalog commands. Inspect the real entry, publisher, prerequisites and CLI help before proposing its exact install command. An unrecognized provider is a discovery task, not permission to invent an endpoint or silently choose a third-party broker.

Commands and behavior: [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp), [native plugins](https://learn.chatgpt.com/docs/plugins). Configuration and authorization live on the selected host, never in the distributed ZIP.
