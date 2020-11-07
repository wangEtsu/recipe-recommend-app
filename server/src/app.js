console.log("HOla");
// import packages from /node_modules
const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const morgan = require("morgan");

// start an express server
const app = express();
app.use(morgan("combine"));
app.use(bodyParser.json());
app.use(cors());

// routing stuff
app.get('/status', (req, res) => {
    res.send({
        message:"Hello World"
    })
})

app.post('/register', (req, res) => {
    res.send({
        message: `Hello ${req.body.email} ! your user was registered! Have fun!`
    })
})

app.listen(process.env.PORT || 8081);