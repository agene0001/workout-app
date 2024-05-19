const express = require('express');
const path = require('path');
const cors = require('cors');
const app = express();
const sql = require('mysql2')
const dbCon = sql.createConnection({
  host: "localhost",
  user: "root",               // replace with the database user provided to you
  password: "LexLuthern246!!??",                  // replace with the database password provided to you
  database: "automation",           // replace with the database user provided to you
  port: 3306
});
// dbCon.query('SELECT * FROM recipes', (err, result) => {
//     console.log(result.length)
//     // console.log(result);
// });
app.use(cors({origin:'http://localhost:5173'}))
app.use(express.static(path.join(__dirname, '../client/src/main.tsx')));
app.get('/api',(req,res)=>{
    res.send(['user1','user2','user3']);
})
app.get('/api/recipes',(req,res)=>{
   dbCon.query('SELECT * FROM recipes LIMIT 10', (err, result) => {
    res.send(result)
});
})

// const corsOptions = {
//     origin: '*',
//     credentials: true,
//     optionsSuccessStatus: 200
// }

app.listen(5001, ()=>{console.log('Server is running on port http://localhost:5001.')});