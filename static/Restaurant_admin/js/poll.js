window.onscroll = function() {myFunction()};

var header = document.getElementById("myHeader");
var sticky = header.offsetTop;

function myFunction() {
  if (window.pageYOffset > sticky) {
    header.classList.add("sticky");
  } else {
    header.classList.remove("sticky");
  }
}
var text;
function myFunction(event){
text=event.target.dataset.poll;
    document.getElementById("sahand").href="Poll_delete/"+text;
}