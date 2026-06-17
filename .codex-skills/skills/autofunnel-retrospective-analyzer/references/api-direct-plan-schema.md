# API Direct Plan Schema

Default path:

```text
VK/auto_funnel/state/accounts/<account>/api_direct_plan.json
```

Minimal shape:

```json
{
  "version": 1,
  "plan_id": "2026-06-01-anton-next",
  "account": "anton",
  "prepared_at": "2026-06-01T18:00:00+00:00",
  "strategy": {
    "goal": "move selected contacts toward trust-contact list",
    "kpi": {
      "first_messages_per_cycle": 15,
      "incoming_replies_count_toward_kpi": false
    },
    "pacing": {
      "max_messages_per_run": 6,
      "max_first_messages_per_run": 2,
      "max_inbound_replies_per_run": 4,
      "max_followups_per_run": 1,
      "friend_requests": {
        "recommendations": 2,
        "lists": 2
      }
    },
    "source_allocation": {
      "recommendations_per_run": 2,
      "friends_from_lists_per_run": 2,
      "candidate_pool_low_watermark": 20,
      "candidate_pool_target_after_refill": 80,
      "candidate_replenishment": {
        "enabled": true,
        "collector_account": "anton",
        "source": "https://vk.com/example_group",
        "mode": "mixed",
        "status": "not_needed|queued|completed|blocked"
      }
    },
    "social_life": {
      "enabled": true,
      "posture": "low_frequency_attention_and_contact_discovery",
      "pacing": {
        "max_actions_per_run": 1,
        "max_wall_posts_per_run": 0,
        "max_community_actions_per_run": 1
      },
      "asset_dir": "assets/generated_social",
      "community_discovery_dir": "state/social_life/community_discovery"
    },
    "limits": {
      "max_actions_per_account": 12,
      "max_messages_per_account": 8
    },
    "variation": "avatar for new requests, sparse wall-post touches for older accepted friends"
  },
  "targets": [
    {
      "user_id": 123456,
      "display_name": "Имя",
      "stage": "accepted_friend",
      "actions": [
        {"type": "like_avatar", "enabled": true},
        {"type": "like_wall_post", "enabled": true, "post_index": 2},
        {"type": "like_wall_comment", "enabled": false, "post_index": 0, "comment_index": 0}
      ],
      "message": {
        "enabled": true,
        "kind": "first_message",
        "dialogue_direction": "outbound_first_message",
        "counts_toward_kpi": true,
        "not_before": "2026-06-02",
        "text": "готовый текст",
        "reason": "accepted yesterday and profile context is enough for a soft first touch"
      }
    }
  ],
  "social_life_actions": [
    {
      "type": "wall_post",
      "enabled": false,
      "not_before": "2026-06-07",
      "text": "готовый текст поста",
      "image_path": "2026-06-07-anton-reflection.png",
      "reason": "rare profile presence post; image must already exist in assets/generated_social"
    },
    {
      "type": "community_comment",
      "enabled": true,
      "not_before": "2026-06-04",
      "owner_id": -123456,
      "post_id": 777,
      "text": "конкретный комментарий по теме поста",
      "reason": "psychology/AI post matches profile tone and comment is non-generic"
    },
    {
      "type": "inspect_comment_engagement",
      "enabled": false,
      "not_before": "2026-06-06",
      "owner_id": -123456,
      "post_id": 777,
      "comment_id": 888,
      "auto_friend_add": true,
      "max_friend_adds": 2,
      "reason": "follow up on likes/replies to our previous comment"
    }
  ],
  "messages": [
    {
      "user_id": 789012,
      "display_name": "Имя",
      "enabled": false,
      "kind": "hold",
      "dialogue_direction": "hold",
      "counts_toward_kpi": false,
      "not_before": "2026-06-03",
      "text": "",
      "reason": "no fresh basis for a natural message"
    },
    {
      "user_id": 345678,
      "display_name": "Имя",
      "enabled": true,
      "kind": "inbound_reply",
      "dialogue_direction": "inbound_reply",
      "counts_toward_kpi": false,
      "not_before": "2026-06-02",
      "text": "готовый ответ на входящее сообщение",
      "reason": "contact replied first; answer this run but do not count toward first-message KPI"
    }
  ]
}
```

Rules:

- Use `targets[].actions` for likes/touches the next runner may execute.
- Use `target.message` when the message belongs to the same target decision.
- Use top-level `messages[]` for dialogue-only followups or contacts not needing touches.
- Do not omit `enabled`; disabled entries are useful because they explain holds.
- Do not repeat completed actions with `completed_at` unless there is a new explicit reason.
- Do not prepare a message if it sounds generic enough to fit any contact.
- Use `kind=first_message` and `counts_toward_kpi=true` only for first outbound touches counted toward the profile KPI.
- Use `kind=inbound_reply` or `kind=reply_to_inbound` and `counts_toward_kpi=false` for answers to unread incoming dialogues.
- Keep `strategy.pacing` specific enough that the runner can enforce profile-local tempo without editing global config.
- Keep `strategy.pacing.friend_requests.recommendations` and `.lists` explicit when the director changes how many friends this profile should add next run.
- Keep `strategy.source_allocation.candidate_replenishment` explicit when a source list is below watermark or refill is intentionally skipped.
- Use `social_life_actions[]` for rare public profile behavior that creates attention or natural contact reasons: `wall_post`, `community_repost`, `join_group`, `community_comment`, `inspect_comment_engagement`.
- Use ordinary web/internet research to find relevant public VK communities, posts, discussions, and thematic lists; Browser is optional visual verification for public pages only, not account control.
- Use `scripts/discover_social_communities.py --include-subscriptions` when a repost/comment should prefer communities the profile already follows.
- For `wall_post`, `text` must be ready; `image_path` is optional but must point to an existing file under `VK/auto_funnel/assets/generated_social/` unless absolute.
- For `community_comment`, text must be specific to the actual post; no generic comments.
- For `inspect_comment_engagement`, use `auto_friend_add=true` only with a small `max_friend_adds`.
- Regularly inspect the profile's own recent wall posts through API-read. If there are comments, prepare replies; if there are likes from non-friends, treat them as warmer candidates for friend request and possibly a soft prepared first message. Do not message every liker; choose a small, relevant subset.
- If own-post engagement needs an action type the runner does not support yet, record a self-improvement/code task or extend the existing API-only module with tests. Do not create a new standalone script just for that idea.
- Never assign the same enabled unsent message `user_id` to more than one profile. Validate with `python -m VK.auto_funnel.scripts.validate_api_direct_plans`.
- Keep action types inside the API-only set: `like_avatar`, `like_wall_post`, `like_wall_comment`.
- Runner sends only text that already exists in this plan; do not rely on runtime generation.
- Before increasing pacing, read `state/safety/api_call_ledger/latest.json`. If a profile has `critical` findings or a fresh incident note, put write actions on hold; if it has `warning`, lower limits and avoid broad heavy reads like repeated `friends.get`.

Director change-log payload should include:

```json
{
  "cycle_id": "2026-06-01-cycle",
  "based_on_run_id": "run-id",
  "changed_at": "2026-06-01T18:00:00+00:00",
  "accounts": ["anton"],
  "config_changes": [],
  "plan_changes": [],
  "code_cleanup": [],
  "skill_self_updates": [],
  "verification": [],
  "prepared_message_count": 0,
  "prepared_inbound_reply_count": 0,
  "planned_first_message_count": 0,
  "profile_kpis": {
    "anton": {
      "first_messages_per_cycle": 15,
      "planned_first_messages_next_run": 0,
      "planned_inbound_replies_next_run": 0
    }
  },
  "candidate_replenishment": [],
  "cross_profile_dedup": {
    "checked": true,
    "duplicate_count": 0
  },
  "social_life_changes": [],
  "generated_social_assets": [],
  "community_discovery": [],
  "api_call_ledger": {
    "path": "state/safety/api_call_ledger/latest.json",
    "risk_accounts": ["anton"]
  },
  "account_safety_actions": [
    {
      "account": "anton",
      "action": "hold_writes",
      "reason": "critical heavy-read ledger findings and fresh VK block incident"
    }
  ],
  "skipped_repeat_count": 0,
  "dead_path_notes": [],
  "strongest_next_ideas": [],
  "trust_progression_note": "surface_growth|trust_progression|hold"
}
```
