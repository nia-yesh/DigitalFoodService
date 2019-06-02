// // When the user scrolls the page, execute myFunction
// window.onscroll = function() {myFunction2(),myFunction3()};
//
// // Get the header
// var header = document.getElementById("myHeader");
// var navi=document.getElementById("myTopnav");
// // Get the offset position of the navbar
// var sticky = header.offsetTop;
// var sticky2=navi.offsetTop;
//
// // Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
// function myFunction2() {
// if (window.pageYOffset > sticky) {
// header.classList.add("sticky");
// } else {
// header.classList.remove("sticky");
// }
// }
// function myFunction3() {
// if (window.pageYOffset > sticky2) {
// navi.classList.add("sticky2");
// } else {
// navi.classList.remove("sticky2");
// }
// }
// /* Toggle between adding and removing the "responsive" class to topnav when the user clicks on the icon */
// function myFunction() {
//   var x = document.getElementById("myTopnav");
//   if (x.className === "topnav") {
//     x.className += " responsive";
//   }
//   else if (x.className === "topnav sticky2") {
//     x.className+= " responsive";
//   }
//    else {
//     x.className = "topnav sticky2";
//   }
// }
//
// function myFunction4() {
//   var x = document.getElementsByClassName("topnav sticky2");
//   if (x.className === "topnav sticky2") {
//     x.className += " responsive";
//   } else {
//     x.className = "topnav sticky2";
//   }
// }
var buttons = document.getElementById('plus');

Array.prototype.forEach.call(buttons, function (b) {
    b.addEventListener('click', createRipple);
});


function createRipple (e) {
		// alert('x');
    var circle = document.createElement('div');
    this.appendChild(circle);

    var d = Math.max(this.clientWidth, this.clientHeight);

    circle.style.width = circle.style.height = d + 'px';

var rect = this.getBoundingClientRect();
circle.style.left = e.clientX - rect.left -d/2 + 'px';
circle.style.top = e.clientY - rect.top - d/2 + 'px';
circle.classList.add('ripple');

	setTimeout(function(){
		circle.remove();
	},500);
}
