const express = require('express');
const path = require('path');
const res = require("express/lib/response");
const app = express();

app.use(express.static(path.join(__dirname, '../client/src/main.tsx')));
app.get('/api',(req,res)=>{
    res.send(['user1','user2','user3']);
})


app.listen(5000, ()=>{console.log('Server is running on port http://localhost:5000.')});