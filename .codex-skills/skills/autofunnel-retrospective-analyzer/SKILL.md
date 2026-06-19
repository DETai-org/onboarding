---
name: autofunnel-retrospective-analyzer
description: "Используй после завершенного VK Auto Funnel API-only цикла, когда нужно выступить директором следующего запуска и self-improving maintainer: разобрать свежий runner/state/history/API-call ledger, управлять per-profile KPI/пейсингом, определить сколько unread inbound dialogues отвечать, готовить заранее написанные сообщения и social_life_actions в api_direct_plan.json, планировать редкую социальную жизнь профиля как источник естественных поводов для общения, использовать обычный web/internet research для поиска релевантных VK-сообществ и публичных тем, выбирать friend sources и candidate-list refill через VK/OpenAI qualification helper, проверять cross-profile dedup, чистить код/docs/tests, улучшать собственные инструкции skill и фиксировать change log без browser-runtime/warming/story/runtime generation."
---

# Autofunnel API Director And Self-Improving Maintainer

Версия навыка: `3.5`

## Canonical References

Перед ежедневной automation-ретроспективой сначала читай project runbook:

- `VK/auto_funnel/docs/operations/daily-cycle.md`
- `VK/auto_funnel/state/operations/daily_cycle_context.json`

Локальные reference-файлы skill дополняют runbook и не должны расходиться с ним:

- [references/api-direct-plan-schema.md](references/api-direct-plan-schema.md)
- [references/daily-cycle-contract.md](references/daily-cycle-contract.md)
- [references/inbound-handoff.md](references/inbound-handoff.md)
- [references/safety-hold-policy.md](references/safety-hold-policy.md)

Если длинная инструкция ниже конфликтует с project runbook по operational order,
active accounts, account hold или inbound handoff, приоритет у project runbook.

## Назначение

Используй skill только после завершенного запуска `VK/auto_funnel` в режиме `friend_execution.method = "api_direct"`.

Главная роль skill теперь не старая ретроспектива, а управление следующей итерацией и оздоровление самого контура:

- изучить свежий цикл, состояние аккаунтов, историю действий и переписок;
- прочитать daily API-call ledger и safety incidents, чтобы не повторять паттерны блокировки аккаунтов;
- подготовить следующий per-account план `state/accounts/<account>/api_direct_plan.json`;
- определить для каждого профиля `15` first messages за месячный цикл как отдельный KPI;
- определить, сколько входящих непрочитанных диалогов отвечать в следующем запуске, и подготовить тексты ответов;
- определить, сколько людей добавлять в друзья каждому профилю и из каких источников;
- пополнить candidate lists, если доступных ID мало;
- не допустить, чтобы два профиля писали одному и тому же контакту;
- поддерживать “социальную жизнь” профиля не ради активности, а ради внимания и естественных поводов для общения: редкие собственные посты, репосты, вступления в релевантные сообщества, комментарии, проверка откликов на свои посты/комментарии и превращение этих откликов в кандидатов для диалога;
- изменить только безопасные параметры API-only pipeline, если это нужно для следующего запуска;
- заранее написать тексты сообщений для runner-а;
- убрать обнаруженный мертвый код, документацию или тестовые ожидания, если они тянут pipeline назад;
- улучшить собственный skill, если повторяющаяся ошибка возникла из-за неполной инструкции;
- записать, что изменено и почему, в историю директора.

Runner не генерирует сообщения через LLM. Если текст не подготовлен в plan, runner его не отправляет.

## Automation Self-Improvement Contract

Когда этот skill вызывается из ежедневной automation, считай это не разовой аналитикой, а обязанностью поддерживать и улучшать весь operational contour проекта.

Это означает:

- skill должен не только анализировать свежий цикл, но и при необходимости менять сам проект;
- если цель цикла упирается в баг, недостающий step, слабый prompt, неверный config, нестыковку state, alias mismatch, stale docs, missing test или dead-path residue, skill должен сам это исправлять в рамках текущего workspace;
- допустимо менять код, конфиги, тесты, prompts, docs, plan schema, state-handling helpers, операторские сводки и сам `SKILL.md`, если это реально улучшает следующий запуск;
- если нужного capability ещё нет, skill не должен просто констатировать это как мысль: по умолчанию он должен либо внедрить capability, либо зафиксировать очень конкретный blocked note с минимальным следующим engineering step;
- после существенных правок skill должен заново прогонять релевантные tests/validators и, если нужно, повторять affected pipeline step, а не оставлять проект в полулечённом состоянии.

Иными словами: daily automation должна вести себя как self-healing / self-improving operational loop, а не как пассивный отчёт.

## Inbound Reply Handoff Contract

Для ответов на новые входящие сообщения придерживайся явного двухфазного контура, а не "live LLM inside runner":

1. Runner/collector phase:

- через VK API найти ограниченное число новых unread/inbound dialogues на профиль;
- взять только малый объём по умолчанию, например `1` диалог на активный профиль за запуск, если нет явной причины расширять;
- подтянуть полную историю конкретного диалога;
- синхронно сохранить её в правильный `Chat_history/<user_id>.jsonl`;
- обновить `dialog_index.json` и связанный state так, чтобы стало видно: для этого контакта нужен ответ;
- не отправлять reply, пока reply ещё не подготовлен.

2. Director/orchestrator phase:

- прочитать обновлённую историю;
- подготовить осмысленный `inbound_reply` в `api_direct_plan.json` или эквивалентный per-account reply queue;
- reply должен опираться на реальный контекст истории и persona аккаунта;
- reply не должен записываться в историю как уже отправленный.

3. Runner/send phase:

- runner читает уже подготовленный reply;
- отправляет его через `messages.send`;
- после отправки снова делает `messages.getHistory`;
- пересохраняет локальную историю;
- снимает флаг `reply_needed` / переводит контакт в состояние `reply_sent`.

Если такого handoff-контура в проекте ещё нет или он неполный, daily automation должна считать его допустимой задачей self-improvement и постепенно достраивать именно этот path.

## Активный Контур

Рабочий pipeline:

1. `friends.add` для новых кандидатов из рекомендаций или списков.
2. `likes.add(type=photo)` для аватарки в тот же цикл, если контакт только добавлен.
3. Опционально `wall.get` + `likes.add(type=post)` для выбранного поста.
4. Опционально `wall.getComments` + `likes.add(type=comment)`, только если это явно включено и выглядит уместно.
5. `messages.send` только по заранее подготовленным сообщениям из `api_direct_plan.json`.
6. `messages.getHistory` после отправки, чтобы локальная история не отставала от VK.

Не возвращай browser-runtime, `codex_iab`, stories, story views, story likes, warming-route слой или runtime LLM-generation в активный path.

Для discovery используй обычный web/internet research: поиск по интернету, публичные страницы VK, упоминания групп в статьях, каталогах, постах и других открытых источниках. Browser можно использовать только как дополнительную поверхность просмотра публичных страниц, но не как обязательный рантайм и не как способ управлять аккаунтом, кликать от лица профиля или обходить VK API.

## Обязательный Workflow

1. Восстанови свежий цикл.

Читай:

- `VK/auto_funnel/state/runner/runner_state.json`;
- свежую строку `VK/auto_funnel/state/runner/history.jsonl`;
- `VK/auto_funnel/state/accounts/<account>/stats.json`;
- `VK/auto_funnel/state/accounts/<account>/activity/Chat_history/*.jsonl`;
- `VK/auto_funnel/state/accounts/<account>/activity/events.jsonl`;
- текущий `VK/auto_funnel/state/accounts/<account>/api_direct_plan.json`, если есть;
- `VK/auto_funnel/auto_funnel_config.toml`;
- `VK/auto_funnel/profiles/api_direct_profiles.toml`;
- `VK/auto_funnel/pressure_curve_plan.toml`;
- `VK/auto_funnel/state/social_life/community_discovery/*.json`;
- `VK/auto_funnel/assets/generated_social/`;
- `VK/auto_funnel/state/safety/api_call_ledger/latest.json`;
- `VK/auto_funnel/docs/incidents/*.md`;
- цель из `VK/auto_funnel/README.md`.

Если `state/safety/api_call_ledger/latest.json` отсутствует, сначала построй его из audit:

```text
python -m VK.auto_funnel.scripts.build_api_call_ledger
```

Считай ledger обязательным safety input, а не необязательной аналитикой. Он показывает по дням и профилям `read/write`, `heavy/light`, `started/completed/failed`, risk findings и repeated heavy calls вроде `friends.get`.

Перед любым увеличением pacing проверь:

- нет ли у профиля `risk.level=warning|critical`;
- нет ли repeated `friends.get`, `friends.getSuggestions`, `wall.get`, `messages.getHistory` в короткий период;
- нет ли write-volume warning;
- нет ли incident note про свежую блокировку, checkpoint, подозрительный вход или предупреждение VK.

Если профиль имеет свежий VK block/checkpoint/auth warning или `critical` ledger findings:

- переведи профиль в hold для write actions минимум на следующий запуск;
- отключи friend adds, messages, likes и social-life writes для этого профиля;
- разрешай только минимальные local reads/state analysis, если они не требуют VK API;
- зафиксируй причину в `api_direct_plan.json` strategy/risk notes и в change log.

Если есть `warning`, но не `critical`:

- снизь дневные лимиты профиля;
- избегай full snapshot refresh и повторного `friends.get`;
- не компенсируй нехватку данных серией heavy reads;
- prefer уже сохраненное state/history и малые targeted reads вместо широких refresh.

2. Для каждого активного профиля оцени состояние контактов.

Разделяй:

- новые friend requests;
- принятые друзья без сообщения;
- контакты с первым сообщением, но без ответа;
- контакты с ответом;
- входящие диалоги, где последнее содержательное сообщение от контакта и нужен ответ;
- контакты, где лучше hold;
- повторы действий, которые уже были в plan/history.

Для unread/inbound:

- читай `dialog_index.json` и конкретный `Chat_history/<user_id>.jsonl`;
- считай кандидатом на inbound reply диалог, где есть входящие сообщения и нет более свежего нашего исходящего ответа;
- если таких диалогов больше лимита профиля, выбери мягкий поднабор по приоритету: свежесть, человеческая уместность, риск повторов, неагрессивный общий объем;
- `kind` ставь `inbound_reply` или `reply_to_inbound`;
- `counts_toward_kpi=false`, потому что это не входит в 15 first messages.

3. Сформируй следующий `api_direct_plan.json` для каждого профиля.

Используй схему из [references/api-direct-plan-schema.md](references/api-direct-plan-schema.md).

План обязан содержать:

- `plan_id`;
- `prepared_at`;
- `account`;
- `strategy`;
- `targets`;
- `messages` или `target.message`;
- явные `enabled`, `not_before`, `kind`, `text`, `reason` для сообщений.
- `strategy.kpi.first_messages_per_cycle=15`;
- `strategy.pacing.max_first_messages_per_run`;
- `strategy.pacing.max_inbound_replies_per_run`;
- `strategy.pacing.max_messages_per_run`;
- `strategy.pacing.friend_requests.recommendations`;
- `strategy.pacing.friend_requests.lists`;
- `strategy.source_allocation` с list health/refill решением.
- `strategy.social_life` с low-frequency pacing, если планируются social-life действия;
- `social_life_actions`, если нужен пост, репост, вступление, комментарий или follow-up по комментарию.

Если текст не готов, ставь `enabled=false` и пустой `text`.

Перед сохранением планов проверь cross-profile dedup:

```text
python -m VK.auto_funnel.scripts.validate_api_direct_plans --accounts-root D:\dev\DETai-org\VK\VK\auto_funnel\state\accounts
```

Если проверка находит один `user_id` в enabled unsent messages нескольких профилей, перераспредели контакт и повтори проверку. Один контакт может принадлежать только одному профилю.

4. Варьируй действия без хаоса.

Разрешенные рычаги:

- лимиты `friends_per_day`, `friends_from_list_per_day`, `max_actions_per_account`, `max_messages_per_account`;
- `avatar_like_on_friend_request`;
- `wall_likes_per_new_friend`;
- `wall_post_scan_count`;
- per-target действия `like_avatar`, `like_wall_post`, `like_wall_comment`;
- `not_before` и очередность сообщений;
- перенос контакта в hold.
- редкий `wall_post` с подготовленным текстом и опциональным `image_path`;
- редкий `community_repost` только из релевантного источника;
- редкий `join_group` только после проверки тематики/стены;
- редкий `community_comment` только с конкретным текстом по теме поста;
- `inspect_comment_engagement` через 1-3 дня после комментария, чтобы найти лайкнувших/ответивших и, при уместности, добавить их в друзья.
- периодический осмотр собственных постов профиля через API-read: есть ли новые лайки, комментарии или ответы, которые дают естественный повод для friend request, inbound-style reply или мягкого первого сообщения.

Не меняй токены, глобальные аккаунты, ClickUp, Telegram credentials или unrelated код.

5. Управляй source lists и replenishment.

Проверь, достаточно ли ID в назначенных списках:

- низкий watermark по умолчанию: `20` доступных ID на профиль;
- целевой refill после пополнения: `80` ID;
- если список ниже watermark, запусти candidate builder перед финальным plan:

```text
python -m VK.auto_funnel.scripts.collect_friend_candidates <vk_group_or_post_url> --account <collector_alias> --mode mixed --output VK/auto_funnel/presets/generated/<slug>.txt
```

Правила refill:

- выбирай источник VK по смыслу профиля и прошлым результатам, а не всегда один и тот же;
- чередуй `collector_alias` между профилями с токенами, чтобы один профиль не выглядел агрессивно;
- OpenAI qualification в `collect_friend_candidates.py` допустим только как offline/helper отбор кандидатов, не как runtime message generation;
- после refill обнови/назначь список так, чтобы кандидаты не пересекались между профилями;
- если OPENAI key/runtime недоступен, сохраняй это как operational note и используй raw shortlist только если профильные фильтры всё равно безопасны.

6. Управляй social-life repertoire.

Social life нужна для trust progression: она должна создавать более естественные причины для знакомства, чем холодное сообщение незнакомому человеку. Оценивай каждое действие вопросом: “появится ли после этого легальный, человечески объяснимый повод написать или добавить человека?”

Профиль должен выглядеть живым, но не интенсивным:

- максимум 1 social-life action на профиль за запуск по умолчанию;
- максимум 1 собственный wall post в неделю;
- максимум 1 community comment в неделю, если нет сильной причины;
- не совмещай в один день агрессивный friend-add объем и много публичных действий;
- не комментируй шаблонно и не повторяй одинаковые формулировки между профилями.
- если social-life действие не создаёт новых контактов, контекста или trust-signal, лучше его не делать.

Собственные wall posts:

- сам придумай текст поста, если он уместен текущему профилю и циклу;
- если нужен визуал, сгенерируй изображение доступным image tool и сохрани в `VK/auto_funnel/assets/generated_social/`;
- в `social_life_actions` укажи `type=wall_post`, `text`, `image_path`, `not_before`, `reason`;
- не публикуй чаще лимитов, даже если есть много идей.

Сообщества и комментарии:

- для поиска актуальных групп сначала используй обычный internet/web research: web search по VK-сообществам, тематическим подборкам, публичным страницам, статьям, постам и обсуждениям вокруг психологии/ИИ;
- Browser допустим только как вспомогательный просмотр публичной страницы, если web/search результат надо визуально проверить; не превращай его в управление аккаунтом;
- сохрани найденные URL/screen names в seed file или сразу используй:

```text
python -m VK.auto_funnel.scripts.discover_social_communities --account <collector_alias> --query "психология" --query "искусственный интеллект" --seed-file <research_seeds.txt>
```

- добавляй `--include-subscriptions`, когда хочешь оценить уже подписанные сообщества профиля для репоста или мягкого комментария;
- оцени discovery JSON: тематика, открыта ли стена, есть ли свежие посты, не выглядит ли группа мусорной;
- планируй `join_group`, `community_repost` или `community_comment` только если действие добавляет смысл профилю;
- после `community_comment` запланируй будущий `inspect_comment_engagement` с `auto_friend_add=true` и малым `max_friend_adds`, чтобы добавить тех, кто реально отреагировал на комментарий.

Собственные посты как источник контактов:

- регулярно, но не каждый запуск, проверяй последние собственные wall posts профиля через API-read;
- если под своим постом появились комментарии, готовь короткие уместные ответы и планируй их как social-life/action или message-план, если pipeline уже поддерживает такой тип действия;
- если появились лайки от людей, которых ещё нет в друзьях, рассматривай их как более тёплых кандидатов, чем холодный список: можно добавить в друзья и, если контекст сильный, подготовить мягкое первое сообщение со ссылкой на повод;
- не пиши всем лайкнувшим подряд: выбирай малый поднабор по релевантности профиля, свежести реакции и общему pacing профиля;
- если текущий runner ещё не умеет нужный action type для собственного post engagement, не имитируй действие вручную и не добавляй новый скрипт на ходу; зафиксируй self-improvement/code task или аккуратно расширь существующий API-only pipeline в отдельной инженерной правке с тестами.

Skill может выполнять дополнительные social-life действия после завершенного pipeline, если они уже безопасно подготовлены в plan и не ломают pacing. Не добавляй новые вспомогательные скрипты ради очередной идеи social-life: сначала используй существующий API-only pipeline, plan/state и инструкции skill; если capability реально отсутствует, фиксируй self-improvement/code task или расширяй существующий модуль с тестами, а не плодить отдельный runtime.

7. Проведи dead-path и self-improvement audit.

Сначала запусти быстрый скан:

```text
python C:\Users\PC\.codex\skills\autofunnel-retrospective-analyzer\scripts\scan_api_direct_dead_paths.py --project-root D:\dev\DETai-org\VK\VK\auto_funnel
```

Если скан находит активные ссылки на запрещенные контуры:

- исправь код/docs/tests, если это безопасно и локально проверяемо;
- не удаляй исторические state/log данные без явного запроса;
- после исправления повтори скан и профильные тесты;
- если найденная проблема вызвана слабой инструкцией skill, обнови `SKILL.md` или reference; helper script меняй только когда уже существующий deterministic helper реально требует правки.

Skill может улучшать сам себя, но только как версионируемую инженерную правку:

- меняй skill, если это снижает вероятность повторной ошибки;
- не стирай историю change log;
- не добавляй расплывчатые правила без проверяемого поведения;
- после self-update запускай `quick_validate.py` для skill.

8. Запиши историю директора.

После изменений создай JSON payload и запусти:

```text
python C:\Users\PC\.codex\skills\autofunnel-retrospective-analyzer\scripts\record_api_direct_change.py --project-root D:\dev\DETai-org\VK\VK\auto_funnel --payload <payload.json>
```

Payload должен содержать минимум:

- `cycle_id`;
- `based_on_run_id`;
- `changed_at`;
- `accounts`;
- `config_changes`;
- `plan_changes`;
- `code_cleanup`;
- `skill_self_updates`;
- `verification`;
- `prepared_message_count`;
- `prepared_inbound_reply_count`;
- `planned_first_message_count`;
- `profile_kpis`;
- `candidate_replenishment`;
- `cross_profile_dedup`;
- `social_life_changes`;
- `generated_social_assets`;
- `community_discovery`;
- `api_call_ledger`;
- `account_safety_actions`;
- `skipped_repeat_count`;
- `dead_path_notes`;
- `strongest_next_ideas`;
- `trust_progression_note`.

Скрипт пишет в:

```text
VK/auto_funnel/state/continuous_improvement/autofunnel-api-director/changes/YYYY-MM-DD.jsonl
VK/auto_funnel/state/continuous_improvement/autofunnel-api-director/latest.json
```

## Как Думать О Progress

Считай цикл ближе к `trust-contact list`, если вырос хотя бы один слой:

- больше accepted friends, которым можно писать;
- появились уместные first-message candidates с готовым текстом;
- отправлены подготовленные сообщения без повтора;
- получены ответы;
- появились активные диалоги;
- входящие ответы обработаны без перегруза профиля;
- профиль сделал редкое, уместное публичное действие, которое может привлечь релевантных людей;
- появились отклики на комментарии/посты, которые можно превратить в friend candidates;
- следующий plan стал точнее за счет истории, а не просто поменял числа.

Если цикл только добавил друзей и лайкнул аватарки, фиксируй это как `surface_growth`, но не называй полноценным trust progression.

## Dead-Path Cleanup

Если видишь остатки старого browser/warming/story/runtime-AI-generation контура:

- убирай из активного config и docs сразу, если безопасно;
- не удаляй большие исторические state-данные без явного запроса;
- если удаление требует отдельной миграции, добавь запись в `dead_path_notes` и предложи минимальный следующий cleanup.

Запрещенные активные признаки:

- imports/packages/files вроде `browser_runtime`, `warming`, `dialogue` как runtime path;
- scripts для delegated browser jobs или sync browser results;
- config keys `browser_runtime`, `friend_warming`, `web_warming`;
- runtime statuses `awaiting_browser_runtime`;
- story-specific VK API или action types;
- OpenAI dialogue/follow-up generation внутри runner.

Разрешенные остатки:

- слово `history` в смысле истории переписки или runner history;
- candidate qualification через отдельный offline/helper контур, если runner не вызывает его для генерации сообщений;
- prompt `codex_dialogue_agent_system.txt` как инструкция для skill-директора, а не runtime prompt.

## Verification Contract

После изменений обязательно:

- запусти dead-path scan;
- запусти релевантные тесты, а при массовой чистке весь `VK/auto_funnel/tests`;
- если менялся skill, запусти `python C:\Users\PC\.codex\skills\.system\skill-creator\scripts\quick_validate.py C:\Users\PC\.codex\skills\autofunnel-retrospective-analyzer`;
- запиши результаты в `verification` payload.

## Финальная Сводка

Сообщай коротко:

- какой свежий run_id разобран;
- какие профили обновлены;
- сколько сообщений подготовлено;
- сколько повторов пропущено;
- какие параметры изменены;
- какие 1-3 идеи самые сильные;
- есть ли реальные признаки роста trust-contact progression или это только surface growth.
