#!/usr/bin/env python3
"""Generate static MiniRef pages with Python standard library. Run: python tools/build.py"""
import json
import html
from pathlib import Path
from urllib.parse import urljoin

BASE = Path(__file__).resolve().parents[1]
CFG = json.loads((BASE / 'settings.json').read_text(encoding='utf-8'))
SITE_URL = CFG['site_url'].strip().rstrip('/')
PHONE, TEL = CFG['phone_display'], CFG['phone_href']

PAGES = {
    '': ('Главная', 'Рефрижераторные перевозки по Москве и области | MiniRef', 'Рефрижераторные перевозки по Москве и МО. Отдельная машина под ваш груз, разовые и регулярные рейсы, доставка в распределительные центры.'),
    'services/': ('Услуги', 'Рефрижераторные перевозки: услуги для бизнеса | MiniRef', 'Виды рефрижераторных перевозок MiniRef: температурные грузы, регулярные поставки, срочные перевозки, работа с распределительными центрами.'),
    'services/refrigerated/': ('Перевозки', 'Рефрижераторные перевозки по Москве и МО | MiniRef', 'Перевозки охлаждённых и замороженных грузов по Москве и области отдельным рефрижератором. Согласование температурного режима и маршрута.'),
    'services/regular/': ('Регулярные рейсы', 'Регулярные рефрижераторные перевозки для компаний | MiniRef', 'Регулярная доставка продуктов и температурных грузов по графику. Рейсы на склады, в магазины и распределительные центры Москвы и МО.'),
    'services/urgent/': ('Срочная доставка', 'Срочный рефрижератор по Москве и области | MiniRef', 'Срочная подача рефрижератора в Москве и МО при наличии свободного автомобиля. Уточните адрес погрузки, время и требования к температуре.'),
    'services/retail/': ('Доставка в РЦ', 'Доставка рефрижератором в распределительные центры | MiniRef', 'Доставка охлаждённой и замороженной продукции на склады и в распределительные центры. Согласование окон и требований к документам.'),
    'fleet/': ('Автопарк', 'Автопарк рефрижераторов для перевозок 1–7 тонн | MiniRef', 'Выбор рефрижератора для доставки по Москве и области. Ориентиры по тоннажности, сценарии использования и подбор машины под груз.'),
    'process/': ('Как работаем', 'Как заказать рефрижераторную перевозку | MiniRef', 'Порядок заказа рефрижератора по Москве и МО: заявка, согласование температурного режима, подача машины, доставка и документы.'),
    'about/': ('О нас', 'О MiniRef — рефрижераторная логистика для бизнеса', 'MiniRef организует рефрижераторные перевозки по Москве и Московской области. Прямой контакт, отдельная машина под рейс, понятные процессы.'),
    'contacts/': ('Контакты', 'Контакты MiniRef — рефрижераторные перевозки Москва', 'Свяжитесь с MiniRef, чтобы обсудить рефрижераторные перевозки по Москве и области, маршрут, температуру, сроки и тип автомобиля.'),
    'privacy/': ('Конфиденциальность', 'Политика конфиденциальности | MiniRef', 'Информация об обработке данных при использовании сайта MiniRef.'),
}

def h(s): return html.escape(str(s), quote=True)
def link(path, root, label, cls='', attrs=''):
    return f'<a href="{root}{path}"{(" class=" + repr(cls)) if cls else ""} {attrs}>{label}</a>'

def header(root, current):
    nav = [('services/', 'Услуги'), ('fleet/', 'Автопарк'), ('process/', 'Как работаем'), ('about/', 'О компании'), ('contacts/', 'Контакты')]
    nav_html = ''.join(f'<a href="{root}{path}" {"aria-current=\"page\"" if current == path or (current.startswith("services/") and path=="services/") else ""}>{label}</a>' for path,label in nav)
    return f'''<header class="site-header"><div class="wrap head-inner">
<a class="wordmark" href="{root}" aria-label="MiniRef — главная">mini<em>ref</em><span class="wordmark__sub">TRANSPORT &amp; COLD</span></a>
<nav class="main-nav" id="main-nav" aria-label="Основное меню">{nav_html}</nav>
<div class="head-contact"><a class="phone" href="tel:{h(TEL)}">{h(PHONE)}</a><a class="head-btn" href="{root}contacts/">Обсудить рейс <span aria-hidden="true">↗</span></a></div>
<button class="menu-toggle" type="button" aria-controls="main-nav" aria-expanded="false" aria-label="Открыть меню" data-menu-toggle><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
</div></header>'''

def footer(root):
    return f'''<footer class="site-footer"><div class="wrap"><div class="footer-grid"><div><a class="wordmark" href="{root}">mini<em>ref</em><span class="wordmark__sub">TRANSPORT &amp; COLD</span></a><p>Рефрижераторные перевозки для бизнеса. Москва и Московская область.</p></div>
<div><h3>Услуги</h3><a href="{root}services/refrigerated/">Температурные грузы</a><a href="{root}services/regular/">Регулярные поставки</a><a href="{root}services/urgent/">Срочные рейсы</a><a href="{root}services/retail/">Доставка в РЦ</a></div>
<div><h3>Компания</h3><a href="{root}fleet/">Автопарк</a><a href="{root}process/">Как работаем</a><a href="{root}about/">О компании</a><a href="{root}contacts/">Контакты</a></div>
<div><h3>Связаться</h3><a href="tel:{h(TEL)}" style="font-size:1.25rem;font-weight:800">{h(PHONE)}</a><p>Москва и Московская область<br>Время подачи — по согласованию</p><a href="{root}contacts/">Обсудить задачу ↗</a></div></div><div class="footer-bottom"><span>© 2026 MiniRef. Рефрижераторные перевозки.</span><a href="{root}privacy/">Политика конфиденциальности</a><span>Сайт без сторонних библиотек и трекеров</span></div></div></footer>'''

def cta(root, headline='Есть маршрут? Подберём машину.'):
    return f'''<section class="cta-banner"><div class="wrap cta-grid"><div><span class="eyebrow eyebrow--light">На связи с логистом</span><h2>{headline}</h2><p>Расскажите, что перевозите, откуда и куда. Согласуем доступный автомобиль и условия рейса.</p></div><a class="button button--primary" href="tel:{h(TEL)}">Позвонить менеджеру <span class="arrow" aria-hidden="true">↗</span></a></div></section>'''

def breadcrumbs(root, items):
    parts = [f'<a href="{root}">Главная</a>']
    for name, path in items[:-1]: parts.append(f'<a href="{root}{path}">{h(name)}</a>')
    parts.append(f'<span aria-current="page">{h(items[-1][0])}</span>')
    return '<nav class="breadcrumbs" aria-label="Хлебные крошки">' + ' <span aria-hidden="true">/</span> '.join(parts) + '</nav>'

def page_hero(root, items, tag, title, lead, pills=()):
    pill_html = ''.join(f'<span class="pill">{h(item)}</span>' for item in pills)
    return f'''<section class="page-hero"><div class="wrap page-hero__inner">{breadcrumbs(root,items)}<span class="eyebrow">{h(tag)}</span><h1>{title}</h1><p>{lead}</p>{f'<div class="pill-row">{pill_html}</div>' if pill_html else ''}</div></section>'''

def faq(faqs):
    return '<div class="faq-list">' + ''.join(f'<details><summary>{h(q)}</summary><p>{a}</p></details>' for q,a in faqs) + '</div>'

def page_html(path, main):
    title, seo_title, desc = PAGES[path]
    depth = 0 if not path else len([p for p in path.split('/') if p]); root = '../' * depth
    canonical = f'{SITE_URL}/{path}' if SITE_URL else ''
    structured = {'@context':'https://schema.org','@type':'Organization','name':'MiniRef','description':'Рефрижераторные перевозки по Москве и Московской области','telephone':TEL,'areaServed':[{'@type':'AdministrativeArea','name':'Москва'},{'@type':'AdministrativeArea','name':'Московская область'}]}
    if SITE_URL: structured['url'] = SITE_URL + '/'
    ld = json.dumps(structured,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    seo_extras = (f'<link rel="canonical" href="{h(canonical)}"><meta property="og:url" content="{h(canonical)}"><meta property="og:image" content="{h(SITE_URL)}/assets/img/og-preview.jpg">' if SITE_URL else '')
    head = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#ffffff"><meta name="color-scheme" content="light"><title>{h(seo_title)}</title><meta name="description" content="{h(desc)}"><meta name="robots" content="index,follow,max-image-preview:large"><meta property="og:type" content="website"><meta property="og:locale" content="ru_RU"><meta property="og:title" content="{h(seo_title)}"><meta property="og:description" content="{h(desc)}">{seo_extras}<link rel="icon" type="image/svg+xml" href="{root}assets/img/logo-mark.svg"><link rel="stylesheet" href="{root}assets/css/styles.css"><script type="application/ld+json">{ld}</script><script src="{root}assets/js/main.js" defer></script></head><body><a class="skip" href="#main">Перейти к содержимому</a>{header(root,path)}<main id="main">'''
    return head + main + '</main>' + footer(root) + '</body></html>'

def homepage():
    root=''
    serv = [
        ('01','Рефрижераторные перевозки','Охлаждённые и замороженные грузы, отдельный автомобиль под задачу.','services/refrigerated/','°C'),
        ('02','Регулярные поставки','Маршруты по графику для магазинов, складов и производителей.','services/regular/','↗'),
        ('03','Срочная подача','Когда рейс нужен вне привычного расписания. По доступности машины.','services/urgent/','24'),
        ('04','Доставка в РЦ и сети','Помогаем согласовать окна, режим и сопроводительные документы.','services/retail/','РЦ'),
    ]
    cards=''
    for n,name,desc,path,symbol in serv:
        cards += f'''<a class="service-card reveal" href="{path}"><span class="service-num">УСЛУГА / {n}</span><div class="service-abstract" aria-hidden="true"><span class="rings"></span><span class="big-symbol">{symbol}</span></div><div class="service-body"><h3>{name}</h3><p>{desc}</p><span class="service-card__link">Подробнее <span aria-hidden="true">↗</span></span></div></a>'''
    fleets = [('1–2 т','Городские доставки','Для небольших партий и маршрутов с несколькими точками.'),('3–5 т','Поставки для бизнеса','Для системных рейсов на склады и к получателям.'),('до 7 т','Объёмные задачи','При большем объёме груза или регулярной загрузке.')]
    fleet_html=''.join(f'''<article class="fleet-card reveal"><div class="fleet-vehicle"><img src="assets/img/hero-truck.svg" width="1280" height="810" loading="lazy" decoding="async" alt="Иллюстрация рефрижераторного автомобиля MiniRef"></div><span class="eyebrow">Рефрижератор</span><h3>{weight}</h3><p>{desc}</p><div class="fleet-card__bottom"><span>{caption}</span><a href="fleet/">Подбор ↗</a></div></article>''' for weight,caption,desc in fleets)
    steps=[('01','Задача','Груз, температурный режим, адреса и желаемое время.'),('02','Согласование','Подбираем машину и обсуждаем условия выполнения.'),('03','Перевозка','Подача, погрузка и рейс по согласованному маршруту.'),('04','Завершение','Выгрузка и передача необходимых документов.')]
    step_html=''.join(f'<article class="step reveal"><strong>{n}</strong><h3>{title}</h3><p>{desc}</p></article>' for n,title,desc in steps)
    return f'''<section class="hero"><div class="wrap hero-layout"><div class="hero-copy"><span class="hero-label">Минимум сложностей. Максимум контроля.</span><h1><span class="hero-long">Рефрижераторные</span> перевозки <span>без лишних звеньев.</span></h1><p class="hero-lead">Москва и Московская область. Выделенная машина под ваш груз: от разовой доставки до регулярных маршрутов по графику.</p><div class="hero-actions"><a class="button button--primary" href="#calculation">Обсудить перевозку <span class="arrow" aria-hidden="true">↗</span></a><a class="button button--outline" href="services/">Наши услуги <span class="arrow" aria-hidden="true">↗</span></a></div><div class="hero-foot"><span>01 / 07 — тонны</span><span>Москва + МО</span><span>Без догруза</span></div></div><div class="hero-art"><img class="hero-truck" src="assets/img/hero-truck.svg" alt="Иллюстрация автомобиля-рефрижератора MiniRef для перевозок в Москве" width="1280" height="810" fetchpriority="high" decoding="async"><div class="floating-stamp"><small>Формат работы</small><strong>1 машина<br>1 клиент</strong></div><span class="hero-rail">MINIREF / LOGISTICS SYSTEM</span></div></div></section>
<div class="signal-band" aria-hidden="true"><div class="signal-track"><span>МОСКВА / МО <i>✳</i> COLD CHAIN / MINIREF <i>✳</i> ПЕРЕВОЗКИ ПОД КОНТРОЛЕМ <i>✳</i>&nbsp;&nbsp;&nbsp;&nbsp;</span><span>МОСКВА / МО <i>✳</i> COLD CHAIN / MINIREF <i>✳</i> ПЕРЕВОЗКИ ПОД КОНТРОЛЕМ <i>✳</i>&nbsp;&nbsp;&nbsp;&nbsp;</span></div></div><section class="proof-bar"><div class="wrap proof-grid"><div class="proof-cell"><span class="proof-symbol" aria-hidden="true">↗</span><div><strong>Москва и область</strong><small>Локальные маршруты</small></div></div><div class="proof-cell"><span class="proof-symbol" aria-hidden="true">◈</span><div><strong>1–7 тонн</strong><small>Подбор под груз</small></div></div><div class="proof-cell"><span class="proof-symbol" aria-hidden="true">◎</span><div><strong>Без догруза</strong><small>Отдельный автомобиль</small></div></div><div class="proof-cell"><span class="proof-symbol" aria-hidden="true">⌁</span><div><strong>Прямой контакт</strong><small>Без лишних согласований</small></div></div></div></section>
<section class="section" id="services"><div class="wrap"><div class="section-heading reveal"><div><span class="eyebrow">Что мы делаем / 01</span><h2>Логистика, которая<br>подстраивается <span class="accent">под вас.</span></h2></div><p>Не заставляем бизнес подстраиваться под абстрактные тарифы. Начинаем с маршрута, товара и режима перевозки.</p></div><div class="service-grid">{cards}</div></div></section>
<section class="statement"><div class="wrap reveal"><span class="statement-label">Принцип MiniRef</span><p>Ваш груз.<br><em>Ваша машина.</em><br>Ваш маршрут.</p></div></section>
<section class="section"><div class="wrap split-grid"><div class="visual-frame reveal"><img src="assets/img/cold-chain.svg" width="760" height="720" loading="lazy" decoding="async" alt="Схема перевозки температурного груза в изотермическом кузове"><span class="frame-tag">COLD CHAIN / 001</span></div><div class="split-copy reveal"><span class="eyebrow">Внимание к условиям / 02</span><h2>Температура — часть задачи, <span class="accent">а не мелочь.</span></h2><p>Перед рейсом уточняем требования к продукции, маршрут и условия погрузки. Подходящий режим и возможность его поддержания согласуются до подачи автомобиля.</p><ul class="checklist"><li>Охлаждённая и замороженная продукция</li><li>Отдельный автомобиль под отправку</li><li>Точки доставки и временные окна</li><li>Документы по требованиям получателя</li></ul><a class="button button--dark" href="services/refrigerated/" style="margin-top:29px">Подробнее о перевозках <span aria-hidden="true">↗</span></a></div></div></section>
<section class="section route-section"><div class="wrap"><div class="section-heading reveal"><div><span class="eyebrow">География / 03</span><h2>Москва рядом.<br><span class="accent">Область — тоже.</span></h2></div><p>От небольших городских рейсов до системных поставок по Московской области.</p></div><div class="route-card reveal"><div class="route-card__map"><img src="assets/img/route-grid.svg" width="1200" height="650" loading="lazy" decoding="async" alt="Стилизованная маршрутная схема Москвы и Московской области"></div><div class="route-card__aside"><div><span class="eyebrow eyebrow--light">Маршруты</span><h3>От склада<br>до точки<br>выгрузки.</h3><p>Работаем с магазинами, складами, производителями и распределительными центрами.</p></div><a class="button button--light" href="contacts/">Обсудить маршрут <span aria-hidden="true">↗</span></a></div></div></div></section>
<section class="section"><div class="wrap"><div class="section-heading reveal"><div><span class="eyebrow">Машины / 04</span><h2>Не больше.<br><span class="accent">Не меньше.</span></h2></div><p>Подбираем класс машины исходя из объёма, массы груза, точек маршрута и условий разгрузки. Иллюстрации заменяются реальными фото автопарка.</p></div><div class="fleet-grid">{fleet_html}</div></div></section>
<section class="section section--mist"><div class="wrap"><div class="section-heading reveal"><div><span class="eyebrow">Сценарий работы / 05</span><h2>От задачи<br>до доставки. <span class="accent">Понятно.</span></h2></div><p>Никаких длинных анкет для первого обращения. Вначале уточняем главное, а детали согласуем с менеджером.</p></div><div class="steps">{step_html}</div><a class="button button--outline" href="process/" style="margin-top:35px">Как мы работаем <span aria-hidden="true">↗</span></a></div></section>
<section class="section calc-section" id="calculation"><div class="wrap calc-layout"><div class="reveal"><span class="eyebrow">Быстрый запрос / 06</span><h2>Параметры рейса <span class="accent">за минуту.</span></h2><p>Это не публичный тарифный калькулятор: стоимость зависит от автомобиля, времени, маршрута и условий. Заполните параметры и обсудите итог с менеджером.</p><p class="small-note">Никаких форм с передачей персональных данных: текст заявки формируется прямо в браузере.</p></div><form class="calc-panel reveal" data-calculator><div class="form-grid"><div class="field"><label for="vehicle">Автомобиль</label><select id="vehicle" name="vehicle"><option value="1–2 т">1–2 тонны</option><option value="3–5 т">3–5 тонн</option><option value="до 7 т">До 7 тонн</option></select></div><div class="field"><label for="hours">Время работы, ч</label><input id="hours" name="hours" type="number" min="1" max="24" step="1" value="4" inputmode="numeric"></div><div class="field"><label for="km">Км за МКАД</label><input id="km" name="km" type="number" min="0" max="500" step="1" value="0" inputmode="numeric"></div><div class="field"><span class="field-label">Регион</span><div class="field-static">Москва и область</div></div></div><label class="checkbox-field"><input type="checkbox" name="night"> Ночной рейс</label><div class="estimate"><strong data-estimate aria-live="polite"></strong><p>Точная стоимость и доступность машины — после согласования. Параметры не отправляются на сервер.</p></div><div class="calc-actions"><button class="button button--primary" type="submit">Скопировать запрос <span aria-hidden="true">↗</span></button><a class="button button--outline" href="tel:{h(TEL)}">Позвонить</a></div><span class="toast" role="status" aria-live="polite" data-toast></span></form></div></section>
<section class="section"><div class="wrap"><div class="section-heading reveal"><div><span class="eyebrow">Ответы / 07</span><h2>Частые <span class="accent">вопросы.</span></h2></div><p>Основные условия лучше согласовать до начала перевозки.</p></div>{faq([('Вы работаете только по Москве?','Выполняем рейсы по Москве и Московской области. Возможность конкретного маршрута уточняйте при обращении.'),('Можно заказать машину на регулярной основе?','Да. Обсудим график, загрузку, точки получения и разгрузки, а также подходящий автомобиль.'),('Можно перевозить замороженные продукты?','Возможность перевозки зависит от требуемого режима и доступного автомобиля. Укажите температуру и характеристики груза заранее.'),('Как узнать стоимость?','Сообщите тип груза, маршрут, время в работе, километраж за МКАД и необходимые дополнительные условия. Менеджер уточнит расчёт.')])}</div></section>
{cta(root)}'''

def services_page():
    root='../'; items=[('Услуги','services/')]
    cards=[('Температурные перевозки','Подбор транспорта для охлаждённых и замороженных грузов.','services/refrigerated/'),('Регулярные маршруты','Плановые поставки по согласованному графику.','services/regular/'),('Срочные рейсы','Подача при наличии свободного автомобиля.','services/urgent/'),('Поставки в РЦ','Маршруты с учётом окон и правил получателя.','services/retail/')]
    cells=''.join(f'<article class="content-block reveal"><h3>{name}</h3><p>{desc}</p><a class="button button--outline" style="margin-top:22px" href="{root}{path}">Подробнее ↗</a></article>' for name,desc,path in cards)
    return page_hero(root,items,'Услуги MiniRef','Перевозки под ваш <span class="accent">бизнес.</span>','От разовой отправки до графика ежедневных поставок. Выбирайте задачу, а не случайный набор опций.',('Москва и МО','Выделенный транспорт','Для юридических лиц'))+f'''<section class="section"><div class="wrap"><div class="section-heading"><div><span class="eyebrow">Направления</span><h2>Четыре задачи.<br>Один понятный процесс.</h2></div><p>Условия конкретной перевозки согласуются по маршруту, характеристикам груза и требованиям к автомобилю.</p></div><div class="rich-grid">{cells}</div></div></section><section class="section section--mist"><div class="wrap split-grid"><div class="split-copy"><span class="eyebrow">Как выбрать</span><h2>Начните с <span class="accent">груза.</span></h2><p>Назовите товар, требуемый температурный режим, вес и объём. Затем — адреса, дату и время. На этой основе подберём формат перевозки.</p><ul class="checklist"><li>Масса и габариты</li><li>Температурные требования</li><li>Количество точек</li><li>Временные окна</li></ul></div><div class="visual-frame"><img src="{root}assets/img/cold-chain.svg" width="760" height="720" loading="lazy" alt="Иллюстрация температурной логистики"></div></div></section>{cta(root)}'''

SERVICE_CONTENT={
'refrigerated':{
 'name':'Рефрижераторные перевозки','title':'Груз в нужном <span class="accent">режиме.</span>','lead':'Рефрижераторные перевозки охлаждённой и замороженной продукции по Москве и Московской области. Отдельный автомобиль под согласованный маршрут.',
 'pills':['Охлаждённые грузы','Заморозка','Москва и МО'],
 'intro':'Температурная доставка начинается до загрузки: важно согласовать режим, тип товара, время пути и условия выгрузки. Мы не обещаем универсальную температуру для любого груза — параметры определяются задачей и возможностями машины.',
 'blocks':[('Что можно перевозить','Продукты питания и другую продукцию, которой требуется согласованный температурный режим. При первом обращении уточняем категорию товара и ограничения.'),('Что важно сообщить','Требуемый диапазон температуры, вес и объём, характер упаковки, точки погрузки и выгрузки, время подачи и особые условия приёмки.'),('Как подбираем автомобиль','Смотрим на грузоподъёмность, объём кузова, наличие подходящего режима и ограничения на маршруте.'),('Что получает клиент','Отдельный автомобиль без догруза, согласованные условия и прямой контакт по исполнению рейса.')],
 'faqs':[('Вы гарантируете любую температуру?','Нет: доступные режимы зависят от конкретной машины и условий рейса. Согласуем требования до подтверждения заказа.'),('Возможна перевозка с несколькими точками выгрузки?','Да, если маршрут и условия согласованы заранее. Важно учесть время открывания кузова и специфику продукции.')]
},
'regular':{
 'name':'Регулярные перевозки','title':'Рейс по графику. <span class="accent">Не по случаю.</span>','lead':'Плановые рефрижераторные перевозки для производителей, поставщиков, торговых точек и складов Москвы и области.',
 'pills':['Регулярные рейсы','График поставок','B2B'],
 'intro':'Когда поставки повторяются, важна не только цена отдельного рейса. Нужны понятная последовательность работы, окна приёмки, согласованные маршруты и возможность заранее планировать загрузку.',
 'blocks':[('Для кого','Производители и дистрибьюторы продуктов, поставщики магазинов, рестораны, кейтеринг и другие компании с повторяющимися отправками.'),('Как строится график','Уточняем частоту, дни, адреса, интервалы разгрузки и характеристики поставок. Далее согласуем условия на период.'),('Что можно менять','При согласовании можно пересматривать точки, загрузку и расписание. Изменения зависят от доступности транспорта.'),('Как начать','Передайте пример одного рейса и планируемую частоту. На их основе обсуждаются подходящий класс автомобиля и организация работы.')],
 'faqs':[('Можно ли закрепить машину на постоянный маршрут?','Обсудим такую схему индивидуально: она зависит от графика и доступности машин.'),('Работаете с несколькими адресами в рамках рейса?','Да, маршрут и количество точек согласуются до перевозки.')]
},
'urgent':{
 'name':'Срочные перевозки','title':'Когда нужно <span class="accent">быстрее.</span>','lead':'Срочная рефрижераторная доставка по Москве и Московской области, если свободная подходящая машина доступна на нужное время.',
 'pills':['По доступности','Прямой контакт','Москва и МО'],
 'intro':'Срочный рейс требует быстрого решения без обещаний, которые невозможно выполнить. Сразу уточняем критичные вводные: откуда забрать груз, когда он готов и какая температура требуется.',
 'blocks':[('Что сообщить сразу','Адрес подачи, желаемое время, характеристики груза, режим и адрес выгрузки.'),('Что проверяем','Доступность подходящей машины, реальность времени подачи и условия маршрута.'),('Когда подтверждаем','Только после согласования автомобиля, маршрута и основных условий выполнения.'),('Как связаться','Для срочного запроса лучше позвонить менеджеру: так быстрее уточнить доступность и детали.')],
 'faqs':[('Есть подача за 30 минут?','Не заявляем фиксированное время без подтверждения: оно зависит от местоположения и доступности машин.'),('Можно заказать ночью?','Ночные рейсы обсуждаются индивидуально, в зависимости от доступности транспорта и условий доставки.')]
},
'retail':{
 'name':'Доставка в распределительные центры','title':'Поставка, которая <span class="accent">доезжает до РЦ.</span>','lead':'Рефрижераторные поставки на склады, в распределительные центры и торговые сети Москвы и Московской области.',
 'pills':['Распределительные центры','Временные окна','Документы'],
 'intro':'Приёмка в РЦ часто связана с отдельными требованиями: временными окнами, пропусками, упаковкой и документами. Эти условия важно учесть до выезда, а не уже перед воротами.',
 'blocks':[('Подготовка к поставке','Собираем информацию о площадке, окне приёмки, необходимых пропусках, условиях въезда и выгрузки.'),('Документы','Уточняем необходимые сопроводительные документы со стороны заказчика и получателя. Перечень согласуется для конкретной поставки.'),('Маршрут','Учитываем время на дорогу, процедуру регистрации и возможные ожидания при приёмке.'),('Повторяющиеся поставки','Для регулярных отгрузок согласуем типовые маршруты и расписание, чтобы снижать количество ручных уточнений.')],
 'faqs':[('Вы возите в торговые сети?','Да, доставка на склады и в распределительные центры — одно из направлений работы. Условия конкретного получателя уточняются перед рейсом.'),('Вы оформляете все документы за отправителя?','Перечень документов и ответственность сторон зависят от договора и характера груза; обсуждаем это до начала работы.')]
}}

def service_page(kind):
    s=SERVICE_CONTENT[kind]; root='../../'
    items=[('Услуги','services/'),(s['name'],f'services/{kind}/')]
    blocks=''.join(f'<article class="content-block reveal"><h3>{name}</h3><p>{text}</p></article>' for name,text in s['blocks'])
    other=''.join(f'<a class="button button--outline" href="{root}services/{key}/">{data["name"]} ↗</a>' for key,data in SERVICE_CONTENT.items() if key!=kind)
    return page_hero(root,items,'Направление MiniRef',s['title'],s['lead'],s['pills']) + f'''<section class="section"><div class="wrap split-grid"><div class="split-copy"><span class="eyebrow">Об услуге</span><h2>Не просто перевозка. <span class="accent">Продуманный рейс.</span></h2><p>{s['intro']}</p><a class="button button--dark" href="{root}contacts/" style="margin-top:20px">Обсудить перевозку ↗</a></div><div class="visual-frame"><img src="{root}assets/img/cold-chain.svg" width="760" height="720" loading="lazy" alt="Фирменная иллюстрация температурной логистики MiniRef"><span class="frame-tag">MINIREF / COLD CHAIN</span></div></div></section><section class="section section--mist"><div class="wrap"><div class="section-heading"><div><span class="eyebrow">Условия работы</span><h2>Сначала детали.<br><span class="accent">Потом рейс.</span></h2></div><p>Параметры услуги согласуются до подачи автомобиля.</p></div><div class="rich-grid">{blocks}</div></div></section><section class="section"><div class="wrap"><div class="section-heading"><div><span class="eyebrow">Вопросы</span><h2>Важно знать заранее.</h2></div></div>{faq(s['faqs'])}<h3 style="margin-top:55px;font-size:1.4rem">Другие направления</h3><div class="pill-row">{other}</div></div></section>{cta(root)}'''

def fleet_page():
    root='../'; items=[('Автопарк','fleet/')]
    return page_hero(root,items,'Машины MiniRef','Ровно столько машины, <span class="accent">сколько нужно.</span>','Выбираем рефрижератор под грузоподъёмность, объём и условия выгрузки. Указанные классы — ориентиры для обсуждения, не технический паспорт конкретного автомобиля.',('1–7 тонн','Подбор по задаче','Отдельный рейс'))+f'''<section class="section"><div class="wrap"><div class="section-heading"><div><span class="eyebrow">Классы машин</span><h2>Под разные объёмы.<br><span class="accent">Один подход.</span></h2></div><p>Точные характеристики и доступность конкретного рефрижератора подтверждает менеджер.</p></div><div class="rich-grid"><article class="content-block"><h3>01 / 1–2 тонны</h3><p>Компактные перевозки небольших партий и городские поставки, когда важны манёвренность и несколько точек доставки.</p></article><article class="content-block"><h3>02 / 3–5 тонн</h3><p>Маршруты поставщиков, складская логистика и регулярные перевозки средних партий.</p></article><article class="content-block"><h3>03 / До 7 тонн</h3><p>Более объёмные отправки, требующие заранее согласовать массу, объём и параметры кузова.</p></article><article class="content-block content-block--blue"><h3>Подбор по задаче</h3><p>Сообщите вес, габариты, упаковку, температурный режим, точки и способ погрузки. Подберём подходящий вариант из доступных.</p><a class="button button--light" href="{root}contacts/" style="margin-top:22px">Связаться ↗</a></article></div><div class="photo-slot" style="margin-top:27px"><span>Место для реальной фотографии автопарка MiniRef</span></div><p class="photo-caption">Заготовка: замените этот блок фотографией собственных автомобилей перед публикацией.</p></div></section>{cta(root)}'''

def process_page():
    root='../'; items=[('Как работаем','process/')]
    steps=[('01','Передаёте задачу','Тип и масса груза, температурный режим, адреса, желаемое время подачи и выгрузки.'),('02','Уточняем условия','Проверяем наличие подходящей машины, маршрут, режим и требования получателя.'),('03','Согласуем рейс','Подтверждаем стоимость, время, автомобиль, документы и другие условия.'),('04','Выполняем доставку','Подача под загрузку, перевозка, прибытие на точку и завершение рейса по согласованным условиям.')]
    cards=''.join(f'<article class="content-block reveal"><span class="eyebrow">Этап {n}</span><h3 style="margin-top:20px">{title}</h3><p>{desc}</p></article>' for n,title,desc in steps)
    return page_hero(root,items,'Процесс','Просто <span class="accent">договориться.</span> Понятно работать.','Порядок работы выстроен вокруг задачи клиента: без лишних этапов до согласования основных параметров.')+f'''<section class="section"><div class="wrap"><div class="rich-grid">{cards}</div><div class="highlight" style="margin-top:30px">Для согласования первого рейса достаточно описания груза, адресов, времени и контакта для обратной связи. Детали по документам обсуждаются отдельно.</div></div></section>{cta(root)}'''

def about_page():
    root='../';items=[('О компании','about/')]
    return page_hero(root,items,'О MiniRef','Не просто машины. <span class="accent">Рабочая логистика.</span>','MiniRef — перевозки температурных грузов по Москве и Московской области с фокусом на задачи поставщиков и бизнеса.',('Москва и область','Отдельный автомобиль','Прямое общение'))+f'''<section class="section"><div class="wrap split-grid"><div class="split-copy"><span class="eyebrow">Наш подход</span><h2>Меньше обещаний.<br><span class="accent">Больше ясности.</span></h2><p>Мы строим взаимодействие вокруг понятного заказа: выделенная машина, согласованные условия, актуальная информация о рейсе и необходимые документы. Условия подтверждаются индивидуально, без универсальных обещаний для любого груза.</p><ul class="checklist"><li>Ориентация на B2B-поставки</li><li>Разовые и регулярные маршруты</li><li>Перевозки без догруза</li><li>Москва и Московская область</li></ul></div><div><div class="photo-slot"><span>Здесь будет реальное фото команды, базы или автомобилей MiniRef</span></div><p class="photo-caption">Добавьте фирменные фотографии для усиления доверия.</p></div></div></section><section class="section section--mist"><div class="wrap"><div class="section-heading"><div><span class="eyebrow">Кому подходим</span><h2>Людям, которым<br><span class="accent">важна доставка.</span></h2></div></div><div class="rich-grid"><div class="content-block"><h3>Поставщикам и производителям</h3><p>Когда важно вовремя довезти товар до торговой точки или склада с учётом режима перевозки.</p></div><div class="content-block"><h3>Логистам и дистрибьюторам</h3><p>Когда нужно закрыть отдельный рейс или согласовать повторяющийся маршрут без цепочки посредников.</p></div></div></div></section>{cta(root)}'''

def contacts_page():
    root='../'; items=[('Контакты','contacts/')]
    return page_hero(root,items,'Связь с MiniRef','Есть груз? <span class="accent">Обсудим.</span>','Позвоните, чтобы уточнить доступность машины, режим, маршрут и условия перевозки по Москве и Московской области.')+f'''<section class="section"><div class="wrap contacts-grid"><div class="contact-tile"><span class="eyebrow">Телефон</span><h2>Обсудить рейс</h2><a class="contact-big" href="tel:{h(TEL)}">{h(PHONE)}</a><p class="small-note">Нажмите на номер для звонка.</p><a class="button button--primary" href="tel:{h(TEL)}">Позвонить ↗</a></div><div class="contact-tile"><span class="eyebrow">География</span><h2>Москва и Московская область</h2><p>Уточните адрес погрузки, пункт назначения, время в работе и километраж за МКАД — это поможет обсудить условия без лишних вопросов.</p><div class="note">Точный режим работы, юридические реквизиты и адрес базы необходимо добавить после подтверждения владельцем.</div></div></div><div class="highlight" style="margin-top:30px">Для быстрой заявки подготовьте: тип груза, массу, температуру, адреса, дату, время и требования получателя.</div></div></section>{cta(root,'Задача понятна? Начнём с разговора.') }'''

def privacy_page():
    root='../';items=[('Политика конфиденциальности','privacy/')]
    return page_hero(root,items,'Информация','Конфиденциальность.','Минимум обработки данных на статическом сайте MiniRef.')+f'''<section class="section"><div class="wrap" style="max-width:850px"><h2>О данных на сайте</h2><p>В текущей статической версии сайт не содержит форм отправки персональных данных на сервер, аналитических пикселей, внешних шрифтов и рекламных трекеров. Параметры рейса в калькуляторе обрабатываются локально в браузере; при нажатии «Скопировать запрос» данные копируются в буфер обмена пользователя.</p><p>При звонке по номеру телефона взаимодействие происходит через телефонную сеть. Возможность обработки сведений в рамках обращения определяется условиями связи с компанией.</p><h2 style="margin-top:44px">Данные оператора</h2><p>Полные сведения об операторе, юридические реквизиты и применимые правила обработки обращений должны быть уточнены перед размещением на рабочем домене. Эта страница не является завершённой юридической политикой для сайта с аналитикой или онлайн-формами.</p><a class="button button--outline" href="{root}contacts/">Контакты ↗</a></div></section>'''

def main():
    bodies={'':homepage(), 'services/':services_page(), 'fleet/':fleet_page(), 'process/':process_page(), 'about/':about_page(), 'contacts/':contacts_page(), 'privacy/':privacy_page()}
    for kind in SERVICE_CONTENT: bodies[f'services/{kind}/']=service_page(kind)
    for path, body in bodies.items():
        dest = BASE / path / 'index.html'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page_html(path, body),encoding='utf-8')
        print('wrote', dest.relative_to(BASE))
    (BASE / 'robots.txt').write_text('User-agent: *\nAllow: /\n' + (f'Sitemap: {SITE_URL}/sitemap.xml\n' if SITE_URL else ''), encoding='utf-8')
    if SITE_URL:
        from xml.sax.saxutils import escape
        urls=''.join(f'<url><loc>{escape(SITE_URL + "/" + path)}</loc></url>' for path in PAGES)
        (BASE/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+urls+'</urlset>',encoding='utf-8')
    else:
        (BASE/'sitemap.xml').unlink(missing_ok=True)

if __name__=='__main__': main()
