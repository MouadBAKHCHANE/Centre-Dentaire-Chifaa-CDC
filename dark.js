/* ============================================================
   Centre Dentaire Chifaa, version sombre
   GSAP ScrollTrigger choreography + Lenis + Three.js implant.
   The sticky treatment stack is the page's one authored scroll
   moment; everything else stays quiet and supportive.
   ============================================================ */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var isMobile = window.matchMedia('(max-width: 820px), (hover: none)').matches;
  var hasGsap = !!(window.gsap && window.ScrollTrigger);


  /* ---------- nav dropdowns ---------- */
  document.querySelectorAll('[data-drop]').forEach(function (drop) {
    var btn = drop.querySelector('.pill');
    var set = function (v) {
      btn.setAttribute('aria-expanded', v ? 'true' : 'false');
      drop.setAttribute('data-open', v ? '1' : '0');
    };
    drop.addEventListener('pointerenter', function () { set(true); });
    drop.addEventListener('pointerleave', function () { set(false); });
    drop.addEventListener('focusin', function () { set(true); });
    drop.addEventListener('focusout', function (e) { if (!drop.contains(e.relatedTarget)) set(false); });
    btn.addEventListener('click', function () { set(drop.getAttribute('data-open') !== '1'); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { set(false); btn.blur(); }
    });
  });

  /* ---------- hero video pause/play ---------- */
  var vid = document.getElementById('hero-video');
  var toggle = document.getElementById('media-toggle');
  if (vid && toggle) {
    /* lecture automatique robuste : iOS peut refuser le premier play()
       (economie d'energie, chargement) — on reessaie des que possible
       puis au premier contact avec la page */
    var tryPlay = function () {
      vid.muted = true;
      var p = vid.play();
      if (p && p.catch) p.catch(function () {});
    };
    tryPlay();
    ['loadeddata', 'canplay'].forEach(function (ev) {
      vid.addEventListener(ev, tryPlay, { once: true });
    });
    ['touchstart', 'click'].forEach(function (ev) {
      document.addEventListener(ev, function onFirst() {
        if (vid.paused) tryPlay();
        document.removeEventListener(ev, onFirst);
      }, { passive: true });
    });
    var userPaused = false;
    toggle.addEventListener('click', function () {
      var paused = vid.paused;
      userPaused = !paused;
      if (paused) vid.play(); else vid.pause();
      toggle.setAttribute('aria-pressed', paused ? 'false' : 'true');
      toggle.setAttribute('aria-label', paused ? 'Mettre la vidéo en pause' : 'Lire la vidéo');
    });
    /* hors écran, la vidéo ne tourne plus : le décodage continu ralentissait le défilement */
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        if (es[0].isIntersecting) { if (!userPaused) tryPlay(); } else vid.pause();
      }).observe(vid);
    }
  }

  /* ---------- menu mobile (burger) ---------- */
  (function initBurger() {
    var burger = document.querySelector('.burger');
    var menu = document.getElementById('m-menu');
    if (!burger || !menu) return;
    var setOpen = function (open) {
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
      menu.classList.toggle('is-open', open);
      document.documentElement.style.overflow = open ? 'hidden' : '';
      if (window.cdcLenis) { open ? window.cdcLenis.stop() : window.cdcLenis.start(); }
    };
    burger.addEventListener('click', function () {
      setOpen(burger.getAttribute('aria-expanded') !== 'true');
    });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { setOpen(false); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });
  })();

  /* ---------- nav state + bouton retour en haut ---------- */
  var nav = document.getElementById('nav');
  var fabTop = document.querySelector('.fab-top');
  var onScrollNav = function () {
    var y = window.scrollY || 0;
    nav.classList.toggle('is-scrolled', y > 30);
    if (fabTop) fabTop.classList.toggle('is-visible', y > 600);
  };
  window.addEventListener('scroll', onScrollNav, { passive: true });
  onScrollNav();

  if (hasGsap && !reduced) {
    gsap.registerPlugin(ScrollTrigger);
    gsap.config({ nullTargetWarn: false });

    /* ---------- smooth scroll ---------- */
    var lenis = null;
    if (window.Lenis) {
      lenis = new Lenis({ lerp: 0.11 });
      window.cdcLenis = lenis;
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
      gsap.ticker.lagSmoothing(0);
      document.querySelectorAll('a[href^="#"]').forEach(function (a) {
        a.addEventListener('click', function (e) {
          var target = document.querySelector(a.getAttribute('href'));
          if (!target) return;
          e.preventDefault();
          lenis.scrollTo(target, { offset: -80 });
        });
      });
    }

    /* ---------- line reveals (headline splitting honors <br>) ---------- */
    document.querySelectorAll('[data-lines]').forEach(function (el) {
      var lines = el.innerHTML.split(/<br\s*\/?>/i).map(function (l) { return l.trim(); });
      el.innerHTML = lines.map(function (l) {
        return '<span class="l-clip"><span class="l-line">' + l + '</span></span>';
      }).join('');
    });

    /* hero entrance */
    gsap.timeline({ defaults: { ease: 'power4.out' } })
      .from('.hero-media', { opacity: 0, scale: 0.985, duration: 1.1 }, 0.05)
      .from('.hero-panel', { opacity: 0, y: 40, duration: 1.0 }, 0.25)
      .from('.hero h1 .l-line', { yPercent: 115, duration: 1.05, stagger: 0.12 }, 0.45)
      .from('.hero [data-fade]', { opacity: 0, y: 22, duration: 0.8, stagger: 0.12 }, 0.75)
      .from('.nav', { opacity: 0, y: -14, duration: 0.7 }, 0.3);

    /* scroll reveals elsewhere */
    document.querySelectorAll('[data-lines]').forEach(function (el) {
      if (el.closest('.hero')) return;
      gsap.from(el.querySelectorAll('.l-line'), {
        yPercent: 115, duration: 0.95, ease: 'power4.out', stagger: 0.1,
        scrollTrigger: { trigger: el, start: 'top 85%' }
      });
    });
    document.querySelectorAll('[data-fade]').forEach(function (el) {
      if (el.closest('.hero')) return;
      gsap.from(el, {
        opacity: 0, y: 30, duration: 0.85, ease: 'power3.out',
        scrollTrigger: { trigger: el, start: 'top 87%' }
      });
    });

    /* hero media slow pan (scale leaves headroom, video fills the card) */
    gsap.fromTo('.hero-media video', { yPercent: -6, scale: 1.14 }, {
      yPercent: 6, scale: 1.14, ease: 'none',
      scrollTrigger: { trigger: '.hero-media', start: 'top top', end: 'bottom top', scrub: true }
    });

    /* condition cards reveal one by one as they enter the viewport */
    gsap.utils.toArray('.s-card').forEach(function (card) {
      gsap.from(card, {
        opacity: 0, y: 90, scale: 0.97, duration: 1.0, ease: 'power3.out',
        scrollTrigger: { trigger: card, start: 'top 82%' }
      });
      gsap.from(card.querySelectorAll('.s-cond, .s-text > *, .s-rel'), {
        opacity: 0, y: 26, duration: 0.7, ease: 'power3.out', stagger: 0.09, delay: 0.15,
        scrollTrigger: { trigger: card, start: 'top 82%' }
      });
    });

    /* 5. photos des cartes : dévoilement du centre vers les bords + léger zoom arrière */
    gsap.utils.toArray('.s-card figure').forEach(function (fig) {
      gsap.fromTo(fig, { clipPath: 'inset(14% 14% 14% 14% round 10px)' }, {
        clipPath: 'inset(0% 0% 0% 0% round 10px)', duration: 1.3, ease: 'expo.out', delay: 0.1,
        scrollTrigger: { trigger: fig, start: 'top 85%' }
      });
      gsap.fromTo(fig.querySelectorAll('img'), { scale: 1.1 }, {
        scale: 1, duration: 1.6, ease: 'expo.out', delay: 0.1,
        scrollTrigger: { trigger: fig, start: 'top 85%' }
      });
    });

    /* Le cabinet : la photo de fond glisse doucement au scroll (parallaxe) */
    if (document.querySelector('[data-lieu-parallax]')) {
      gsap.fromTo('[data-lieu-parallax]', { yPercent: -4 }, {
        yPercent: 4, ease: 'none',
        scrollTrigger: { trigger: '.lieu', start: 'top bottom', end: 'bottom top', scrub: true }
      });
    }

    /* cabinet photo parallax (section optionnelle) */
    if (document.querySelector('[data-parallax] img')) {
      gsap.fromTo('[data-parallax] img', { yPercent: -8 }, {
        yPercent: 0, ease: 'none',
        scrollTrigger: { trigger: '[data-parallax]', start: 'top bottom', end: 'bottom top', scrub: true }
      });
    }

    /* magnetic CTA */
    if (!isMobile) {
      document.querySelectorAll('[data-magnet]').forEach(function (btn) {
        btn.addEventListener('pointermove', function (e) {
          var r = btn.getBoundingClientRect();
          gsap.to(btn, {
            x: (e.clientX - r.left - r.width / 2) * 0.2,
            y: (e.clientY - r.top - r.height / 2) * 0.3,
            duration: 0.5, ease: 'power3.out'
          });
        });
        btn.addEventListener('pointerleave', function () {
          gsap.to(btn, { x: 0, y: 0, duration: 0.7, ease: 'elastic.out(1, 0.5)' });
        });
      });
    }
  }

  /* ============================================================
     Three.js: the implant model, relit for the dark room.
     Same procedural sculpt as the light site, navy fog, warm key.
     ============================================================ */
  var host = document.getElementById('three-host');
  var hint = document.getElementById('three-hint');
  var fallback = document.getElementById('three-fallback');

  function threeFail(err) {
    if (err) console.warn('[CDC] modèle 3D indisponible :', err);
    if (hint) hint.style.display = 'none';
    if (fallback) fallback.style.display = 'grid';
  }

  function initThree() {
    return Promise.resolve(window.THREE).then(function (THREE) {
      if (!THREE) throw new Error('three.js indisponible');
      var w = host.clientWidth, h = host.clientHeight;
      var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
      renderer.setSize(w, h);
      renderer.domElement.style.display = 'block';
      renderer.domElement.setAttribute('aria-hidden', 'true');
      host.appendChild(renderer.domElement);

      var scene = new THREE.Scene();
      scene.fog = new THREE.Fog(0x0A1D30, 9, 22);
      var camera = new THREE.PerspectiveCamera(38, w / h, .1, 100);
      camera.position.set(4.2, 1.4, 6.4);

      scene.add(new THREE.HemisphereLight(0xF4E9DC, 0x0E2740, 1.35));
      var key = new THREE.DirectionalLight(0xFFE2C4, 2.1);
      key.position.set(4, 6, 5);
      scene.add(key);
      var rim = new THREE.DirectionalLight(0x9CB9D7, 1.1);
      rim.position.set(-5, 2, -4);
      scene.add(rim);

      var g = new THREE.Group();

      var boneMat = new THREE.MeshStandardMaterial({ color: 0xD9CFC6, roughness: .85, metalness: 0, side: THREE.DoubleSide });
      var bone = new THREE.Mesh(new THREE.BoxGeometry(4.6, 2.6, 2.2, 1, 1, 1), boneMat);
      bone.position.y = -1.35;
      g.add(bone);

      var gum = new THREE.Mesh(new THREE.BoxGeometry(4.6, .42, 2.2),
        new THREE.MeshStandardMaterial({ color: 0xB56A5E, roughness: .6 }));
      gum.position.y = .05;
      g.add(gum);

      var tiMat = new THREE.MeshStandardMaterial({ color: 0xC6CDD4, roughness: .26, metalness: .95 });
      var post = new THREE.Mesh(new THREE.CylinderGeometry(.34, .24, 2.1, 28), tiMat);
      post.position.y = -1.1;
      g.add(post);
      for (var i = 0; i < 9; i++) {
        var t = new THREE.Mesh(new THREE.TorusGeometry(.3 - i * .012, .045, 8, 26), tiMat);
        t.rotation.x = Math.PI / 2;
        t.position.y = -.15 - i * .22;
        g.add(t);
      }
      var abut = new THREE.Mesh(new THREE.CylinderGeometry(.22, .3, .75, 24), tiMat);
      abut.position.y = .33;
      g.add(abut);

      var crownMat = new THREE.MeshStandardMaterial({ color: 0xFBF7F2, roughness: .16, metalness: .05 });
      var crown = new THREE.Mesh(new THREE.SphereGeometry(.62, 32, 24), crownMat);
      crown.scale.set(1, .95, .85);
      crown.position.y = 1.12;
      g.add(crown);
      var neck = new THREE.Mesh(new THREE.CylinderGeometry(.38, .5, .5, 24), crownMat);
      neck.position.y = .62;
      g.add(neck);

      var nb = new THREE.Mesh(new THREE.CylinderGeometry(.42, .3, 2.2, 24),
        new THREE.MeshStandardMaterial({ color: 0xFBF7F2, roughness: .2 }));
      nb.position.set(-1.5, -1.05, 0);
      g.add(nb);
      var nc = new THREE.Mesh(new THREE.SphereGeometry(.66, 28, 20), crownMat);
      nc.scale.set(1, .95, .85);
      nc.position.set(-1.5, .95, 0);
      g.add(nc);

      scene.add(g);
      camera.lookAt(0, .1, 0);

      var yaw = 0, pitch = .1, targetYaw = 0, targetPitch = .1, auto = !reduced, dragging = false, lastX = 0, lastY = 0;
      var el = renderer.domElement;
      el.style.cursor = 'grab';
      el.style.touchAction = 'pan-y';
      el.addEventListener('pointerdown', function (e) {
        dragging = true; auto = false; lastX = e.clientX; lastY = e.clientY;
        el.style.cursor = 'grabbing';
        if (el.setPointerCapture) el.setPointerCapture(e.pointerId);
      });
      el.addEventListener('pointermove', function (e) {
        if (!dragging) return;
        targetYaw += (e.clientX - lastX) * .008;
        targetPitch = Math.max(-.6, Math.min(.9, targetPitch - (e.clientY - lastY) * .006));
        lastX = e.clientX; lastY = e.clientY;
      });
      var up = function () { dragging = false; el.style.cursor = 'grab'; };
      el.addEventListener('pointerup', up);
      el.addEventListener('pointercancel', up);
      el.addEventListener('pointerleave', up);

      host.setAttribute('tabindex', '0');
      host.setAttribute('role', 'application');
      host.setAttribute('aria-label', "Modèle 3D d'un implant dentaire dans l'os. Faites glisser ou utilisez les flèches pour le faire tourner.");
      host.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowLeft') { auto = false; targetYaw -= .18; }
        else if (e.key === 'ArrowRight') { auto = false; targetYaw += .18; }
        else if (e.key === 'ArrowUp') { auto = false; targetPitch = Math.min(.9, targetPitch + .12); }
        else if (e.key === 'ArrowDown') { auto = false; targetPitch = Math.max(-.6, targetPitch - .12); }
        else return;
        e.preventDefault();
      });

      window.addEventListener('resize', function () {
        var nw = host.clientWidth, nh = host.clientHeight;
        camera.aspect = nw / nh; camera.updateProjectionMatrix(); renderer.setSize(nw, nh);
      });

      var R = 7.8;
      (function tick() {
        if (auto) targetYaw += .0022;
        yaw += (targetYaw - yaw) * .12;
        pitch += (targetPitch - pitch) * .12;
        camera.position.set(Math.sin(yaw) * R * Math.cos(pitch), Math.sin(pitch) * R + .6, Math.cos(yaw) * R * Math.cos(pitch));
        camera.lookAt(0, .1, 0);
        renderer.render(scene, camera);
        requestAnimationFrame(tick);
      })();
    });
  }

  if (host) {
    var started = false;
    var start = function () {
      if (started) return;
      started = true;
      initThree().catch(threeFail);
    };
    if ('IntersectionObserver' in window) {
      var tio = new IntersectionObserver(function (entries) {
        if (entries.some(function (e) { return e.isIntersecting; })) { tio.disconnect(); start(); }
      }, { rootMargin: '400px' });
      tio.observe(host);
      setTimeout(function () {
        if (!host.querySelector('canvas')) { tio.disconnect(); start(); }
      }, 5000);
    } else {
      start();
    }
  }
})();

/* Cartes soins : fondu entre plusieurs photos + points de navigation, seulement quand la carte est visible */
(function () {
  var figs = document.querySelectorAll('[data-slides]');
  if (!figs.length) return;
  figs.forEach(function (fig) {
    var imgs = fig.querySelectorAll('img'), i = 0, timer = null;
    if (imgs.length < 2) return;
    var dots = document.createElement('div');
    dots.className = 's-dots';
    dots.setAttribute('role', 'tablist');
    dots.setAttribute('aria-label', 'Photos');
    var btns = [];
    imgs.forEach(function (img, k) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 's-dot' + (k === 0 ? ' is-on' : '');
      b.setAttribute('aria-label', 'Photo ' + (k + 1) + ' sur ' + imgs.length);
      b.addEventListener('click', function () { go(k); stop(); start(); });
      dots.appendChild(b); btns.push(b);
    });
    fig.appendChild(dots);
    function go(n) {
      imgs[i].classList.remove('is-on'); btns[i].classList.remove('is-on');
      i = n; imgs[i].classList.add('is-on'); btns[i].classList.add('is-on');
    }
    function step() { go((i + 1) % imgs.length); }
    function start() { if (!timer) timer = setInterval(step, 2400); }
    function stop() { clearInterval(timer); timer = null; }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { es[0].isIntersecting ? start() : stop(); }, { threshold: 0.25 }).observe(fig);
    } else start();
  });
})();


/* Pages traitement : étiquettes flottantes + demande de rendez-vous envoyée sur WhatsApp */
(function () {
  var form = document.getElementById('tp-form');
  if (!form) return;
  form.querySelectorAll('.tp-field').forEach(function (f) {
    var inp = f.querySelector('.tp-input');
    var sync = function () { f.classList.toggle('is-active', document.activeElement === inp || inp.value.trim() !== ''); };
    ['focus', 'blur', 'input'].forEach(function (ev) { inp.addEventListener(ev, sync); });
    sync();
  });
  var err = document.getElementById('tp-form-err');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var nom = form.nom.value.trim();
    var tel = form.tel.value.trim();
    var ok = nom.length >= 2 && tel.replace(/\D/g, '').length >= 9;
    err.hidden = ok;
    if (!ok) { (nom.length < 2 ? form.nom : form.tel).focus(); return; }
    var prio = [].map.call(form.querySelectorAll('input[name="priorite"]:checked'), function (c) { return c.value; }).join(', ');
    var lines = ['Bonjour, je souhaite un rendez-vous.', 'Nom : ' + nom, 'Téléphone : ' + tel];
    if (form.email.value.trim()) lines.push('E-mail : ' + form.email.value.trim());
    if (form.traitement.value) lines.push('Traitement : ' + form.traitement.value);
    lines.push('Disponibilité : ' + form.quand.value);
    if (prio) lines.push('Priorité : ' + prio);
    if (form.motif.value.trim()) lines.push('Motif : ' + form.motif.value.trim());
    lines.push('Page : ' + document.title.split('|')[0].trim());
    window.open('https://wa.me/212636432214?text=' + encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
  });
})();

/* Visionneuse photos : liens [data-lightbox] groupés, flèches, miniatures, clavier, fermeture au clic sur le fond */
(function () {
  var links = [].slice.call(document.querySelectorAll('a[data-lightbox]'));
  if (!links.length) return;
  var lb = document.createElement('div');
  lb.className = 'lb'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', 'Galerie photos'); lb.hidden = true;
  lb.innerHTML =
    '<div class="lb-view"><img alt=""></div>' +
    '<button class="lb-btn lb-prev" type="button" aria-label="Photo précédente"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M15 6l-6 6l6 6"/></svg></button>' +
    '<button class="lb-btn lb-next" type="button" aria-label="Photo suivante"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6l-6 6"/></svg></button>' +
    '<button class="lb-btn lb-close" type="button" aria-label="Fermer"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6l-12 12"/><path d="M6 6l12 12"/></svg></button>' +
    '<div class="lb-top"><span class="lb-count mono" aria-live="polite"></span><span class="lb-cap"></span></div>' +
    '<div class="lb-strip" role="tablist"></div>';
  document.body.appendChild(lb);
  var img = lb.querySelector('.lb-view img'), strip = lb.querySelector('.lb-strip');
  var prev = lb.querySelector('.lb-prev'), next = lb.querySelector('.lb-next'), close = lb.querySelector('.lb-close');
  var count = lb.querySelector('.lb-count'), cap = lb.querySelector('.lb-cap'), view = lb.querySelector('.lb-view');
  var group = [], idx = 0, lastFocus = null;

  function show(i) {
    var dir = i > idx ? 'is-next' : (i < idx ? 'is-prev' : '');
    idx = i;
    img.classList.remove('is-swap', 'is-next', 'is-prev'); void img.offsetWidth;
    img.src = group[i].href; img.alt = (group[i].querySelector('img') || {}).alt || '';
    img.classList.add('is-swap'); if (dir) img.classList.add(dir);
    prev.disabled = i === 0; next.disabled = i === group.length - 1;
    count.textContent = (i + 1) + ' / ' + group.length;
    cap.textContent = img.alt;
    strip.querySelectorAll('button').forEach(function (b, k) {
      b.classList.toggle('is-active', k === i); b.setAttribute('aria-selected', k === i);
      if (k === i) strip.scrollTo({ left: b.offsetLeft - (strip.clientWidth - b.offsetWidth) / 2, behavior: 'smooth' });
    });
  }
  function open(link) {
    var name = link.getAttribute('data-lightbox');
    group = links.filter(function (l) { return l.getAttribute('data-lightbox') === name; });
    strip.innerHTML = '';
    group.forEach(function (l, k) {
      var b = document.createElement('button'); b.type = 'button'; b.setAttribute('role', 'tab'); b.setAttribute('aria-label', 'Photo ' + (k + 1));
      var t = document.createElement('img'); t.src = l.href; t.alt = ''; b.appendChild(t);
      b.addEventListener('click', function () { show(k); });
      strip.appendChild(b);
    });
    lastFocus = document.activeElement;
    lb.hidden = false; setTimeout(function () { lb.classList.add('is-open'); }, 20);
    if (window.cdcLenis) window.cdcLenis.stop();
    document.body.style.overflow = 'hidden';
    idx = -1; show(group.indexOf(link)); close.focus();
  }
  function shut() {
    lb.classList.remove('is-open');
    setTimeout(function () { lb.hidden = true; img.src = ''; }, 300);
    if (window.cdcLenis) window.cdcLenis.start();
    document.body.style.overflow = '';
    if (lastFocus) lastFocus.focus();
  }
  links.forEach(function (l) { l.addEventListener('click', function (e) { e.preventDefault(); open(l); }); });
  prev.addEventListener('click', function () { if (idx > 0) show(idx - 1); });
  next.addEventListener('click', function () { if (idx < group.length - 1) show(idx + 1); });
  close.addEventListener('click', shut);
  lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('lb-view')) shut(); });
  document.addEventListener('keydown', function (e) {
    if (lb.hidden) return;
    if (e.key === 'Escape') shut();
    else if (e.key === 'ArrowLeft' && idx > 0) show(idx - 1);
    else if (e.key === 'ArrowRight' && idx < group.length - 1) show(idx + 1);
  });
  var sx = 0, sy = 0;
  view.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
  view.addEventListener('touchend', function (e) {
    var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
    if (Math.abs(dx) < 50 || Math.abs(dx) < Math.abs(dy)) return;
    if (dx > 0 && idx > 0) show(idx - 1); else if (dx < 0 && idx < group.length - 1) show(idx + 1);
  });
})();

/* Texte courbe « Prendre rendez-vous » : comme la référence, pas de défilement infini.
   Entrée : le bandeau descend de 80 px et passe de 1,4 à 1 (0,45 s) quand il atteint 67 % de l'écran ;
   il revient à l'état initial une fois sorti de l'écran, pour rejouer l'entrée au prochain passage. */
(function () {
  var svgs = document.querySelectorAll('[data-arc]');
  if (!svgs.length || !window.gsap || !window.ScrollTrigger) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  svgs.forEach(function (svg) {
    var reset = function () { gsap.set(svg, { y: -80, scale: 1.4, transformOrigin: '50% 50%', overwrite: true }); };
    var play = function () { gsap.to(svg, { y: 0, scale: 1, duration: 0.45, delay: 0.12, ease: 'power2.inOut', overwrite: true }); };
    reset();
    ScrollTrigger.create({ trigger: svg, start: 'top 67%', end: 'bottom top', onEnter: play, onEnterBack: play });
    ScrollTrigger.create({ trigger: svg, start: 'top bottom', end: 'bottom top', onLeave: reset, onLeaveBack: reset });
  });
})();

/* Menu « priorité » : se ferme au clic extérieur et avec Échap, comme un menu déroulant classique */
(function () {
  var dd = document.querySelector('.tp-dd');
  if (!dd) return;
  document.addEventListener('click', function (e) { if (dd.open && !dd.contains(e.target)) dd.open = false; });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && dd.open) { dd.open = false; dd.querySelector('summary').focus(); } });
})();

/* 4. Projecteur : la lumière suit le curseur sur la carte survolée (souris uniquement) */
(function () {
  if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.querySelectorAll('.s-card').forEach(function (card) {
    card.addEventListener('pointermove', function (e) {
      var r = card.getBoundingClientRect();
      card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      card.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });
})();

/* Pages contact, blog, équipements : accordéons numérotés, héros au scroll */
(function () {
  document.querySelectorAll('.cf-acc-t').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var acc = btn.closest('.cf-acc'), open = !acc.classList.contains('is-open');
      acc.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  if (!window.gsap || !window.ScrollTrigger) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  /* héro contact / blog : comme la référence, au scroll la photo zoome de 1 à 1,2 et le titre remonte de 112 px */
  var heroSec = document.querySelector('.cf-hero');
  if (heroSec) {
    gsap.fromTo('.cf-hero-bg', { scale: 1 }, { scale: 1.2, ease: 'none', scrollTrigger: { trigger: heroSec, start: 'top top', end: '+=400', scrub: true } });
    gsap.fromTo('.cf-hero-title', { y: 0 }, { y: -112, ease: 'none', scrollTrigger: { trigger: heroSec, start: 'top top', end: '+=425', scrub: true } });
  }

  /* bandeau « Trouver le cabinet » : titre et lien glissent, médaillons grossissent */
  var map = document.querySelector('.cf-map');
  if (map) {
    var st = { trigger: map, start: 'top bottom', end: 'center center', scrub: true };
    gsap.fromTo('[data-cf-left]', { x: 80 }, { x: 0, ease: 'none', scrollTrigger: st });
    gsap.fromTo('[data-cf-right]', { x: -80 }, { x: 0, ease: 'none', scrollTrigger: st });
    gsap.fromTo('[data-cf-pics]', { scale: 0.7 }, { scale: 1, ease: 'none', scrollTrigger: st });
  }

  /* héro d'article : léger zoom de la photo au scroll */
  var ar = document.querySelector('.ar-hero');
  if (ar) {
    gsap.fromTo('.ar-hero-bg', { scale: 1 }, { scale: 1.12, ease: 'none', scrollTrigger: { trigger: ar, start: 'top top', end: 'bottom top', scrub: true } });
  }

  /* héro équipements : la photo s'éclaircit, le titre s'efface, trois mots montent, puis la carte se réduit */
  var stack = document.querySelector('[data-eq-stack]');
  if (stack) {
    var tl = gsap.timeline({ scrollTrigger: { trigger: stack, start: 'top top', end: 'bottom bottom', scrub: true } });
    tl.fromTo('[data-eq-bg]', { opacity: 0.5 }, { opacity: 1, ease: 'none', duration: 0.3 }, 0)
      .fromTo('[data-eq-title]', { y: 0, opacity: 1 }, { y: -65, opacity: 0, ease: 'none', duration: 0.3 }, 0)
      .fromTo('[data-eq-word]', { y: 80, opacity: 0 }, { y: 0, opacity: 1, ease: 'power2.out', duration: 0.22, stagger: 0.1 }, 0.3)
      .fromTo('[data-eq-card]', { scale: 1 }, { scale: 0.8, ease: 'none', duration: 0.28 }, 0.72);
  }

  /* cartes équipements : entrée en léger zoom */
  gsap.utils.toArray('[data-eq-item]').forEach(function (item) {
    gsap.fromTo(item, { scale: 0.92, opacity: 0.4 }, { scale: 1, opacity: 1, ease: 'none',
      scrollTrigger: { trigger: item, start: 'top bottom', end: 'top 62%', scrub: true } });
  });
})();

/* Page /soins/ : carrousel (flèches, clavier, balayage) + héro qui s'efface au scroll */
(function () {
  var slider = document.querySelector('[data-st-slider]');
  if (slider) {
    var track = slider.querySelector('[data-st-track]');
    var slides = [].slice.call(slider.querySelectorAll('.st-slide'));
    var i = 0, n = slides.length;
    var go = function (k) {
      i = (k + n) % n;
      slides.forEach(function (s, j) {
        var on = j === i;
        s.classList.toggle('is-active', on);
        if (on) s.removeAttribute('aria-hidden'); else s.setAttribute('aria-hidden', 'true');
        s.querySelectorAll('a, input').forEach(function (a) { if (on) a.removeAttribute('tabindex'); else a.setAttribute('tabindex', '-1'); });
      });
      var cur = slider.querySelector('[data-st-cur]'); if (cur) cur.textContent = (i < 9 ? '0' : '') + (i + 1);
    };
    slider.querySelector('[data-st-prev]').addEventListener('click', function () { go(i - 1); });
    slider.querySelector('[data-st-next]').addEventListener('click', function () { go(i + 1); });
    slider.addEventListener('keydown', function (e) {
      if (e.target.classList && e.target.classList.contains('ba-range')) return; /* les flèches pilotent la comparaison */
      if (e.key === 'ArrowLeft') { go(i - 1); } else if (e.key === 'ArrowRight') { go(i + 1); }
    });
  }

  var hero = document.querySelector('.st-hero');
  if (!hero || !window.gsap || !window.ScrollTrigger) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  /* comme la référence : la photo zoome, le titre et la preuve sociale remontent de 112 px en s'effaçant */
  gsap.fromTo('.st-hero-bg', { scale: 1 }, { scale: 1.2, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: '+=600', scrub: true } });
  gsap.fromTo('.st-hero-l', { y: 0, opacity: 1 }, { y: -112, opacity: 0, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: '+=710', scrub: true } });
  gsap.fromTo('.st-hero-r', { y: 0, opacity: 1 }, { y: -112, opacity: 0, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top-=175', end: '+=710', scrub: true } });

  /* grille : toutes les cartes glissent depuis la droite (2rem) en cascade quand la grille atteint 67 % de l'écran */
  var grid = document.querySelector('.st-grid');
  if (grid) {
    gsap.fromTo(grid.querySelectorAll('.st-card'), { x: 32, opacity: 0 }, {
      x: 0, opacity: 1, duration: 0.6, ease: 'power2.out', stagger: 0.1,
      scrollTrigger: { trigger: grid, start: 'top 67%', once: true }
    });
  }
})();

/* Bandeau « Prendre rendez-vous » (toutes les pages) : titre, lien et liste montent de 2rem en grandissant de 0,8 à 1,
   rejoué à chaque passage comme la référence */
(function () {
  var cta = document.querySelector('.tp-cta');
  if (!cta || !window.gsap || !window.ScrollTrigger) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var items = cta.querySelectorAll('.tp-cta-copy > *, .tp-cta-faces img, .tp-cta-list li');
  gsap.set(items, { y: 32, scale: 0.8, opacity: 0 });
  ScrollTrigger.create({
    trigger: cta, start: 'top 80%', end: 'bottom top',
    onEnter: function () { gsap.to(items, { y: 0, scale: 1, opacity: 1, duration: 0.7, ease: 'power2.out', stagger: 0.08, overwrite: true }); },
    onEnterBack: function () { gsap.to(items, { y: 0, scale: 1, opacity: 1, duration: 0.7, ease: 'power2.out', stagger: 0.08, overwrite: true }); },
    onLeaveBack: function () { gsap.set(items, { y: 32, scale: 0.8, opacity: 0, overwrite: true }); }
  });
})();

/* Page « Le cabinet » : animations de la page /about de la référence */
(function () {
  if (!document.querySelector('.ab-hero')) return;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var G = window.gsap && window.ScrollTrigger && !reduced;

  /* découpe d'un texte en lignes réelles (masque + ligne), refaite si la largeur change */
  var esc = function (s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;'); };
  function split(el) {
    var text = el.getAttribute('data-ab-text');
    if (!text) { text = el.textContent.replace(/\s+/g, ' ').trim(); el.setAttribute('data-ab-text', text); }
    el.innerHTML = text.split(' ').map(function (w) { return '<span class="ab-w">' + esc(w) + '</span>'; }).join(' ');
    var lines = [], top = null;
    el.querySelectorAll('.ab-w').forEach(function (w) {
      if (top === null || Math.abs(w.offsetTop - top) > 2) { lines.push([]); top = w.offsetTop; }
      lines[lines.length - 1].push(esc(w.textContent));
    });
    el.innerHTML = lines.map(function (l, i) { return '<span class="ab-line"><span class="ab-line-in" style="--i:' + i + '">' + l.join(' ') + '</span></span>'; }).join('');
  }
  var splits = [].slice.call(document.querySelectorAll('[data-ab-split]'));
  splits.forEach(split);
  var afterSplit = function () {};
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { splits.forEach(split); afterSplit(); });

  /* héro : fondu enchaîné (l'image entrante grandit de 0,8 à 1, la sortante de 1 à 1,2), vignettes cliquables */
  var hero = document.querySelector('[data-ab-hero]');
  var imgs = [].slice.call(hero.querySelectorAll('.ab-hero-img'));
  var thumbs = [].slice.call(hero.querySelectorAll('.ab-thumb'));
  var cur = 0, timer = null;
  function show(k) {
    if (k === cur) return;
    var old = imgs[cur];
    old.classList.remove('is-active'); old.classList.add('is-leaving');
    setTimeout(function () { old.classList.remove('is-leaving'); }, 1300);
    cur = k; imgs[cur].classList.add('is-active');
    thumbs.forEach(function (t, j) { t.classList.toggle('is-active', j === cur); t.setAttribute('aria-pressed', j === cur ? 'true' : 'false'); });
  }
  function auto() { clearInterval(timer); if (!reduced) timer = setInterval(function () { show((cur + 1) % imgs.length); }, 4500); }
  thumbs.forEach(function (t, j) { t.addEventListener('click', function () { show(j); auto(); }); });
  auto();

  if (!G) return;

  /* héro : au chargement, chaque ligne du titre monte de 32 px en apparaissant, 0,1 s d'écart (comme la référence) */
  gsap.fromTo(hero.querySelectorAll('.ab-hl'), { y: 32, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power2.out', stagger: 0.1, delay: 0.15 });

  /* adresse : la photo dézoome de 1,1 à 1 pendant qu'elle entre à l'écran */
  var lieuSec = document.querySelector('.lieu');
  if (lieuSec) gsap.fromTo(lieuSec.querySelector('.lieu-bg'), { scale: 1.1 }, { scale: 1, ease: 'none', scrollTrigger: { trigger: lieuSec, start: 'top bottom', end: 'top 30%', scrub: true } });

  /* approche : étiquette (8rem) et lignes (4rem) montent à l'entrée, redescendent quand la section sort par le haut */
  var ap = document.querySelector('.ab-approach');
  if (ap) {
    var label = ap.querySelector('[data-ab-label]');
    var shown = false;
    var hide = function () { gsap.set(label, { y: 128 }); gsap.set(ap.querySelectorAll('.ab-line-in'), { y: 64, opacity: 0 }); };
    var play = function () { shown = true; gsap.to(label, { y: 0, duration: 0.9, ease: 'power3.out', overwrite: true });
      gsap.to(ap.querySelectorAll('.ab-line-in'), { y: 0, opacity: 1, duration: 0.9, ease: 'power3.out', stagger: 0.08, overwrite: true }); };
    var back = function () { shown = false; gsap.to(label, { y: 128, duration: 0.6, ease: 'power2.in', overwrite: true });
      gsap.to(ap.querySelectorAll('.ab-line-in'), { y: 64, opacity: 0, duration: 0.6, ease: 'power2.in', stagger: 0.04, overwrite: true }); };
    hide();
    afterSplit = function () { if (!shown) gsap.set(ap.querySelectorAll('.ab-line-in'), { y: 64, opacity: 0 }); else gsap.set(ap.querySelectorAll('.ab-line-in'), { y: 0, opacity: 1 }); };
    ScrollTrigger.create({ trigger: ap, start: 'top 60%', end: 'bottom top', onEnter: play, onLeave: back, onEnterBack: play, onLeaveBack: back });
    var w = window.innerWidth;
    window.addEventListener('resize', function () {
      if (window.innerWidth === w) return; w = window.innerWidth;
      splits.forEach(split); afterSplit();
    });
  }

  /* le centre : cartes qui montent de 5rem, liste en cascade, pastilles qui glissent, photo qui dézoome */
  var bento = document.querySelector('.ab-bento');
  if (bento) {
    var st = { trigger: bento, start: 'top 75%', once: true };
    gsap.fromTo(bento.querySelectorAll('[data-ab-in]'), { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.9, ease: 'power3.out', stagger: 0.1, scrollTrigger: st });
    gsap.fromTo(bento.querySelectorAll('.ab-spec'), { y: 48, opacity: 0 }, { y: 0, opacity: 1, duration: 0.7, ease: 'power3.out', stagger: 0.07, delay: 0.25, scrollTrigger: st });
    gsap.fromTo(bento.querySelectorAll('.ab-circle'), { x: 16, opacity: 0 }, { x: 0, opacity: 1, duration: 0.7, ease: 'power3.out', stagger: 0.1, delay: 0.35, scrollTrigger: st });
    gsap.fromTo(bento.querySelector('.ab-cover'), { scale: 1.3 }, { scale: 1, duration: 1.4, ease: 'power3.out', delay: 0.2, scrollTrigger: st });
  }


  /* plateau technique : la grande photo arrive de la droite en grandissant, les vignettes de la gauche */
  var tech = document.querySelector('.ab-tech');
  if (tech) {
    var st2 = { trigger: tech, start: 'top 70%', once: true };
    gsap.fromTo('[data-ab-main]', { xPercent: 50, scale: 0.7, opacity: 0.5 }, { xPercent: 0, scale: 1, opacity: 1, duration: 1.1, ease: 'power3.out', scrollTrigger: st2 });
    gsap.fromTo('[data-ab-thumbs]', { xPercent: -10, scale: 0.8, opacity: 0 }, { xPercent: 0, scale: 1, opacity: 1, duration: 1.1, ease: 'power3.out', delay: 0.1, scrollTrigger: st2 });
  }

  /* le cabinet : cartes qui glissent depuis la droite (3rem) */
  var team = document.querySelector('.ab-team-grid');
  if (team) gsap.fromTo(team.querySelectorAll('.ab-member'), { x: 48, opacity: 0 }, { x: 0, opacity: 1, duration: 0.8, ease: 'power3.out', stagger: 0.1, scrollTrigger: { trigger: team, start: 'top 80%', once: true } });
})();

/* Comparaison avant / après : un curseur natif invisible couvre l'image (souris, doigt, clavier) */
(function () {
  document.querySelectorAll('[data-ba]').forEach(function (ba) {
    var r = ba.querySelector('.ba-range');
    var set = function () { ba.style.setProperty('--p', r.value + '%'); };
    r.addEventListener('input', set);
    r.addEventListener('pointerdown', function () { ba.classList.add('is-drag'); });
    ['pointerup', 'pointercancel', 'blur'].forEach(function (ev) { r.addEventListener(ev, function () { ba.classList.remove('is-drag'); }); });
    set();
  });
})();

/* Bloc « Prenez rendez-vous » (blog) : l'anneau tourne tout seul en continu (animation CSS .ab-ring) */

/* « Prenez rendez-vous » (blog) : les photos partent du centre de la section (échelle 0,1) et rejoignent leur place
   pendant que la section entre à l'écran, comme la référence */
(function () {
  var sec = document.querySelector('[data-fl]');
  if (!sec || !window.gsap || !window.ScrollTrigger) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  gsap.utils.toArray(sec.querySelectorAll('.fl-img')).forEach(function (el) {
    var off = function (axis) {
      var s = sec.getBoundingClientRect(), r = el.getBoundingClientRect();
      /* position de départ : le centre de la section (mesuré sans la transformation en cours) */
      var t = gsap.getProperty(el, axis === 'x' ? 'x' : 'y');
      return axis === 'x' ? (s.left + s.width / 2) - (r.left + r.width / 2) + t : (s.top + s.height / 2) - (r.top + r.height / 2) + t;
    };
    gsap.fromTo(el, { x: function () { return off('x'); }, y: function () { return off('y'); }, scale: 0.1 },
      { x: 0, y: 0, scale: 1, ease: 'none', immediateRender: true,
        scrollTrigger: { trigger: sec, start: 'top bottom', end: 'top 45%', scrub: 1 } });
  });
})();
