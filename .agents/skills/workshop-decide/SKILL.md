---
name: workshop-decide
description: Start or navigate the Codex CRM and sales workshop, including "Start the workshop" and "Workshop'u başlat", choose among seven workflows, or return to its menu. Route to customer research, email, meeting actions, work planning, Notion answers, Slack catch-up, or meeting preparation without restarting completed work.
---

# Workshop guide

Read [common](references/common.md) before starting or resuming. This is a conversational guide, not a form or a timed assessment.

## Welcome or resume

If the participant already has a goal or requested destination, load the matching skill before answering that request. Reuse previous results and choices. For a fresh start, open in English with a short welcome and these seven outcomes; this is a menu, not a sequence to complete:

1. **Find My Next Customers** - clarify your ideal customer and research suitable companies.
2. **Write Emails in My Style** - explore your email and prepare messages that sound like you.
3. **Turn Meetings Into Action** - turn a customer conversation into useful records and follow-ups.
4. **Plan My Day / Week** - find priorities and open loops: promises and follow-ups that may need attention.
5. **Find Answers in Notion** - answer a real project question using your workspace's knowledge.
6. **Catch Up With My Team** - understand what changed in selected Slack conversations.
7. **Get Ready for My Next Meeting** - bring the context, open questions, and goal into a useful preparation brief.

Mention once: "We'll connect only what your chosen workflow needs. I'll handle the supported setup steps with your approval; you sign in with the provider. You can also use our fictional Kivo examples. Explore freely, continue where we left off, or ask to try another workflow. If setup needs a new chat, I'll help you carry over a short recap."

Ask which outcome they want to explore. If unsure, ask one question about their work and suggest the best fit. The selected skill leads with the relevant connection, while account authorization remains the participant's choice. There is no all-app setup checklist before choosing a workflow.

## Route by intent

Load only the selected skill, using its installed location or the sibling path below. These skills allow normal automatic selection; reading a skill's instructions is not equivalent to performing its external actions.

| Intent | Skill | Inputs and optional connections |
| --- | --- | --- |
| ICP, buyer fit, prospect companies | [workshop-find-customers](../workshop-find-customers/SKILL.md) | Their business or Kivo; public web research. Apollo is optional. |
| Email voice, a draft, a particular conversation | [workshop-email-style](../workshop-email-style/SKILL.md) | Connect Gmail or Outlook Email first unless a different source is already chosen. |
| Meeting needs, objections, CRM updates, follow-ups | [workshop-meeting-actions](../workshop-meeting-actions/SKILL.md) | Connect the meeting's source or use a supplied/chosen transcript. Notion writes are optional. |
| Today/next week, open loops, promises, priorities | [workshop-plan-week](../workshop-plan-week/SKILL.md) | Connect the relevant email source; calendar is optional. |
| Questions across project pages and existing knowledge | [workshop-notion-answers](../workshop-notion-answers/SKILL.md) | Connect Notion and choose the relevant project/pages. |
| Team catch-up, changes between weeks, Slack decisions | [workshop-team-catchup](../workshop-team-catchup/SKILL.md) | Connect Slack and choose channel/date scope. |
| Upcoming meeting, pre-call context, agenda, rehearsal | [workshop-meeting-prep](../workshop-meeting-prep/SKILL.md) | Connect calendar if needed to choose the meeting, then relevant context sources. |

Pass along what is already known: the participant's aim, language, own/example source mode, company, selected scope, available connections, current result, and pending decision. Let the selected skill establish any missing input. Do not stack a second intake questionnaire in front of it.

## Return without reset

On "another workflow" or "menu", show the seven outcomes again, briefly noting any result they may reuse. On "continue where we left off", restore the last guided goal and pending decision from this conversation. When the participant is exploring their own question, stay with that question until they ask to return.

For missing context, apply the recovery procedure in [delivery](references/delivery.md); acknowledge what is missing instead of inventing prior progress. If a sibling file is missing, explain that the full workshop folder is needed and help locate it. Do not silently substitute a different skill or claim this package was installed globally.
