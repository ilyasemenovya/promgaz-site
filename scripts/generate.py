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
  <link rel="stylesheet" href="{prefix}assets/styles.css?v=3">
  <script src="{prefix}assets/site.js?v=3" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Перейти к содержимому</a>'''

def header(prefix):
    home = prefix + "index.html"
    return f'''
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{home}" aria-label="ПРОМГАЗ — главная">
      <span class="brand-name">ПРОМГАЗ</span>
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
    <button class="button button-blue button-full" type="submit">Открыть письмо</button>
    <p class="form-note">Откроется ваша почтовая программа. Отправьте письмо, чтобы отдел продаж получил запрос.</p>
    <p id="email-feedback" class="email-feedback" role="status" hidden>Письмо подготовлено. Если почтовая программа не открылась, напишите на <a href="mailto:{EMAIL}">{EMAIL}</a> или позвоните.</p>
  </form>
  <a class="dialog-phone" href="tel:+78352222121">{PHONE} +7 (8352) 22-21-21</a>
</dialog>'''

def footer(prefix):
    return f'''
<footer class="site-footer">
  <div class="container footer-main">
    <a class="brand brand-light" href="{prefix}index.html" aria-label="ПРОМГАЗ — главная"><span class="brand-name">ПРОМГАЗ</span><span class="brand-caption">ТЕХНИЧЕСКИЕ ГАЗЫ</span></a>
    <p>Чебоксары<br>Хозяйственный проезд, 19В</p>
    <div><a href="tel:+78352222121">+7 (8352) 22-21-21</a><a href="mailto:{EMAIL}">{EMAIL}</a></div>
  </div>
  <div class="container footer-bottom"><span>© ПРОМГАЗ, 2026</span><span>ИП Сусарина А. В. · ИНН 212900123770</span></div>
</footer>
<div class="mobile-contact-bar"><a href="tel:+78352222121">{PHONE} Позвонить</a><button type="button" data-order>Узнать стоимость</button></div>'''

def card(g, prefix=""):
    return f'''<article class="gas-card"><a class="product-link" href="{prefix}gases/{g['id']}.html"><div class="catalog-photo"><img src="{prefix}assets/products/{g['id']}.jpg" alt="{escape(g['name'])}: газ в баллонах" width="270" height="190" loading="lazy"></div><div class="card-copy"><span class="gas-type">{escape(g['type'])}</span><h3>{escape(g['name'])}</h3></div></a><div class="card-order"><a href="{prefix}gases/{g['id']}.html">О газе</a><button type="button" data-order="{escape(g['name'])}">Узнать цену</button></div></article>'''

cards = "".join(card(g) for g in GASES)
home = head("ПРОМГАЗ — технические газы в Чебоксарах", "Продажа технических газов в Чебоксарах. ПРОМГАЗ: более 20 лет на рынке. Хозяйственный проезд, 19В. Телефон +7 (8352) 22-21-21.", "")
home += header("")
home += f'''
<main id="main">
<section class="hero">
 <div class="container hero-grid">
  <div class="hero-copy"><p class="hero-location">ПРОМГАЗ / ЧЕБОКСАРЫ</p><h1>Технические газы<br>для вашего<br><span>производства</span></h1><p class="hero-description">Поставка газов, заправка и обмен баллонов.<br>Более 20 лет работаем в Чебоксарах.</p><div class="hero-actions"><a href="#catalog" class="button button-blue">Выбрать газ</a><a href="tel:+78352222121" class="hero-phone">+7 (8352) 22-21-21<span>Уточнить наличие и стоимость</span></a></div></div>
  <div class="hero-media"><img class="industry-image" src="assets/industrial.jpg" alt="Применение технических газов в промышленности — материалы Linde" width="900" height="600" fetchpriority="high"><div class="dealer-card"><img src="assets/linde-logo.png" alt="Linde" width="150" height="80"><div><strong>Дилер Linde</strong><span>Мировой бренд промышленных газов</span></div></div></div>
 </div>
</section>
<div class="facts"><div class="container facts-grid"><div><strong>20+ лет</strong><span>на рынке технических газов</span></div><div><strong>Газы и баллоны</strong><span>Заправка, обмен, покупка и аренда</span></div><div><strong>Чебоксары</strong><span>Хозяйственный проезд, 19В</span></div></div></div>
<section id="catalog" class="section catalog-section"><div class="container"><div class="section-heading"><div><span class="eyebrow">ПРОДУКЦИЯ</span><h2>Какой газ вам нужен?</h2></div><p>Выберите газ для заказа.<br>Марку, объём и стоимость уточним при обращении.</p></div><div class="catalog-grid">{cards}</div><div class="catalog-bottom"><p>Есть спецификация или список для закупки?</p><a href="mailto:{EMAIL}" class="text-button">Отправить на {EMAIL}</a></div></div></section>
<section id="services" class="section services-section"><div class="container service-layout"><div class="service-heading"><span class="eyebrow">БАЛЛОНЫ И УСЛУГИ</span><h2>Решим вопрос<br>с баллонами</h2><p>Можно обратиться за газом, баллоном или обслуживанием — согласуем всё в одном заказе.</p></div><div class="service-list">
 <article class="service"><h3>Заправка и обмен</h3><p>Сообщите тип и объём ваших баллонов. Уточним условия заправки или подберём обмен.</p><button type="button" data-order="Другая продукция или услуга" data-comment="Нужна заправка или обмен баллонов.">Обсудить заправку</button></article>
 <article class="service"><h3>Продажа и аренда</h3><p>Если своего баллона нет, обсудим покупку или аренду под ваш заказ.</p><button type="button" data-order="Другая продукция или услуга" data-comment="Нужна покупка или аренда баллона.">Подобрать баллон</button></article>
 <article class="service"><h3>Обслуживание баллонов</h3><p>Освидетельствование и ремонт. Для расчёта нужны тип и состояние баллона.</p><button type="button" data-order="Другая продукция или услуга" data-comment="Интересует обслуживание баллонов.">Уточнить условия</button></article>
 <article class="service"><h3>Доставка и самовывоз</h3><p>Самовывоз — с Хозяйственного проезда, 19В. Доставку рассчитаем по адресу и объёму заказа.</p><button type="button" data-order="Другая продукция или услуга" data-comment="Хочу рассчитать доставку.">Рассчитать доставку</button></article>
</div></div></section>
<section id="company" class="section company-section"><div class="container dealer-section"><div class="dealer-brand"><img src="assets/linde-logo.png" alt="Linde" width="240" height="128"><span>ПРОМГАЗ — ДИЛЕР LINDE</span></div><div class="company-copy"><span class="eyebrow">ПРОИЗВОДИТЕЛЬ ИМЕЕТ ЗНАЧЕНИЕ</span><h2>Газы Linde.<br>Поставщик в Чебоксарах.</h2><p>ПРОМГАЗ — дилер Linde. Вы можете заказать продукцию бренда у местного поставщика и обсудить марку газа, объём и условия получения напрямую с нашим отделом продаж.</p><a href="https://linru.ru/gases_and_equipment/" target="_blank" rel="noopener noreferrer" class="text-button">Продукция Linde</a></div></div></section>
<section class="request-section"><div class="container request-grid"><div><span class="eyebrow">ЗАКАЗ ГАЗА</span><h2>Назовите газ и объём.<br>Рассчитаем заказ.</h2><p>Сообщите, есть ли свои баллоны и нужна ли доставка.</p></div><div class="request-contact"><a href="tel:+78352222121">+7 (8352) 22-21-21</a><button type="button" class="button button-white" data-order>Подготовить запрос по почте</button><span>Для спецификаций: <a href="mailto:{EMAIL}">{EMAIL}</a></span></div></div></section>
<section id="contacts" class="section contacts-section"><div class="container"><div class="section-heading"><div><span class="eyebrow">КОНТАКТЫ</span><h2>ПРОМГАЗ в Чебоксарах</h2></div></div><div class="contacts-grid"><div class="contact-details"><div class="contact-item"><span class="contact-label">ОТДЕЛ ПРОДАЖ</span><a href="tel:+78352222121">+7 (8352) 22-21-21</a><a href="tel:+78352283093">+7 (8352) 28-30-93</a><a href="tel:+79278480990">+7 (927) 848-09-90</a></div><div class="contact-item"><span class="contact-label">ЭЛЕКТРОННАЯ ПОЧТА</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></div><div class="visit-panel"><span class="eyebrow">АДРЕС</span><h3>Хозяйственный проезд, 19В</h3><p>Перед приездом уточните время работы и наличие нужного газа.</p><a class="button button-blue" href="{MAP}" target="_blank" rel="noopener noreferrer">Построить маршрут</a></div></div></div></section>
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
    <div class="product-symbol"><img src="../assets/products/{g["id"]}.jpg" alt="{escape(g["name"])} в баллонах" width="270" height="190"><span>{escape(g["type"])}</span></div>
    <div class="product-info"><span class="eyebrow">ТЕХНИЧЕСКИЕ ГАЗЫ В ЧЕБОКСАРАХ</span><h1>{escape(g["name"])}</h1><p class="product-description">{escape(g["description"])}</p><div class="product-price"><strong>Стоимость по запросу</strong><span>Зависит от марки газа, объёма и условий заказа.</span></div><button class="button button-blue" type="button" data-order="{escape(g["name"])}">Узнать стоимость</button><a class="product-phone" href="tel:+78352222121">{PHONE} +7 (8352) 22-21-21</a></div>
  </section>
  <section class="container product-order-info"><div><span class="eyebrow">ДЛЯ РАСЧЁТА ЗАКАЗА</span><h2>Уточним детали</h2></div><div><p>{escape(g["note"])}</p><p>Если у вас есть собственные баллоны, сообщите об этом. Возможность заправки или обмена согласуем отдельно.</p><p>Получение: Хозяйственный проезд, 19В, Чебоксары. Возможность и условия доставки уточняйте в отделе продаж.</p></div></section>
  <section class="section related-section"><div class="container"><div class="section-heading"><h2>Другие газы</h2><a class="text-button" href="../index.html#catalog">Весь каталог</a></div><div class="related-grid">{"".join(card(p, "../") for p in related)}</div></div></section>
</main>'''
    page += footer("../") + order_dialog(g["name"]) + "\n</body></html>\n"
    (DIST / "gases" / (g["id"] + ".html")).write_text(page, encoding="utf-8")

(DIST / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
(DIST / ".nojekyll").write_text("")
(DIST / "assets" / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="0" fill="#164ca8"/><path d="M17 47V17h30v30H37V27H27v20Z" fill="white"/></svg>')
print("Generated homepage and", len(GASES), "product pages.")
