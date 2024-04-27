const express = require('express');
const res = require("express/lib/response");
const app = express();

app.get('/api',(req,res)=>{
    res.send(['user1','user2','user3']);
})

app.listen(5000, ()=>{console.log('Server is running on port 5000')})