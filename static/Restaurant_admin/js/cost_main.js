var text;
function myFunction(event){
text=event.target.dataset.food;
    document.getElementById("sahand").href="Cost_delete/"+text;
}