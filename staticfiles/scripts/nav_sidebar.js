
const navbarButtonEl = document.querySelector('.navbar-toggler');
const navbarCollapseEl = document.querySelector('.navbar-collapse');
navbarButtonEl.addEventListener('click', onClickNavbarButton);

function onClickNavbarButton() {
    console.log('onClickNavbarButton')
    navbarCollapseEl.classList.toggle('show')
}