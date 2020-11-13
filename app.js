// require packages
const express = require("express");
const bodyParser = require("body-parser");


// initialate express and ejs
const app = express();
app.set("view engine", "ejs");

app.use(express.urlencoded({ extended: false }))

// set up static folder
app.use(express.static("public"));

// routing
app.get("/", function(req, res) {
    res.render("index", {
        homePageContent: "Test"
    })
})

// feed to server
app.listen(process.env.PORT || 3000, function () {
    console.log("Server is running on port 3000");
});
