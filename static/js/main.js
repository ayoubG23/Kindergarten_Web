/* ============================================================
   روضة البراعم – El Baraem Kindergarten
   Main JavaScript
   Linked from: templates/index.html  (loaded at bottom of <body>)
   ============================================================ */

/* ── 1. Set current year in footer ────────────────────────── */
document.getElementById('year').textContent = new Date().getFullYear();


/* ── 2. Mobile nav toggle ──────────────────────────────────── */
const navToggle = document.getElementById('navToggle');
const navLinks  = document.getElementById('navLinks');

// Toggle the .open class to show/hide the mobile menu
navToggle.addEventListener('click', () => {
  navLinks.classList.toggle('open');
});

// Auto-close the nav when any link inside it is clicked
navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => navLinks.classList.remove('open'));
});


/* ── 3. Scroll-reveal animation ────────────────────────────── */
/*
 * IntersectionObserver watches every element with class .reveal.
 * When an element scrolls into view (12% visible), it gets the
 * .visible class, which triggers the CSS fade+slide transition.
 * observer.unobserve() ensures the animation fires only once.
 */
const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target); // animate only once
      }
    });
  },
  { threshold: 0.12 } // fire when 12 % of the element is visible
);

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));


/* ── 4. Contact form submission ────────────────────────────── */
/*
 * Reads the three form fields, validates them, then POSTs JSON
 * to the FastAPI route /api/contact.
 * Displays a success or error message inside #form-msg.
 *
 * To add real notifications (email, WhatsApp), edit main.py.
 */
async function sendContact() {
  const name    = document.getElementById('name').value.trim();
  const phone   = document.getElementById('phone').value.trim();
  const message = document.getElementById('message').value.trim();
  const msgEl   = document.getElementById('form-msg');
  const btn     = document.getElementById('sendBtn');

  // ── Validation: name and phone are required ──
  if (!name || !phone) {
    msgEl.className = 'error';
    msgEl.textContent = 'الرجاء تعبئة الاسم ورقم الهاتف على الأقل.';
    return;
  }

  // ── Show loading state on the submit button ──
  btn.disabled = true;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> جاري الإرسال...';

  try {
    // POST JSON payload to the FastAPI endpoint
    const res = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, phone, message }),
    });

    const data = await res.json();

    if (data.success) {
      // ── Success: show bilingual confirmation, clear fields ──
      msgEl.className = 'success';
      msgEl.textContent = data.message_ar + '  ' + data.message_fr;

      document.getElementById('name').value    = '';
      document.getElementById('phone').value   = '';
      document.getElementById('message').value = '';
    } else {
      throw new Error('Server returned success: false');
    }

  } catch (err) {
    // ── Error: show bilingual error message ──
    msgEl.className = 'error';
    msgEl.textContent = 'حدث خطأ، يرجى المحاولة مجدداً. / Une erreur est survenue, réessayez.';
    console.error('[Contact form error]', err);

  } finally {
    // ── Always restore the button, success or failure ──
    btn.disabled = false;
    btn.innerHTML = '<i class="fas fa-paper-plane"></i>&nbsp;إرسال الرسالة';
  }
}
