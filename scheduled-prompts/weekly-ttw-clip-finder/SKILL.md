---
name: weekly-ttw-clip-finder
description: Weekly TikTok Wiz Avoma clip finder, every Monday morning. Delivers to Cayden's Slack DM via the Lovable WFS Slack connector.
---

Run the ttw-avoma-clip-finder skill to source this week's world-class sales coaching clips from TikTok Wiz consultation calls in Avoma.

Invoke the `anthropic-skills:ttw-avoma-clip-finder` skill and follow its full workflow: score how reps executed the Decision Leadership Objection Matrix across the week's Avoma calls, identify the best teachable moments (Great Demo / objection handling / Missed Opportunity), apply the strict clip eligibility gate and verbatim clip-anchor rule, and hand Caydo exact clip-in and clip-out anchors so each Avoma snippet is one click to create.

Use the Avoma connector for all call data. Cover the past week of calls (the most recent 7 days). Deliver the finished clip list to Cayden's Slack DM via the Lovable WFS Slack connector (slack_schedule_message, channel @cayden; if that handle errors, use Slack user ID U092C85GA4D), jitter_minutes 0, and send exactly once. Never use the native Slack connector.