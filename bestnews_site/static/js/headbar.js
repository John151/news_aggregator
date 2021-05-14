
let skyline = document.getElementById("skyline")
let baloons = document.getElementById("baloons")
let title = document.getElementById("title")
// let navbar = document.getElementById("navbar")

window.addEventListener('scroll', function(){
    let value = window.scrollY;
    skyline.style.top = value * 0.5 + 'px';
    baloons.style.left = -value * 0.5 + 'px';
    title.style.top = value * 1 + 'px';
    // navbar.style.top = value * .9 + 'px';

})