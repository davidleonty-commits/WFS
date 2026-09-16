---
name: weekly-ttw-clip-finder
description: Weekly TikTok Wiz Avoma clip finder, every Monday morning. Delivers to the director's Slack DM with the workspace Slack connector.
---

CONFIG
DIRECTOR_SLACK_ID: U0BUZ6C0C91 (The only delivery destination for this task.)
SLACK ACCESS: the claude.ai Slack connector, which posts as YOU (the connected user), never as a bot. One sender only: never a second sender.

Run the ttw-avoma-clip-finder skill to source this week's world-class sales coaching clips from TikTok Wiz consultation calls in Avoma.

Invoke the `anthropic-skills:ttw-avoma-clip-finder` skill and follow its full workflow: score how reps executed the Decision Leadership Objection Matrix across the week's Avoma calls, identify the best teachable moments (Great Demo / objection handling / Missed Opportunity), apply the strict clip eligibility gate and verbatim clip-anchor rule, and hand David exact clip-in and clip-out anchors so each Avoma snippet is one click to create.

Use the Avoma connector for all call data. Cover the past week of calls (the most recent 7 days). Deliver the finished clip list to the director's Slack DM with `slack_send_message`, channel = DIRECTOR_SLACK_ID, sent immediately, exactly once. Delivery is proven by the return value only: ok = true, a non-empty ts, and a returned channel matching DIRECTOR_SLACK_ID. On failure retry `slack_send_message` once, then stop, since there is no second sender.