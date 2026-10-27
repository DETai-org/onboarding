# DETai Onboarding — reserved Telegram welcome

`@DETonboardingBot` is a small independent presentation bot, **not** the onboarding team's tutorial progression system. The bot responds to a private `/start` in RU/EN/DE/FI/ZH. Its greeting explains that new members are invited from time to time, and links directly to the public [onboarding page](https://detai-x.com/ru/about/onboarding) in the caption. Three additional inline links lead to the language-specific Telegram channel (ZH → EN), the DETai home page and user-managed notification settings in Hub.

Run using `python3 -m bot` from repository root, with `DETAI_ONBOARDING_BOT_TOKEN` and unique `ECOSYSTEM_NOTIFICATIONS_TOKEN` (bound to `detai-onboarding` in Runtime); `ECOSYSTEM_NOTIFICATIONS_URL` targets the verified central API. Secrets are managed outside Git, in `/home/psy-ru/DETai-org/server-operations/detai-onboarding.env`. See `bot/.env.example`. Unit template: `deploy/linux/systemd/detai-onboarding-bot.service`.

The Runtime [#72](https://github.com/DETai-org/ecosystem-runtime/pull/72) first-start API stores contacts/idempotent `bot_started`, and [Arhivarius #14](https://github.com/DETai-org/arhivarius/pull/14) reports results. A `/start` is not a news subscription. This service has no separate DB, onboarding application form or implicit membership grants. Do not enable without a verified Telegram bot token and correct Runtime sender identity.

Optional welcome illustration: `bot/assets/welcome.png`; the default text with buttons works without an image.
