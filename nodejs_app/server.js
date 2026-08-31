const express = require('express');
const app = express();


app.get("/", (req,res) => {
    res.json({msg: "Hello, World!"});
});

app.listen(3000, () => {
    console.log("Server is running on port 3000");
});