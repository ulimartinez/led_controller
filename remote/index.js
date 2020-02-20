var express = require('express');
var app = express();
var http = require('http').createServer(app);
var path = require('path');

app.get('/', (req, res) => res.sendFile(path.join(__dirname + '/index.html')));
app.use(express.static(__dirname+'/public'));
app.listen(32400, () => console.log('listening on 32400'));
