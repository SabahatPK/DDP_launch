

$(document).ready(function(){
    alert("Noman")
    var province_names = ["Federal Capital Territory", "Balochistan", "Punjab", "Khyber Pakhtunkhwa", "Sindh" ];
    var i;
    for (i = 0; i < province_names.length; i++) {
        text = "slope_graphs/" + province_names[i] + ".html";
    } 
    $('#slope_graph').load("slope_graphs/Balochistan.html");
    // document.getElementById("slope_graph").innerHTML='<object type="type/html" data="slope_graphs/Balochistan.html" ></object>';
    // document.getElementById('slope_graph').style.border = "solid red 1px";

}); 

