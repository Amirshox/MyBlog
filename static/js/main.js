document.addEventListener('keydown', e => {
    const el = document.querySelector('#input');
    if (e.keyCode === 191 && el !== document.activeElement) {
        e.preventDefault();
        el.focus();
    }
});