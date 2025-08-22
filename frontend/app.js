var express = require('express');
var app = express();
app.set('view engine', 'ejs');
app.set('views', './views'); 

var port = process.env.PORT || 3000;

app.get("/", function(req, res){
    res.render("dashboard");
});

app.get("/zone_info", function(req, res){
    res.render("zone_info");
});

app.listen(port, function(){
    console.log("server is running on port" + port);
});