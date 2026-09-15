---
name: weekly-ttw-clip-finder
description: Weekly TikTok Wiz Avoma clip finder, every Monday morning. Delivers to the director's Slack DM with the workspace bot token.
---

CONFIG
DIRECTOR_SLACK_ID: U0BUZ6C0C91 (The only delivery destination for this task.)
SLACK ACCESS: the WFS Group workspace bot token on the Slack Web API, reached either through the Slack MCP connector or a direct POST to https://slack.com/api/<method> with header Authorization: Bearer $SLACK_BOT_TOKEN. One sender only: never a personal user token, never a second sender.

Run the ttw-avoma-clip-finder skill to source this week's world-class sales coaching clips from TikTok Wiz consultation calls in Avoma.

Invoke the `anthropic-skills:ttw-avoma-clip-finder` skill and follow its full workflow: score how reps executed the Decision Leadership Objection Matrix across the week's Avoma calls, identify the best teachable moments (Great Demo / objection handling / Missed Opportunity), apply the strict clip eligibility gate and verbatim clip-anchor rule, and hand David exact clip-in and clip-out anchors so each Avoma snippet is one click to create.

Use the Avoma connector for all call data. Cover the past week of calls (the most recent 7 days). Deliver the finished clip list to the director's Slack DM with `chat.postMessage`, channel = DIRECTOR_SLACK_ID, sent immediately, exactly once. Delivery is proven by the return value only: ok = true, a non-empty ts, and a returned channel matching DIRECTOR_SLACK_ID. On failure retry `chat.postMessage` once, then stop, since there is no second sender.