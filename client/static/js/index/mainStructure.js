document.getElementsByClassName('close-menu')[0].addEventListener('click', function(){
    document.getElementsByClassName('menu-suspend-modal')[0].style.display = 'none';
})

document.getElementsByClassName('btn-menu')[0].addEventListener('click', function(){
    document.getElementsByClassName('menu-suspend-modal')[0].style.display = 'flex';
})