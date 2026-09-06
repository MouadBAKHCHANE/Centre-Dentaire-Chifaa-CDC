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
    toggle.addEventListener('click', function () {
      var paused = vid.paused;
      if (paused) vid.play(); else vid.pause();
      toggle.setAttribute('aria-pressed', paused ? 'false' : 'true');
      toggle.setAttribute('aria-label', paused ? 'Mettre la vidéo en pause' : 'Lire la vidéo');
    });
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
    function start() { if (!timer) timer = setInterval(step, 3200); }
    function stop() { clearInterval(timer); timer = null; }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { es[0].isIntersecting ? start() : stop(); }, { threshold: 0.25 }).observe(fig);
    } else start();
  });
})();
