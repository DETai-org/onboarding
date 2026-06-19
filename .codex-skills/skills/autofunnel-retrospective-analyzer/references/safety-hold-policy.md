# Safety Hold Policy

Full API hold is required when account state or fresh VK errors indicate:

- auth failed;
- user is blocked;
- checkpoint or suspicious login;
- `api_status` contains `blocked`, `auth`, `checkpoint`, or `hold`;
- `friends_add_status = "auth_block_hold"`.

For a full-hold profile:

- do not create VK clients;
- do not make read-only VK API calls;
- set friend source, message, inbound reply and social-life plan caps to `0`;
- update TOML/account plan with reason and date;
- keep only local state analysis, tests, docs, and director history.

`friends_add_status = "restricted_unknown_method"` is not a full API hold. It only
disables `friends.add`; low-volume fallback may continue if `api_status` is healthy
and the plan allows it.

