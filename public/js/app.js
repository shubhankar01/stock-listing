$(document).ready(function(){
  $("#search-stock").click(function() {
	   $.get('/search_by_name', {stock_name: $("#search-stock-name").val()}, function(data) {
		
		   if(Object.keys(data).length === 0){
		    $("#search-result").html("No records found for the requested stock")
		    $("#search-result").css("color", "red");
		  }
		  else{
		  $("#search-result").html("<table class='table table-striped'><thead><tr><th scope='col'>SC_NAME</th><th scope='col'>SC_CODE</th><th scope='col'>Open</th><th scope='col'>High</th><th scope='col'>Low</th><th scope='col'>Close</th><th scope='col'>PreviousClose</th><th scope='col'>No.oftrades</th><th scope='col'>NetTurnover</th></tr></thead><tbody><tr><td>" + data['SC_NAME'] + "</td><td>" + data['SC_CODE'] + "</td><td>" + data['OPEN'] + "</td><td>" + data['HIGH'] + "</td><td>" + data['LOW'] + "</td><td>" + data['CLOSE'] + "</td><td>" + data['PREVCLOSE'] + "</td><td>" + data['NO_TRADES'] + "</td><td>" + data['NET_TURNOV'] + "</td></tr></tbody></table>");
		  }});
return false;
  });  });
