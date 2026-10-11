(() => {
  const slider = document.querySelector('[data-artist-slider]');
  const controls = document.querySelector('[data-slider-controls]');
  const dots = document.querySelector('[data-slider-dots]');
  if (!slider || !controls || !dots) return;

  const slides = [...slider.querySelectorAll('.artist-slide')];
  const selectors = [...dots.querySelectorAll('[data-slide-to]')];
  if (slides.length < 2 || selectors.length !== slides.length) return;

  const count = controls.querySelector('[data-slider-count]');
  let current = 0;

  function show(index) {
    current = (index + slides.length) % slides.length;
    slides.forEach((slide, position) => {
      slide.hidden = position !== current;
    });
    selectors.forEach((button, position) => {
      button.setAttribute('aria-pressed', String(position === current));
    });
    count.textContent = `${String(current + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`;
  }

  controls.querySelector('[data-slider-prev]').addEventListener('click', () => show(current - 1));
  controls.querySelector('[data-slider-next]').addEventListener('click', () => show(current + 1));
  selectors.forEach((button, position) => button.addEventListener('click', () => show(position)));

  let touchStartX = null;
  slider.addEventListener('touchstart', (event) => {
    touchStartX = event.changedTouches[0].screenX;
  }, { passive: true });
  slider.addEventListener('touchend', (event) => {
    if (touchStartX === null) return;
    const distance = event.changedTouches[0].screenX - touchStartX;
    if (Math.abs(distance) > 60) show(current + (distance < 0 ? 1 : -1));
    touchStartX = null;
  }, { passive: true });

  controls.hidden = false;
  dots.hidden = false;
  show(0);
})();
