"""RU/EN/DE/FI/ZH public first-contact copy and three shared destinations."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .runtime_contacts import normalize_locale

LABELS = {
    "ru": ("📢 Следить за DETai", "🌐 Узнать о нас больше", "⚙️ Настроить уведомления"),
    "en": ("📢 Follow DETai", "🌐 Discover DETai", "⚙️ Notification settings"),
    "de": ("📢 DETai folgen", "🌐 DETai kennenlernen", "⚙️ Benachrichtigungen"),
    "fi": ("📢 Seuraa DETaita", "🌐 Tutustu DETaihin", "⚙️ Ilmoitusasetukset"),
    "zh": ("📢 DETai 英语频道", "🌐 了解 DETai", "⚙️ 通知设置"),
}

def welcome_keyboard(locale: str) -> InlineKeyboardMarkup:
    key = normalize_locale(locale)
    channel, website, settings = LABELS[key]
    channel_locale = "en" if key == "zh" else key
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=channel, url=f"https://t.me/detai_{channel_locale}")],
        [InlineKeyboardButton(text=website, url="https://detai-x.com")],
        [InlineKeyboardButton(text=settings, url="https://t.me/detai_hub_bot?start=notifications")],
    ])

WELCOME = {
    "ru": "🌱 <b>Добро пожаловать в DETai!</b>\n\nИногда мы приглашаем новых участников в нашу команду — людей, которым близки исследования, психология, технологии и совместная работа с AI.\n\nПрисоединение к экосистеме — это путь от знакомства с идеями до освоения инструментов и первого вклада.\n\nЕсли тебе интересно когда-нибудь стать частью команды, познакомься с <a href=\"https://detai-x.com/ru/about/onboarding\">процессом онбординга DETai</a>. Это знакомство не означает автоматического зачисления в команду.\n\nА пока можно узнать больше о наших проектах по кнопкам ниже. 💚",
    "en": "🌱 <b>Welcome to DETai!</b>\n\nFrom time to time, we invite new people to join our team — people interested in research, psychology, technology and collaboration with AI.\n\nJoining is a journey from learning about our ideas to making a first contribution.\n\nDiscover <a href=\"https://detai-x.com/ru/about/onboarding\">the DETai onboarding process</a>. Exploring it is not an application or automatic admission. You can also discover our projects below.",
    "de": "🌱 <b>Willkommen bei DETai!</b>\n\nVon Zeit zu Zeit laden wir neue Menschen in unser Team ein, die sich für Forschung, Psychologie, Technologie und Zusammenarbeit mit KI begeistern.\n\nErfahre mehr über den <a href=\"https://detai-x.com/ru/about/onboarding\">DETai-Onboarding-Prozess</a>. Das Kennenlernen bedeutet keine automatische Aufnahme. Unten findest du weitere Projekte.",
    "fi": "🌱 <b>Tervetuloa DETaihin!</b>\n\nAika ajoin kutsumme tiimiimme uusia ihmisiä, joita kiinnostavat tutkimus, psykologia, teknologia ja yhteistyö tekoälyn kanssa.\n\nTutustu <a href=\"https://detai-x.com/ru/about/onboarding\">DETai-onboardingin vaiheisiin</a>. Niihin tutustuminen ei tarkoita automaattista jäsenyyttä. Alta löydät lisää hankkeitamme.",
    "zh": "🌱 <b>欢迎来到 DETai！</b>\n\n我们会不定期邀请对研究、心理学、技术和 AI 协作感兴趣的新成员加入团队。\n\n了解 <a href=\"https://detai-x.com/ru/about/onboarding\">DETai 入门流程</a>，从认识理念到学习工具和初步参与。阅读流程并不代表自动获得团队资格。也欢迎浏览下方的其他项目。",
}
def welcome_copy(locale: str) -> str:
    return WELCOME[normalize_locale(locale)]
