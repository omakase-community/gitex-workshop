"""Read-only connector preflight: inspect capabilities/configuration; propose, never run, setup."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

PROVIDERS = {
    'notion': 'Notion', 'gmail': 'Gmail', 'outlook': 'Outlook Email',
    'google-calendar': 'Google Calendar', 'google-drive': 'Google Drive',
    'outlook-calendar': 'Outlook Calendar', 'slack': 'Slack',
    'fireflies': 'Fireflies', 'apollo': 'Apollo', 'instantly': 'Instantly',
}
PLUGIN_NAMES = {key: key for key in PROVIDERS if key != 'instantly'}
PLUGIN_NAMES['outlook'] = 'outlook-email'
MARKETPLACE = 'openai-curated-remote'
DIRECT_URLS = {
    'notion': 'https://mcp.notion.com/mcp',
    'apollo': 'https://mcp.apollo.io/mcp',
    'fireflies': 'https://api.fireflies.ai/mcp',
    'instantly': 'https://mcp.instantly.ai/mcp',
}
NOTION_URL = DIRECT_URLS['notion']
SAFE_NAME = re.compile(r'[A-Za-z0-9_][A-Za-z0-9_-]*\Z')
SAFE_ENV = re.compile(r'[A-Z_][A-Z0-9_]*\Z')
RESERVED_ENV = {'HOME', 'PATH', 'SHELL', 'USER', 'CODEX_HOME', 'PYTHONPATH'}
AUTH_KEYS = ('bearer_token_env_var', 'http_headers', 'env_http_headers', 'oauth')


def result(status, **fields):
    return {'status': status, 'mutated': False, 'connection_verified': False, **fields}


class Stop(dict):
    """Distinguish a locally generated stop from untrusted inventory fields."""


def blocked(reason):
    return Stop(result('blocked', reason=reason))


def candidates(explicit=None):
    if explicit:
        yield Path(explicit).expanduser()
        return
    seen = set()
    names = ['codex.exe'] if os.name == 'nt' else ['codex']
    for directory in os.get_exec_path():
        for name in names:
            path = Path(directory) / name
            if str(path) not in seen:
                seen.add(str(path))
                yield path
    if os.name != 'nt':
        for parent in (Path('/Applications'), Path.home() / 'Applications'):
            for app in ('ChatGPT.app', 'Codex.app'):
                path = parent / app / 'Contents/Resources/codex'
                if str(path) not in seen:
                    seen.add(str(path))
                    yield path


def discover_cli(explicit=None, runner=subprocess.run):
    """Recognize plugin-only as well as MCP-only CLIs; skip broken PATH wrappers."""
    checks = {
        'mcp_list': (['mcp', 'list', '--help'], ('--json',)),
        'mcp_add': (['mcp', 'add', '--help'], ('--url',)),
        'mcp_login': (['mcp', 'login', '--help'], ()),
        'plugin_list': (['plugin', 'list', '--help'], ('--available', '--json')),
        'plugin_add': (['plugin', 'add', '--help'], ('--json',)),
    }
    for path in candidates(explicit):
        if not path.is_file() or not os.access(path, os.X_OK):
            continue
        capabilities = {'path': str(path), 'bearer': False}
        for key, (args, flags) in checks.items():
            try:
                call = runner([str(path), *args], capture_output=True, text=True, timeout=4)
                capabilities[key] = call.returncode == 0 and all(flag in call.stdout for flag in flags)
                if key == 'mcp_add' and capabilities[key]:
                    capabilities['bearer'] = '--bearer-token-env-var' in call.stdout
            except (OSError, subprocess.TimeoutExpired):
                capabilities[key] = False
        if capabilities['mcp_list'] or capabilities['plugin_list']:
            return capabilities
    return None


def endpoint(entry):
    transport = entry.get('transport', {})
    return transport.get('url', entry.get('url')) if isinstance(transport, dict) else entry.get('url')


def matching_endpoint(value, provider):
    if not isinstance(value, str) or provider not in DIRECT_URLS:
        return False
    try:
        parsed, expected = urlsplit(value), urlsplit(DIRECT_URLS[provider])
        return parsed.hostname == expected.hostname and parsed.path.rstrip('/') == expected.path
    except ValueError:
        return False


def standard_endpoint(value):
    if not isinstance(value, str):
        return False
    try:
        parsed = urlsplit(value)
        return (parsed.scheme == 'https' and parsed.port in (None, 443)
                and not any((parsed.username, parsed.password, parsed.query, parsed.fragment)))
    except ValueError:
        return False


def mcp_entries_valid(entries):
    return isinstance(entries, list) and all(isinstance(e, dict) and isinstance(e.get('name'), str) for e in entries)


def native_mcp_collision(provider, entries):
    """Do not duplicate an existing custom/disabled MCP merely because native is preferred."""
    names = {provider, PLUGIN_NAMES.get(provider, provider)}
    names |= {name.replace('-', '_') for name in names}
    if provider in ('gmail', 'google-calendar', 'google-drive'):
        names |= {'google-workspace', 'google_workspace'}
    if provider in ('outlook', 'outlook-calendar'):
        names |= {'outlook', 'microsoft-365', 'microsoft_365'}
    for entry in entries:
        if entry['name'] in names:
            return True
        # Slack's official direct endpoint is recognized for preservation, not login.
        if provider == 'slack':
            value = endpoint(entry)
            try:
                parsed = urlsplit(value) if isinstance(value, str) else None
                if parsed and parsed.hostname == 'mcp.slack.com' and parsed.path.rstrip('/') == '/mcp':
                    return True
            except ValueError:
                continue
    return False


def existing_direct(provider, entries):
    """Return a server, a sanitized stop result, or None; preserve conflicting names."""
    if not mcp_entries_valid(entries):
        return blocked('Unknown MCP list schema; inspect the supported CLI before changing anything.')
    matches = [e for e in entries if matching_endpoint(endpoint(e), provider)]
    if len(matches) > 1:
        return blocked('Multiple matching provider servers; choose an existing connection before setup.')
    if not matches:
        if any(e['name'] == provider for e in entries):
            return blocked('The provider server name belongs to another configuration; preserve and review it.')
        return None
    entry = matches[0]
    transport = entry.get('transport', {})
    if not standard_endpoint(endpoint(entry)):
        return blocked('The existing endpoint has nonstandard options; preserve and review it.')
    if not SAFE_NAME.fullmatch(entry['name']):
        return blocked('The existing server name needs manual review; no command generated.')
    if entry.get('enabled') is False:
        return blocked('The existing provider server is disabled; ask before changing its state.')
    if not isinstance(transport, dict) or transport.get('type') not in (None, 'streamable_http', 'http'):
        return blocked('The existing transport differs from the supported HTTP route; preserve it.')
    allowed = ('bearer_token_env_var',) if provider == 'instantly' else ()
    if any((entry.get(k) or transport.get(k)) for k in AUTH_KEYS if k not in allowed):
        return blocked('The existing server has custom authentication settings; preserve and review them.')
    return entry


def direct_plan(provider, cli, entries, *, token_env=None, credentials_provisioned=False):
    if provider not in DIRECT_URLS:
        return blocked('No supported direct provider route; no command generated.')
    if token_env is not None and (provider != 'instantly' or not isinstance(token_env, str)
                                  or not SAFE_ENV.fullmatch(token_env) or token_env in RESERVED_ENV):
        return blocked('Use only a dedicated Instantly credential environment variable NAME; never a secret value.')
    existing = existing_direct(provider, entries)
    if isinstance(existing, Stop):
        return existing
    label = PROVIDERS[provider]
    if provider == 'instantly':
        if existing:
            transport = existing.get('transport', {})
            configured_env = existing.get('bearer_token_env_var') or transport.get('bearer_token_env_var')
            if not isinstance(configured_env, str) or not SAFE_ENV.fullmatch(configured_env) or configured_env in RESERVED_ENV:
                return blocked('Existing Instantly credentials need review; do not replace them or request secret values in chat.')
            if token_env and token_env != configured_env:
                return blocked('The existing credential variable differs; preserve it and confirm the intended connection.')
            return result('configured_credentials_unverified', provider=label, server_name=existing['name'],
                          next='Verify credential availability in the actual Codex host and a minimal authorized read; never print the value.')
        if not token_env or not credentials_provisioned:
            return result('credential_required', provider=label,
                          next='Ask whether an API v2 key has been securely provisioned in the Codex host. Accept only its environment variable name, never its value.')
        if not SAFE_ENV.fullmatch(token_env) or token_env in RESERVED_ENV:
            return blocked('Use a dedicated credential environment variable NAME, not a secret or shell expression.')
        return result('approval_required', action='add_bearer_server', provider=label,
                      command=[cli, 'mcp', 'add', provider, '--url', DIRECT_URLS[provider], '--bearer-token-env-var', token_env],
                      next='After approved setup, verify actual host credential availability and a minimal read. This route does not use OAuth.')
    if not existing:
        return result('approval_required', action='add_then_authorize', provider=label,
                      scope='Codex user configuration on this host',
                      command=[cli, 'mcp', 'add', provider, '--url', DIRECT_URLS[provider]],
                      next='Add may start OAuth. Inspect the real result; do not launch a duplicate login. Consent and tool readiness remain separate.')
    name = existing['name']
    auth = str(existing.get('auth_status', '')).lower()
    if auth in ('unsupported', 'bearer_token'):
        return blocked('Existing authentication is not the supported OAuth state; inspect it before login.')
    if auth in ('oauth', 'authenticated', 'authorized', 'logged_in'):
        return result('configured_auth_reported', provider=label, server_name=name,
                      next='Verify actual callable tools and intended account; do not repeat login if usable.')
    if auth not in ('not_logged_in', 'not_authenticated', 'unauthenticated'):
        return result('configured_auth_unknown', provider=label, server_name=name,
                      login_command=[cli, 'mcp', 'login', name],
                      next='Unknown does not mean logged out. Reuse observed OAuth success and check tool readiness. Use login only if authorization is needed and approved.')
    return result('approval_required', action='authorize_existing', provider=label, server_name=name,
                  command=[cli, 'mcp', 'login', name],
                  next='Configuration exists; authorization and tool readiness still need verification.')


def notion_plan(cli, entries):
    """Keep V4's pure direct planner callable for regression tests."""
    return direct_plan('notion', cli, entries)


def incomplete_catalog(response, data):
    # Exit 0 can conceal failed remote discovery and a local-only catalog.
    lines = [line for line in (response.stderr or '').splitlines() if 'could not create PATH aliases' not in line]
    failed = re.search(r'fail|unable|error|denied|timeout|timed out|unreachable', '\n'.join(lines), re.I)
    return bool(response.returncode or failed or (isinstance(data, dict) and (data.get('errors') or data.get('error'))))


def catalog_entry(provider, data):
    """Resolve only an exact provider name in the verified official marketplace."""
    if not isinstance(data, dict) or any(not isinstance(data.get(k), list) for k in ('installed', 'available')):
        return blocked('Unknown plugin catalog schema; no installation command generated.')
    expected = PLUGIN_NAMES.get(provider)
    if expected is None:
        return None
    matches = []
    for group in ('installed', 'available'):
        for entry in data[group]:
            if not isinstance(entry, dict):
                return blocked('Unknown plugin entry schema; no installation command generated.')
            if entry.get('name') != expected:
                continue
            if entry.get('marketplaceName') != MARKETPLACE:
                if group == 'installed' or entry.get('installed') is True:
                    return blocked('A custom provider plugin is installed; preserve it and confirm the intended connection.')
                continue
            if entry.get('pluginId') != expected + '@' + MARKETPLACE:
                return blocked('Provider catalog identity is inconsistent; do not guess an install selector.')
            state = entry.get('installed', group == 'installed')
            if not isinstance(state, bool) or state != (group == 'installed'):
                return blocked('Provider installation state is inconsistent; inspect before setup.')
            matches.append({**entry, 'installed': state})
    if len(matches) > 1:
        return blocked('Multiple provider catalog entries match; resolve the ambiguity before setup.')
    return matches[0] if matches else None


def plugin_plan(provider, cli, entry):
    label = PROVIDERS[provider]
    if not entry:
        return result('unavailable', provider=label,
                      next='No exact official catalog entry was returned. Check provider-routes.md for the selected provider; do not guess a plugin ID.')
    if entry['installed']:
        if entry.get('enabled') is not True:
            return blocked('The provider plugin is disabled or its enabled state is unknown; preserve it and ask before changing anything.')
        return result('installed_readiness_unknown', provider=label, plugin_id=entry['pluginId'],
                      next='Reuse this installation. Discover actual tools; perform a minimal authorized read. If first-use authentication is requested and accepted, retry that read once. Installation does not prove authorization; do not reinstall to trigger it.')
    if entry.get('installPolicy') != 'AVAILABLE':
        return blocked('Provider installation is not explicitly available in the current catalog; respect the policy and verify with the administrator.')
    return result('approval_required', action='install_plugin', provider=label,
                  plugin_id=entry['pluginId'], command=[cli, 'plugin', 'add', entry['pluginId'], '--json'],
                  scope='Selected official plugin on this Codex host',
                  next='Inspect the actual install result, then complete the real connection prompt if offered. ON_INSTALL metadata alone is not OAuth success. A new chat or supported reload may be needed to expose tools.')


def plan(provider, explicit_cli=None, runner=subprocess.run, *, route='auto',
         training_off_confirmed=False, token_env=None, credentials_provisioned=False):
    if provider not in PROVIDERS or route not in ('auto', 'native', 'direct'):
        return blocked('Unknown provider or route; no command generated.')
    if route == 'direct' and provider not in DIRECT_URLS:
        return blocked('No turnkey direct route is enabled for this provider. Use the supported native connection; developer-app setup requires a separate decision.')
    if token_env is not None and (provider != 'instantly' or not isinstance(token_env, str)
                                  or not SAFE_ENV.fullmatch(token_env) or token_env in RESERVED_ENV):
        return blocked('Only Instantly accepts a dedicated credential environment variable NAME; never provide a secret value.')
    cli = discover_cli(explicit_cli, runner)
    if cli is None:
        return blocked('No working Codex executable with native plugin or MCP inspection found. Locate the installed executable; do not reinstall silently.')
    executable = cli['path']
    entries, existing, selected = [], None, None
    if cli['mcp_list']:
        try:
            response = runner([executable, 'mcp', 'list', '--json'], capture_output=True, text=True, timeout=10)
            if response.returncode:
                return blocked('MCP configuration could not be read; no setup command generated.')
            entries = json.loads(response.stdout)
            if not mcp_entries_valid(entries):
                return blocked('Unknown MCP list schema; no setup command generated.')
            if provider in DIRECT_URLS:
                existing = existing_direct(provider, entries)
                if isinstance(existing, Stop):
                    return existing
            elif native_mcp_collision(provider, entries):
                return blocked('An existing same-provider MCP configuration was found. Verify and reuse its tools; preserve disabled/custom settings and ask before adding another connection.')
        except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError):
            return blocked('MCP inspection failed or returned unreadable data; no setup command generated.')
    if cli['plugin_list']:
        try:
            response = runner([executable, 'plugin', 'list', '--available', '--json'], capture_output=True, text=True, timeout=15)
            try:
                catalog = json.loads(response.stdout)
            except json.JSONDecodeError:
                catalog = None
            if incomplete_catalog(response, catalog):
                return result('discovery_incomplete', provider=PROVIDERS[provider],
                              next='Remote catalog discovery failed or is partial. Retry once with permitted network access; do not infer absence, install, or substitute another route from this result.')
            selected = catalog_entry(provider, catalog)
            if isinstance(selected, Stop):
                return selected
        except (OSError, subprocess.TimeoutExpired):
            return result('discovery_incomplete', provider=PROVIDERS[provider],
                          next='Plugin discovery did not complete. Retry once when permitted; no installation or fallback route was selected.')
    if selected and selected['installed'] and selected.get('enabled') is not True:
        return plugin_plan(provider, executable, selected)
    if provider == 'apollo' and not training_off_confirmed:
        return result('provider_prerequisite', provider='Apollo',
                      next='Apollo requires model training off. Ask the participant to confirm that requirement is met; do not alter account settings silently. Credit-consuming enrichment remains separately authorized.')
    if existing:
        # A route preference never silently duplicates an existing direct server.
        output = direct_plan(provider, executable, entries, token_env=token_env, credentials_provisioned=credentials_provisioned)
        if 'command' in output and not cli['mcp_login'] and provider != 'instantly':
            return blocked('Existing server needs OAuth but this executable has no supported login command; preserve it and locate a compatible host.')
        if not cli['mcp_login']:
            output.pop('login_command', None)
        return output
    if selected and selected['installed']:
        return plugin_plan(provider, executable, selected)
    use_direct = route == 'direct' or (route == 'auto' and provider in ('notion', 'instantly'))
    if not use_direct:
        if not cli['plugin_list']:
            return result('native_setup_unavailable', provider=PROVIDERS[provider],
                          next='This executable cannot inspect the native catalog. Discover a supported setup tool or compatible installed CLI; do not assume the provider is unavailable.')
        output = plugin_plan(provider, executable, selected)
        if 'command' in output and not cli['plugin_add']:
            return blocked('The catalog is readable but the native install command is unsupported; no install command generated.')
        return output
    if selected and selected.get('installPolicy') != 'AVAILABLE':
        return blocked('The provider is restricted by native catalog policy; do not bypass it with a direct route.')
    if not cli['mcp_list'] or not cli['mcp_add'] or (provider != 'instantly' and not cli['mcp_login']):
        return blocked('This executable lacks the required direct MCP commands; locate a compatible installed CLI or choose the supported native route.')
    if provider == 'instantly' and not cli['bearer']:
        return blocked('This executable does not support a bearer environment variable; no credential setup command generated.')
    if provider == 'apollo' and not cli['plugin_list']:
        return blocked('Apollo native-plugin state could not be checked; inspect it before adding an alternate direct connection.')
    return direct_plan(provider, executable, entries, token_env=token_env, credentials_provisioned=credentials_provisioned)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('provider', choices=PROVIDERS)
    parser.add_argument('--codex', help='Optional verified native Codex executable path')
    parser.add_argument('--route', choices=('auto', 'native', 'direct'), default='auto')
    parser.add_argument('--training-off-confirmed', action='store_true', help='Participant confirmed Apollo model-training prerequisite')
    parser.add_argument('--token-env', help='Instantly credential environment variable NAME; never the value')
    parser.add_argument('--credentials-provisioned', action='store_true', help='Participant confirmed secure credential provisioning in this Codex host')
    args = parser.parse_args()
    data = plan(args.provider, args.codex, route=args.route,
                training_off_confirmed=args.training_off_confirmed, token_env=args.token_env,
                credentials_provisioned=args.credentials_provisioned)
    print(json.dumps(data, indent=2))
    return 2 if data['status'] == 'blocked' else 0


if __name__ == '__main__':
    raise SystemExit(main())
