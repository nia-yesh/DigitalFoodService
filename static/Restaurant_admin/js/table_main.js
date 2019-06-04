var tables=document.getElementsByClassName("card-img-overlay");
var i;
for(i=0;i<tables.length;i++){
    if(tables[i].dataset.av=="False"){
        tables[i].setAttribute("class","card-img-overlay bg-danger pulse");
    }
    else{
        tables[i].setAttribute("class", "card-img-overlay bg-success pulse");
    }
}

var text;
function myFunction(event){
text=event.target.dataset.link;
    document.getElementById("sahand").href="Table_delete/"+text;
}
document.getElementById("id_table_number").setAttribute("class", "form-control");
document.getElementById("id_table_availability").setAttribute("class", "form-check-input");