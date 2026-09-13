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

  var categoryNav = document.querySelector('.catalog-tabs');
  if (categoryNav) {
    var categoryTabs = Array.from(categoryNav.querySelectorAll('.catalog-tab'));
    var categoryPanels = categoryTabs.map(function (tab) {
      return document.getElementById(tab.hash.slice(1));
    });
    function showCategory(index) {
      categoryTabs.forEach(function (tab, i) {
        tab.setAttribute('aria-selected', String(i === index));
        tab.tabIndex = i === index ? 0 : -1;
        categoryPanels[i].hidden = i !== index;
      });
    }
    function categoryFromHash() {
      var index = categoryTabs.findIndex(function (tab) { return tab.hash === window.location.hash; });
      if (index !== -1) showCategory(index);
    }
    categoryNav.setAttribute('role', 'tablist');
    categoryTabs.forEach(function (tab, index) {
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', categoryPanels[index].id);
      categoryPanels[index].setAttribute('role', 'tabpanel');
      categoryPanels[index].tabIndex = 0;
      tab.addEventListener('click', function (event) {
        event.preventDefault();
        showCategory(index);
        history.replaceState(null, '', tab.hash);
      });
      tab.addEventListener('keydown', function (event) {
        var next = index;
        if (event.key === 'ArrowRight') next = (index + 1) % categoryTabs.length;
        else if (event.key === 'ArrowLeft') next = (index + categoryTabs.length - 1) % categoryTabs.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = categoryTabs.length - 1;
        else if (event.key === ' ') {
          event.preventDefault();
          tab.click();
          return;
        } else return;
        event.preventDefault();
        categoryTabs[next].focus();
        categoryTabs[next].click();
      });
    });
    showCategory(0);
    categoryFromHash();
    window.addEventListener('hashchange', categoryFromHash);
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
