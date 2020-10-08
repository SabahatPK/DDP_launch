$("document").ready(function(){
    console.log("Requesting Server 1")  
    $('#geographicChoice').change(function(){
        console.log("Requesting Server") 
        var province = $("#geographicChoice").val(); 
        var indicator = $("#indicatorChoice").val(); 

        $.ajax({ 
            url: "http://0.0.0.0:5555/generate_scatter_plot",
            type: "POST",
            crossDomain: true, 
            contentType: "application/json",
            data: JSON.stringify({"province": province, "indicator": indicator}),  
            success: function(resp){
                $('div#graph').html(resp['generated_plot']);
                // document.getElementById('graph').innerHTML =  resp['generated_plot'];
            }
        }).done(function(data) {
            console.log(data);        
        });    
    });


    $('#indicatorChoice').change(function(){
        console.log("Requesting Server") 
        var province = $("#geographicChoice").val(); 
        var indicator = $("#indicatorChoice").val(); 

        $.ajax({ 
            url: "http://0.0.0.0:5555/generate_scatter_plot",
            type: "POST",
            crossDomain: true, 
            contentType: "application/json",
            data: JSON.stringify({"province": province, "indicator": indicator}),  
            success: function(resp){
                $('div#graph').html(resp['generated_plot']);
                // document.getElementById('graph').innerHTML =  resp['generated_plot'];
            }
        }).done(function(data) {
            console.log(data);        
        });    
    });
    
});
