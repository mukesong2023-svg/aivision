// 主题切换：在 light/dark 间切换，保留用户选择
(function () {
  const root = document.documentElement;
  const btn = document.getElementById('themeToggle');
  const KEY = 'aivision-theme';

  const applyTheme = (t) => {
    if (t === 'light') root.classList.add('light');
    else root.classList.remove('light');
  };

  const saved = localStorage.getItem(KEY);
  if (saved) applyTheme(saved);

  btn && btn.addEventListener('click', () => {
    const isLight = root.classList.toggle('light');
    localStorage.setItem(KEY, isLight ? 'light' : 'dark');
  });
})();

// 导航平滑滚动与偏移处理
(function () {
  const links = document.querySelectorAll('a[href^="#"]');
  links.forEach((a) => {
    a.addEventListener('click', (e) => {
      const id = a.getAttribute('href');
      const el = document.querySelector(id);
      if (!el) return;
      e.preventDefault();
      const y = el.getBoundingClientRect().top + window.scrollY - 70; // header 偏移
      window.scrollTo({ top: y, behavior: 'smooth' });
    });
  });
})();