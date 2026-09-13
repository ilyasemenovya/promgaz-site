(function () {
  'use strict';
  var menuButton = document.querySelector('.menu-toggle');
  var menu = document.getElementById('mobile-nav');
  function closeMenu() {
    if (!menu || !menuButton) return;
    menu.hidden = true;
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Открыть меню');
  }
  if (menu && menuButton) {
    menuButton.addEventListener('click', function () {
      var open = menuButton.getAttribute('aria-expanded') === 'true';
      menu.hidden = open;
      menuButton.setAttribute('aria-expanded', String(!open));
      menuButton.setAttribute('aria-label', open ? 'Открыть меню' : 'Закрыть меню');
    });
    menu.querySelectorAll('a').forEach(function (link) { link.addEventListener('click', closeMenu); });
    window.addEventListener('resize', function () { if (window.innerWidth > 980) closeMenu(); });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && !menu.hidden) {
        closeMenu();
        menuButton.focus();
      }
    });
  }

  var dialog = document.getElementById('order-dialog');
  var form = document.getElementById('order-form');
  if (!dialog || !form) return;
  var gasInput = document.getElementById('order-gas');
  var commentInput = document.getElementById('order-comment');
  var feedback = document.getElementById('email-feedback');
  var lastTrigger = null;
  var defaultGas = gasInput.value;

  document.querySelectorAll('[data-order]').forEach(function (trigger) {
    trigger.addEventListener('click', function () {
      lastTrigger = trigger;
      form.reset();
      gasInput.value = trigger.getAttribute('data-order') || defaultGas;
      commentInput.value = trigger.getAttribute('data-comment') || '';
      feedback.hidden = true;
      closeMenu();
      if (typeof dialog.showModal !== 'function') {
        window.location.href = 'mailto:Promgaz21@yandex.ru?subject=' + encodeURIComponent('Запрос стоимости — ПРОМГАЗ');
        return;
      }
      dialog.showModal();
      document.body.classList.add('dialog-open');
    });
  });
  dialog.querySelector('.close-dialog').addEventListener('click', function () { dialog.close(); });
  dialog.addEventListener('click', function (event) {
    if (event.target !== dialog) return;
    var rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
  dialog.addEventListener('close', function () {
    document.body.classList.remove('dialog-open');
    if (lastTrigger) lastTrigger.focus();
  });
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    var quantity = document.getElementById('order-quantity').value.trim();
    var gas = gasInput.value || 'Прошу уточнить ассортимент';
    var body = [
      'Здравствуйте! Прошу рассчитать заказ.',
      '',
      'Продукция / услуга: ' + gas,
      'Количество и объём: ' + (quantity || 'Уточню при согласовании'),
      '',
      commentInput.value.trim(),
      '',
      'Запрос с сайта ПРОМГАЗ.'
    ].join('\n');
    var subject = 'Запрос стоимости — ' + gas + ' — ПРОМГАЗ';
    feedback.hidden = false;
    window.location.href = 'mailto:Promgaz21@yandex.ru?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  });
}());
