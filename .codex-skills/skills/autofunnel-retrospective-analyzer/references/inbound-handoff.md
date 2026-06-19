# Inbound Handoff

Inbound reply handling is a three-step handoff.

1. Runner collector:
   - reads a bounded unread batch, default `1` dialogue per healthy active profile;
   - fetches full targeted history;
   - writes `activity/Chat_history/<user_id>.jsonl`;
   - updates `activity/dialog_index.json` with `reply_needed=true`;
   - does not send a reply.

2. Director:
   - reads saved history;
   - writes a prepared `inbound_reply` into `api_direct_plan.json`;
   - sets `counts_toward_kpi=false`;
   - does not pretend the reply was already sent.

3. Runner sender:
   - sends only prepared text;
   - refetches history;
   - marks plan/history state as sent.

If unread collection hits auth/account errors, fail soft, hold that profile, and
continue local analysis plus other accounts.

