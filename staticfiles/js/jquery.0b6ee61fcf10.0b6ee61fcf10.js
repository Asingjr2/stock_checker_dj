$(document).ready(function(e){
    console.log("in business");
    
    $("#delete_stock").click(function(e){
        alert("Stock Deleted");
    })

    $("#add_stock").submit(function(e){
        alert("Stock Saved");
    })
})