var temp=document.getElementsByClassName("isav");
var i;
for ( i = 0; i < temp.length; i++) {
    if(temp[i].innerHTML==" True"){
        temp[i].innerHTML="موجود";
    }
        else{
            temp[i].innerHTML="ناموجود";
            temp[i].previousElementSibling.setAttribute("class", "fas fa-times");
        }
    
}
var text;
function myFunction(event){
text=event.target.dataset.food;
    document.getElementById("sahand").href="Food_delete/"+text;
}
document.getElementById("id_food_availability").setAttribute("class", "form-check-input");
document.getElementById("id_food_name","id_cost").setAttribute("class", "form-control");
document.getElementById("id_food_details").setAttribute("class", "form-control");
document.getElementById("id_cost").setAttribute("class", "form-control");

// document.getElementById("id_food_availability").append("checked");
document.getElementById("id_food_category").setAttribute("class", "mdb-select md-form");
// Material Select Initialization



