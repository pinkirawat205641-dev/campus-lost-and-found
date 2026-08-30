/* ==========================================================================
   College Campus Lost & Found System — interface behaviour
   --------------------------------------------------------------------------
   Four independent concerns, each guarded so that a page which does not
   contain the relevant element is unaffected:
     1. Navigation drawer (modal below 1024 px)
     2. Photograph upload — reflect the chosen filename back to the user
     3. Snackbars — manual dismissal and automatic timeout
     4. Destructive submissions — disable the button to prevent double posts
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {

    /* ------------------------- 1. NAVIGATION DRAWER --------------------- */
    var toggle = document.getElementById('drawerToggle');
    var scrim  = document.getElementById('drawerScrim');
    var drawer = document.getElementById('navDrawer');

    function setDrawer(open) {
        document.body.classList.toggle('drawer-open', open);
        if (toggle) { toggle.setAttribute('aria-expanded', open ? 'true' : 'false'); }
    }

    if (toggle && drawer) {
        toggle.addEventListener('click', function () {
            setDrawer(!document.body.classList.contains('drawer-open'));
        });
    }

    if (scrim) {
        scrim.addEventListener('click', function () { setDrawer(false); });
    }

    // Escape closes the modal drawer, as expected of a modal surface.
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') { setDrawer(false); }
    });

    // Returning to a wide viewport must not leave the scrim visible.
    window.addEventListener('resize', function () {
        if (window.innerWidth > 1024) { setDrawer(false); }
    });

    /* ---------------------- 2. PHOTOGRAPH UPLOAD ------------------------ */
    var fileInput = document.querySelector('.file-input');
    if (fileInput) {
        fileInput.addEventListener('change', function () {
            var label = document.querySelector('.file-upload__text');
            if (!label) { return; }
            if (this.files && this.files.length > 0) {
                var file = this.files[0];
                var sizeKb = Math.round(file.size / 1024);
                label.textContent = file.name + ' (' + sizeKb + ' KB)';
                label.style.fontWeight = '500';
            } else {
                label.textContent = 'Click to choose a photograph';
                label.style.fontWeight = '';
            }
        });
    }

    /* --------------------------- 3. SNACKBARS --------------------------- */
    function dismiss(alert) {
        alert.style.opacity = '0';
        setTimeout(function () { alert.remove(); }, 250);
    }

    document.querySelectorAll('.alert').forEach(function (alert) {
        var close = alert.querySelector('.alert__close');
        if (close) {
            close.addEventListener('click', function () { dismiss(alert); });
        }
        setTimeout(function () { dismiss(alert); }, 6000);
    });

    /* -------------------- 4. DESTRUCTIVE SUBMISSIONS -------------------- */
    // The confirm() dialogue is declared inline on the form; once it has been
    // accepted the button is disabled so the request cannot be sent twice.
    document.querySelectorAll('form[onsubmit]').forEach(function (form) {
        form.addEventListener('submit', function () {
            var button = form.querySelector('button[type="submit"]');
            if (button) {
                button.disabled = true;
                button.style.opacity = '0.6';
            }
        });
    });
});
