from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
GASES = json.loads((ROOT / "content/catalog.json").read_text())
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
  <link rel="stylesheet" href="{prefix}assets/styles.css">
  <script src="{prefix}assets/site.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Перейти к содержимому</a>'''

def header(prefix):
    home = prefix + "index.html"
    return f'''
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{home}" aria-label="ПРОМГАЗ — главная">
      <span class="brand-name">ПРОМГАЗ<span class="brand-square" aria-hidden="true"></span></span>
      <span class="brand-caption">ТЕХНИЧЕСКИЕ ГАЗЫ</span>
    </a>
    <nav class="desktop-nav" aria-label="Основная навигация">
      <a href="{home}#catalog">Каталог</a>
      <a href="{home}#services">Услуги</a>
      <a href="{home}#company">О компании</a>
      <a href="{home}#contacts">Контакты</a>
    </nav>
    <div class="header-contact">
      <a href="tel:+78352222121">+7 (8352) 22-21-21</a>
      <span>Чебоксары</span>
    </div>
    <button class="menu-toggle" type="button" aria-label="Открыть меню" aria-expanded="false" aria-controls="mobile-nav">
      <span></span><span></span>
    </button>
  </div>
  <nav id="mobile-nav" class="mobile-nav" aria-label="Мобильная навигация" hidden>
    <a href="{home}#catalog">Каталог газов</a>
    <a href="{home}#services">Услуги</a>
    <a href="{home}#company">О компании</a>
    <a href="{home}#contacts">Контакты</a>
    <a href="tel:+78352222121">+7 (8352) 22-21-21</a>
  </nav>
</header>'''

def order_dialog(selected=""):
    options = "".join(f'<option value="{escape(g["name"])}"{" selected" if g["name"] == selected else ""}>{escape(g["name"])}</option>' for g in GASES)
    return f'''
<dialog class="order-dialog" id="order-dialog" aria-labelledby="order-title">
  <div class="dialog-top"><span class="eyebrow">ЗАПРОС СТОИМОСТИ</span>
    <button type="button" class="close-dialog" aria-label="Закрыть окно"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m6 6 12 12M6 18 18 6" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg></button>
  </div>
  <h2 id="order-title">Что вам нужно?</h2>
  <p class="dialog-intro">Укажите состав заказа. Подготовим письмо в отдел продаж.</p>
  <form id="order-form">
    <label for="order-gas">Газ или продукция</label>
    <select id="order-gas" name="gas"><option value="">Выберите газ</option>{options}<option value="Другая продукция или услуга">Другая продукция или услуга</option></select>
    <label for="order-quantity">Количество и объём</label>
    <input id="order-quantity" name="quantity" placeholder="Например, 2 баллона по 40 л" maxlength="150">
    <label for="order-comment">Пожелания к заказу</label>
    <textarea id="order-comment" name="comment" rows="3" placeholder="Марка газа, наличие своих баллонов, адрес доставки…" maxlength="1500"></textarea>
    <button class="button button-blue button-full" type="submit">Открыть письмо {ARROW}</button>
    <p class="form-note">Откроется ваша почтовая программа. Отправьте письмо, чтобы отдел продаж получил запрос.</p>
    <p id="email-feedback" class="email-feedback" role="status" hidden>Письмо подготовлено. Если почтовая программа не открылась, напишите на <a href="mailto:{EMAIL}">{EMAIL}</a> или позвоните.</p>
  </form>
  <a class="dialog-phone" href="tel:+78352222121">{PHONE} +7 (8352) 22-21-21</a>
</dialog>'''

def footer(prefix):
    return f'''
<footer class="site-footer">
  <div class="container footer-main">
    <a class="brand brand-light" href="{prefix}index.html" aria-label="ПРОМГАЗ — главная"><span class="brand-name">ПРОМГАЗ<span class="brand-square" aria-hidden="true"></span></span><span class="brand-caption">ТЕХНИЧЕСКИЕ ГАЗЫ</span></a>
    <p>Чебоксары<br>Хозяйственный проезд, 19В</p>
    <div><a href="tel:+78352222121">+7 (8352) 22-21-21</a><a href="mailto:{EMAIL}">{EMAIL}</a></div>
  </div>
  <div class="container footer-bottom"><span>© ПРОМГАЗ, 2026</span><span>ИП Сусарина А. В. · ИНН 212900123770</span></div>
</footer>
<div class="mobile-contact-bar"><a href="tel:+78352222121">{PHONE} Позвонить</a><button type="button" data-order>Запросить стоимость {ARROW}</button></div>'''

def card(g, prefix=""):
    return f'''<a class="gas-card gas-{g["color"]}" href="{prefix}gases/{g["id"]}.html">
  <div class="gas-card-top"><span class="gas-formula">{escape(g["formula"])}</span><span class="card-arrow">{OUT}</span></div>
  <div><span class="gas-type">{escape(g["type"])}</span><h3>{escape(g["name"])}</h3></div>
  <div class="gas-card-bottom"><span>Стоимость по запросу</span><span>Подробнее</span></div>
</a>'''

cards = "".join(card(g) for g in GASES)
home = head("ПРОМГАЗ — технические газы в Чебоксарах", "Продажа технических газов в Чебоксарах. ПРОМГАЗ: более 20 лет на рынке. Хозяйственный проезд, 19В. Телефон +7 (8352) 22-21-21.", "")
home += header("")
home += f'''
<main id="main">
  <section class="hero">
    <div class="container hero-grid">
      <div class="hero-copy">
        <div class="eyebrow hero-eyebrow"><span class="small-rule"></span> ЧЕБОКСАРЫ</div>
        <h1>Технические<br>газы<span class="cyan">.</span><br><span class="hero-soft">Для вашей<br class="desktop-break"> работы.</span></h1>
        <p>Кислород, аргон, углекислота<br class="desktop-break"> и другие газы для технических задач.</p>
        <div class="hero-actions"><a class="button button-white" href="#catalog">Выбрать газ {ARROW}</a><button class="button button-ghost" type="button" data-order>Запросить стоимость</button></div>
        <div class="hero-experience"><strong>20<span>+</span></strong><span>лет на рынке<br>технических газов</span></div>
      </div>
      <figure class="hero-photo">
        <img src="assets/loading-zone.jpeg" alt="Вывеска ПРОМГАЗ и вход в зону отгрузки на Хозяйственном проезде, 19В" width="706" height="1536" fetchpriority="high">
        <figcaption><span class="photo-caption-label">ПРОМГАЗ / ЧЕБОКСАРЫ</span><span>Хозяйственный<br>проезд, 19В</span><a href="{MAP}" target="_blank" rel="noopener noreferrer" aria-label="Построить маршрут в Яндекс Картах">{OUT}</a></figcaption>
      </figure>
    </div>
  </section>

  <div class="intro-strip">
    <div class="container strip-grid">
      <div><span class="strip-number">01</span><p>Выберите<br><strong>нужный газ</strong></p></div>
      <div><span class="strip-number">02</span><p>Уточните<br><strong>стоимость заказа</strong></p></div>
      <div><span class="strip-number">03</span><p>Согласуйте<br><strong>получение</strong></p></div>
    </div>
  </div>

  <section id="catalog" class="section catalog-section">
    <div class="container">
      <div class="section-heading"><div><span class="eyebrow">ПРОДУКЦИЯ</span><h2>Найдите свой газ</h2></div><p>Выберите позицию, чтобы уточнить<br>параметры и запросить стоимость.</p></div>
      <div class="catalog-grid">{cards}</div>
      <div class="catalog-bottom"><p>Нужен другой газ или особая марка?</p><button class="text-button" type="button" data-order="Другая продукция или услуга">Обсудить заказ {ARROW}</button></div>
    </div>
  </section>

  <section id="services" class="section services-section">
    <div class="container">
      <div class="section-heading"><div><span class="eyebrow">УСЛУГИ</span><h2>Газ и всё,<br>что с ним связано</h2></div><p>Уточните доступную услугу<br>и условия для вашего заказа.</p></div>
      <div class="service-grid">
        <article class="service"><span class="service-index">01 /</span><h3>Заправка<br>и обмен</h3><p>Сообщите, какой газ нужен и какие баллоны у вас есть. Уточним порядок заправки или обмена.</p><button class="text-button" type="button" data-order="Другая продукция или услуга" data-comment="Интересует заправка или обмен баллонов.">Уточнить условия {ARROW}</button></article>
        <article class="service"><span class="service-index">02 /</span><h3>Продажа<br>и аренда баллонов</h3><p>Уточните доступные баллоны, стоимость покупки и условия аренды.</p><button class="text-button" type="button" data-order="Другая продукция или услуга" data-comment="Интересует покупка или аренда баллонов.">Уточнить условия {ARROW}</button></article>
        <article class="service"><span class="service-index">03 /</span><h3>Обслуживание<br>баллонов</h3><p>Вопросы по освидетельствованию и ремонту. Для расчёта сообщите тип и состояние баллона.</p><button class="text-button" type="button" data-order="Другая продукция или услуга" data-comment="Интересует обслуживание баллонов.">Уточнить условия {ARROW}</button></article>
        <article class="service"><span class="service-index">04 /</span><h3>Доставка<br>и самовывоз</h3><p>Укажите адрес и объём заказа. Согласуем возможность доставки, стоимость и время получения.</p><button class="text-button" type="button" data-order="Другая продукция или услуга" data-comment="Хочу уточнить условия доставки или самовывоза.">Уточнить условия {ARROW}</button></article>
      </div>
    </div>
  </section>

  <section id="company" class="section company-section">
    <div class="container company-grid">
      <div><span class="eyebrow">О КОМПАНИИ</span><h2>ПРОМГАЗ.<br>Знакомое имя.<br><span class="blue">Большой опыт.</span></h2></div>
      <div class="company-copy"><p class="lead">Более 20 лет<br>на рынке технических газов.</p><p>Работаем в Чебоксарах на Хозяйственном проезде, 19В. Поможем уточнить ассортимент, стоимость и условия получения вашего заказа.</p><p>Для расчёта достаточно сообщить, какой газ нужен, в каком количестве и есть ли у вас свои баллоны.</p><a class="text-button" href="#contacts">Связаться с нами {ARROW}</a></div>
    </div>
    <div class="container"><div class="partner-block"><div><span class="eyebrow">НАШ ПАРТНЁР</span><h3>Линде Газ Рус</h3></div><p>Информация о газах и оборудовании партнёра — в официальном каталоге.</p><a class="button button-outline" href="https://linru.ru/gases_and_equipment/" target="_blank" rel="noopener noreferrer">Каталог партнёра {OUT}</a></div></div>
  </section>

  <section class="request-section">
    <div class="container request-grid"><div><span class="eyebrow">ОТДЕЛ ПРОДАЖ</span><h2>Обсудим<br>ваш заказ?</h2></div><div><p>Газ, количество, условия получения.<br>Начнём с того, что вам нужно.</p><button class="button button-white" type="button" data-order>Запросить стоимость {ARROW}</button><a class="request-email" href="mailto:{EMAIL}">{EMAIL}</a></div></div>
  </section>

  <section id="contacts" class="section contacts-section">
    <div class="container">
      <div class="section-heading"><div><span class="eyebrow">КОНТАКТЫ</span><h2>Мы в Чебоксарах</h2></div><a class="text-button" href="{MAP}" target="_blank" rel="noopener noreferrer">Открыть Яндекс Карты {OUT}</a></div>
      <div class="contacts-grid">
        <div class="contact-details">
          <div class="contact-item"><span class="contact-label">АДРЕС</span><p>Хозяйственный<br>проезд, 19В</p><span class="muted">Перед приездом уточните время работы.</span></div>
          <div class="contact-item"><span class="contact-label">ТЕЛЕФОНЫ</span><a href="tel:+78352222121">+7 (8352) 22-21-21</a><a href="tel:+78352283093">+7 (8352) 28-30-93</a><a href="tel:+79278480990">+7 (927) 848-09-90</a></div>
          <div class="contact-item"><span class="contact-label">ПОЧТА</span><a class="email-link" href="mailto:{EMAIL}">{EMAIL}</a></div>
        </div>
        <a class="contact-photo" href="{MAP}" target="_blank" rel="noopener noreferrer"><img src="assets/loading-zone.jpeg" alt="Здание ПРОМГАЗ: ориентир для приезда на склад" width="706" height="1536" loading="lazy"><span>Узнайте нас по синей вывеске {OUT}</span></a>
      </div>
    </div>
  </section>
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
    <div class="product-symbol gas-{g["color"]}"><span class="eyebrow">ПРОМГАЗ / ТЕХНИЧЕСКИЕ ГАЗЫ</span><div>{escape(g["formula"])}</div><span>{escape(g["type"])}</span></div>
    <div class="product-info"><span class="eyebrow">ТЕХНИЧЕСКИЕ ГАЗЫ В ЧЕБОКСАРАХ</span><h1>{escape(g["name"])}</h1><p class="product-description">{escape(g["description"])}</p><div class="product-price"><strong>Стоимость по запросу</strong><span>Зависит от марки газа, объёма и условий заказа.</span></div><button class="button button-blue" type="button" data-order="{escape(g["name"])}">Запросить стоимость {ARROW}</button><a class="product-phone" href="tel:+78352222121">{PHONE} +7 (8352) 22-21-21</a></div>
  </section>
  <section class="container product-order-info"><div><span class="eyebrow">ДЛЯ РАСЧЁТА ЗАКАЗА</span><h2>Уточним детали</h2></div><div><p>{escape(g["note"])}</p><p>Если у вас есть собственные баллоны, сообщите об этом. Возможность заправки или обмена согласуем отдельно.</p><p>Получение: Хозяйственный проезд, 19В, Чебоксары. Возможность и условия доставки уточняйте в отделе продаж.</p></div></section>
  <section class="section related-section"><div class="container"><div class="section-heading"><h2>Другие газы</h2><a class="text-button" href="../index.html#catalog">Весь каталог {ARROW}</a></div><div class="related-grid">{"".join(card(p, "../") for p in related)}</div></div></section>
</main>'''
    page += footer("../") + order_dialog(g["name"]) + "\n</body></html>\n"
    (DIST / "gases" / (g["id"] + ".html")).write_text(page, encoding="utf-8")

(DIST / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
(DIST / ".nojekyll").write_text("")
(DIST / "assets" / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#164ca8"/><path d="M17 47V17h30v30H37V27H27v20Z" fill="white"/><rect x="44" y="44" width="10" height="10" fill="#55d5d5"/></svg>')
print("Generated homepage and", len(GASES), "product pages.")
