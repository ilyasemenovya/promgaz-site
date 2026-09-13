from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
GASES = json.loads((ROOT / "content/catalog.json").read_text())
CATEGORIES = json.loads((ROOT / "content/categories.json").read_text())
DIST.mkdir(exist_ok=True)
(DIST / "gases").mkdir(exist_ok=True)
(DIST / "assets").mkdir(exist_ok=True)

ARROW = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
OUT = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PHONE = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M8 3H4a1 1 0 0 0-1 1c0 9.4 7.6 17 17 17a1 1 0 0 0 1-1v-4l-5-2-2 2c-3-1.5-4.5-3-6-6l2-2-2-5Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
MAP = "https://yandex.ru/maps/org/promgaz/86533777501/"
EMAIL = "Promgaz21@yandex.ru"

def head(title, description, prefix):
    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <meta name="theme-color" content="#164ca8">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="ru_RU">
  <link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{prefix}assets/styles.css?v=8">
  <script src="{prefix}assets/site.js?v=6" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Перейти к содержимому</a>'''

def header(prefix):
    home = prefix + "index.html"
    return f'''
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{home}" aria-label="ПРОМГАЗ — главная">
      <img class="brand-logo" src="{prefix}assets/brand/promgaz-logo-soft.svg" alt="ПРОМГАЗ — технические газы" width="1486" height="290">
    </a>
    <nav class="desktop-nav" aria-label="Основная навигация">
      <a href="{home}#catalog">Каталог</a>
      <a href="{home}#services">Услуги</a>
      <a href="{home}#company">О компании</a>
      <a href="{home}#contacts">Контакты</a>
    </nav>
    <button class="menu-toggle" type="button" aria-label="Открыть меню" aria-expanded="false" aria-controls="mobile-nav">
      <span></span><span></span>
    </button>
  </div>
  <nav id="mobile-nav" class="mobile-nav" aria-label="Мобильная навигация" hidden>
    <a href="{home}#catalog">Каталог</a>
    <a href="{home}#services">Услуги</a>
    <a href="{home}#company">О компании</a>
    <a href="{home}#contacts">Контакты</a>
  </nav>
</header>'''

def order_dialog(selected=""):
    options = ""
    for category in CATEGORIES:
        positions = GASES if category["id"] == "industrial" else category["items"]
        options += f'<optgroup label="{escape(category["name"])}">'
        options += "".join(f'<option value="{escape(g["name"])}"{" selected" if g["name"] == selected else ""}>{escape(g["name"])}</option>' for g in positions)
        options += '</optgroup>'
    return f'''
<dialog class="order-dialog" id="order-dialog" aria-labelledby="order-title">
  <div class="dialog-top"><span class="eyebrow">ЗАПРОС СТОИМОСТИ</span>
    <button type="button" class="close-dialog" aria-label="Закрыть окно"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m6 6 12 12M6 18 18 6" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg></button>
  </div>
  <h2 id="order-title">Что вам нужно?</h2>
  <p class="dialog-intro">Укажите состав заказа. Подготовим письмо в отдел продаж.</p>
  <form id="order-form">
    <label for="order-gas">Продукция или услуга</label>
    <select id="order-gas" name="gas"><option value="">Выберите позицию</option>{options}<option value="Другая продукция или услуга">Другая продукция или услуга</option></select>
    <label for="order-quantity">Количество и объём</label>
    <input id="order-quantity" name="quantity" placeholder="Например, 2 баллона по 40 л" maxlength="150">
    <label for="order-comment">Пожелания к заказу</label>
    <textarea id="order-comment" name="comment" rows="3" placeholder="Марка, наличие своих баллонов, адрес доставки…" maxlength="1500"></textarea>
    <button class="button button-blue button-full" type="submit">Открыть письмо</button>
    <p class="form-note">Откроется ваша почтовая программа. Отправьте письмо, чтобы отдел продаж получил запрос.</p>
    <p id="email-feedback" class="email-feedback" role="status" hidden>Письмо подготовлено. Если почтовая программа не открылась, напишите на <a href="mailto:{EMAIL}">{EMAIL}</a> или позвоните.</p>
  </form>
</dialog>'''

def footer(prefix):
    return f'''
<footer class="site-footer">
  <div class="container footer-main">
    <a class="brand brand-footer" href="{prefix}index.html" aria-label="ПРОМГАЗ — главная"><img class="brand-logo" src="{prefix}assets/brand/promgaz-logo-soft.svg" alt="ПРОМГАЗ — технические газы" width="1486" height="290" loading="lazy"></a>
    <p>Чебоксары<br>Хозяйственный проезд, 19В</p>
    <div class="footer-links"><a href="{prefix}index.html#contacts">Контакты и схема проезда</a><a href="{prefix}index.html#catalog">Каталог продукции</a></div>
  </div>
  <div class="container footer-bottom"><span>© ПРОМГАЗ, 2026</span><span>ИП Сусарина А. В. · ИНН 212900123770</span></div>
</footer>
<div class="mobile-contact-bar"><button type="button" data-order>Рассчитать заказ</button></div>'''

def card(g, prefix=""):
    return f'''<article class="gas-card"><a class="product-link" href="{prefix}gases/{g['id']}.html"><div class="catalog-photo"><img src="{prefix}assets/products/{g['id']}-new.jpg" alt="{escape(g['name'])} — изображение продукции" width="360" height="360" loading="lazy"></div><div class="card-copy"><h3>{escape(g['name'])}</h3></div></a><div class="card-order"><a href="{prefix}gases/{g['id']}.html">Подробнее</a><button type="button" data-order="{escape(g['name'])}">Узнать цену</button></div></article>'''

def catalog():
    tabs = "".join(f'<a class="catalog-tab" id="tab-{category["id"]}" href="#catalog-{category["id"]}">{escape(category["name"])}</a>' for category in CATEGORIES)
    panels = []
    for category in CATEGORIES:
        if category["id"] == "industrial":
            products = '<div class="catalog-grid">' + "".join(card(g) for g in GASES) + '</div>'
        else:
            products = '<div class="category-products">' + "".join(
                f'<article class="category-product"><div><h3>{escape(item["name"])}</h3><p>{escape(item["description"])}</p></div><button type="button" data-order="{escape(item["name"])}" aria-label="Запросить стоимость: {escape(item["name"])}">Запросить стоимость</button></article>'
                for item in category["items"]
            ) + '</div>'
        panels.append(f'<div class="catalog-panel" id="catalog-{category["id"]}" aria-labelledby="tab-{category["id"]}"><p class="category-description">{escape(category["description"])}</p>{products}</div>')
    return f'<nav class="catalog-tabs" aria-label="Разделы каталога">{tabs}</nav>' + "".join(panels)


home = head("ПРОМГАЗ — технические газы в Чебоксарах", "Продажа технических газов в Чебоксарах. ПРОМГАЗ: более 20 лет на рынке. Хозяйственный проезд, 19В. Телефон +7 (8352) 22-21-21.", "")
home += header("")
home += f'''
<main id="main">
<section class="hero">
 <div class="container hero-grid">
  <div class="hero-copy"><h1>Промышленные,<br>медицинские<br><span>и пищевые газы</span></h1><p class="hero-description">Чистые компоненты и смеси для предприятий, лабораторий и частных заказов. Подберём марку, объём и условия поставки.</p><div class="hero-actions"><a href="#catalog" class="button button-blue">Открыть каталог</a><button class="button button-outline" type="button" data-order>Рассчитать заказ</button></div></div>
  <div class="hero-media"><img class="industry-image" src="assets/industrial.jpg" alt="Применение технических газов в промышленности — материалы Linde" width="900" height="600" fetchpriority="high"><div class="dealer-card"><img src="assets/linde-logo.png" alt="Linde" width="150" height="80"><div><strong>Официальный дилер Linde</strong><span>Продукция международного производителя</span></div></div></div>
 </div>
</section>
<div id="company" class="facts"><div class="container facts-grid"><div><strong>20+ лет</strong><span>опыт поставок</span></div><div><strong>Подбор</strong><span>Марка и состав под вашу задачу</span></div><div><strong>Чебоксары</strong><span>Хозяйственный проезд, 19В</span></div></div></div>
<section id="catalog" class="section catalog-section"><div class="container"><div class="section-heading"><div><span class="eyebrow">КАТАЛОГ</span><h2>Продукция</h2></div><p>Выберите раздел и нужную позицию.<br>Стоимость и сроки поставки уточняйте в запросе.</p></div>{catalog()}<div class="catalog-bottom"><p>Есть спецификация или список для закупки?</p><a href="mailto:{EMAIL}" class="text-button">Отправить спецификацию</a></div></div></section>
<section id="services" class="section services-section"><div class="container service-layout"><div class="service-heading"><span class="eyebrow">УСЛОВИЯ ЗАКАЗА</span><h2>Как получить<br>продукцию</h2><p>Можно заказать с баллоном или использовать свой. Согласуем покупку, аренду, заправку или обмен, а затем — способ получения.</p></div><div class="service-list">
 <article class="service"><h3>Заправка и обмен</h3><p>Сообщите тип и объём ваших баллонов. Уточним условия заправки или подберём обмен.</p><button type="button" data-order="Другая продукция или услуга" data-comment="Нужна заправка или обмен баллонов.">Обсудить заправку</button></article>
 <article class="service"><h3>Продажа и аренда</h3><p>Если своего баллона нет, обсудим покупку или аренду под ваш заказ.</p><button type="button" data-order="Другая продукция или услуга" data-comment="Нужна покупка или аренда баллона.">Подобрать баллон</button></article>
 <article class="service"><h3>Обслуживание баллонов</h3><p>Освидетельствование и ремонт. Для расчёта нужны тип и состояние баллона.</p><button type="button" data-order="Другая продукция или услуга" data-comment="Интересует обслуживание баллонов.">Уточнить условия</button></article>
 <article class="service"><h3>Доставка и самовывоз</h3><p>Самовывоз — с Хозяйственного проезда, 19В. Доставку рассчитаем по адресу и объёму заказа.</p><button type="button" data-order="Другая продукция или услуга" data-comment="Хочу рассчитать доставку.">Рассчитать доставку</button></article>
</div></div></section>
<section class="request-section"><div class="container request-grid"><div><span class="eyebrow">ОТДЕЛ ПРОДАЖ</span><h2>Рассчитаем<br>ваш заказ</h2><p>Пришлите наименование, марку и объём. Уточним стоимость и срок поставки.</p></div><div class="request-contact"><button type="button" class="button button-white" data-order>Подготовить запрос по почте</button><a class="request-spec" href="mailto:{EMAIL}">Отправить готовую спецификацию</a></div></div></section>
<section id="contacts" class="section contacts-section"><div class="container"><div class="section-heading"><div><span class="eyebrow">КОНТАКТЫ</span><h2>ПРОМГАЗ в Чебоксарах</h2></div></div><div class="contacts-grid"><div class="contact-details"><div class="contact-item"><span class="contact-label">ОТДЕЛ ПРОДАЖ</span><a href="tel:+78352222121">+7 (8352) 22-21-21</a><a href="tel:+78352283093">+7 (8352) 28-30-93</a><a href="tel:+79278480990">+7 (927) 848-09-90</a></div><div class="contact-item"><span class="contact-label">ЭЛЕКТРОННАЯ ПОЧТА</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></div><div class="visit-panel"><span class="eyebrow">АДРЕС</span><h3>Хозяйственный проезд, 19В</h3><p>Перед приездом уточните время работы и наличие нужной продукции.</p><a class="button button-blue" href="{MAP}" target="_blank" rel="noopener noreferrer">Построить маршрут</a></div></div></div></section>
</main>'''
home += footer("") + order_dialog() + "\n</body></html>\n"
(DIST / "index.html").write_text(home, encoding="utf-8")

for g in GASES:
    related = [p for p in GASES if p["id"] != g["id"]][:3]
    page = head(g["name"] + " в Чебоксарах — ПРОМГАЗ", g["description"] + " Уточните стоимость и условия заказа в ПРОМГАЗ.", "../") + header("../")
    page += f'''
<main id="main">
  <div class="container breadcrumbs"><a href="../index.html">Главная</a><span>/</span><a href="../index.html#catalog">Каталог</a><span>/</span><span>{escape(g["name"])}</span></div>
  <section class="container product-hero">
    <div class="product-symbol"><img src="../assets/products/{g["id"]}-new.jpg" alt="{escape(g["name"])} в баллонах" width="360" height="360"><span>{escape(g["type"])}</span></div>
    <div class="product-info"><span class="eyebrow">КАТАЛОГ ПРОДУКЦИИ</span><h1>{escape(g["name"])}</h1><p class="product-description">{escape(g["description"])}</p><div class="product-price"><strong>Стоимость по запросу</strong><span>Зависит от марки, объёма и условий заказа.</span></div><button class="button button-blue" type="button" data-order="{escape(g["name"])}">Узнать стоимость</button></div>
  </section>
  <section class="container product-order-info"><div><span class="eyebrow">ДЛЯ РАСЧЁТА ЗАКАЗА</span><h2>Уточним детали</h2></div><div><p>{escape(g["note"])}</p><p>Если у вас есть собственные баллоны, сообщите об этом. Возможность заправки или обмена согласуем отдельно.</p><p>Получение: Хозяйственный проезд, 19В, Чебоксары. Возможность и условия доставки уточняйте в отделе продаж.</p></div></section>
  <section class="section related-section"><div class="container"><div class="section-heading"><h2>Другие позиции</h2><a class="text-button" href="../index.html#catalog">Весь каталог</a></div><div class="related-grid">{"".join(card(p, "../") for p in related)}</div></div></section>
</main>'''
    page += footer("../") + order_dialog(g["name"]) + "\n</body></html>\n"
    (DIST / "gases" / (g["id"] + ".html")).write_text(page, encoding="utf-8")

(DIST / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
(DIST / ".nojekyll").write_text("")
(DIST / "assets" / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="0" fill="#164ca8"/><path d="M17 47V17h30v30H37V27H27v20Z" fill="white"/></svg>')
print("Generated homepage and", len(GASES), "product pages.")
