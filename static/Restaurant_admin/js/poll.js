
var text;
function myFunction(event){
text=event.target.dataset.poll;
    document.getElementById("sahand").href="Poll_delete/"+text;
}