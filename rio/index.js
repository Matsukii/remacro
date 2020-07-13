express = require('express');
conf = require('./conf');

let app = express()

var server = require('http').Server(app);
var io = require('socket.io')(server);


app.use(express.static('public'));
app.use(express.static('assets'));


app.get("/", (req, res, next) => {
    res.status(200).sendFile(`${__dirname}/public/home.html`)
})

app.get("/home", (req, res, next) => {
    res.status(200).redirect('https://github.com/matsukii/remacro')
})

app.get("/help", (req, res, next) => {
    res.status(200).redirect('https://github.com/matsukii/remacro/blob/master/readme.md')
})

app.get("/:code", (req, res, next) => {
    if(!req.params.code) next();
    res.status(200).sendFile(`${__dirname}/public/home.html`)
})

app.get('*', (req, res) => {
    res.status(404).send("Not found")
})



io.on('connection', socket => {
    // emit the unique id for clients
    socket.emit('sid', {id: socket.id, conAt: Date.now()})

    // send a macro click
    socket.on("macro", key => {
        if(!key.toid) return 
        // console.log(`received ${key}`);
        io.to(key.toid).emit("macro", key)
    })

    // get buttons from remote to client
    socket.on("getBtns", get => {
        io.to(get.toid).emit("getBtns", {toid: socket.id})
    })

    // response buttons from client to remote
    socket.on("resBtns", btns => {
        io.to(btns.toid).emit("resBtns", btns)
    })

    
    // dosn't work properly, may be fixed later
    socket.on("stopp", user => {
        io.to(user.tiod).emit("stopp", true)
    })
});


server.listen(conf.app.port, function(){
    console.log(`Server started at http://localhost:${conf.app.port}`);
});
