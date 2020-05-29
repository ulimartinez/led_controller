var irc = require('irc');
var readline = require('readline');
var express = require('express');
var request = require("request-promise");
var app = express();
var http = require('http').Server(app);
var WebSocket = require('ws');
var ws = new WebSocket('ws://localhost:3500');
//var io = require('socket.io')(3500);
const axios = require('axios');

var PASS = 'oauth:hg1ala7i8rkvx742s5aev7tzbxi3ao';
var NICK = 'wombo_combo_happy_feet';
var TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiNWU4OWFiMDEwNTdmYzcyY2RjYjI2N2IxIiwicm9sZSI6Im93bmVyIiwiY2hhbm5lbCI6IjVlODlhYjAxMDU3ZmM3NjhkNWIyNjdiMiIsInByb3ZpZGVyIjoidHdpdGNoIiwiYXV0aFRva2VuIjoiaGZoUGFsOFBEbUVTZjBoOE0tdTZuZGJJR1MzdktHUjJCM0JlOExTRFFWRVgxcnJ6IiwiaWF0IjoxNTg2MDgwNTEzLCJpc3MiOiJTdHJlYW1FbGVtZW50cyJ9.xezTTER8faQl16_mkpMwkxhLgD3glXZm-V3a7lLmcFw" 
var CHAN="5e89ab01057fc768d5b267b2";
var translate_key = 'AIzaSyC4XuvfwF2kLciFIZJb5pfdclxVbjB1G6A';
var CLIENT_ID = '##########';
var options;


var rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});
const opts = {
	identity: {
		username: NICK,
		password: PASS
	},
	channels: [NICK]
};
axios.defaults.headers.common['Authorization'] = "Bearer " + TOKEN;
//


http.listen(3000, function(){
	  console.log('listening on *:3000');
});


setTimeout(function(){
  getChannel();
}, 1000);

//

// get channel name
function getChannel() {
	channel_name = ['#'+NICK];
	console.log("Joining:", channel_name);
	  setTimeout(function () {
	      joinChannel(channel_name);
	  }, 3000);
}


// join channel
function joinChannel(res) {
  var c = new irc.Client('irc.twitch.tv', NICK,
    {
      username: NICK,
      port: 6667,
      password: PASS,
      channels: res
    });

  c.addListener('error', function(message) {
    console.log('error: ', message);
  });
  c.addListener('raw', function(message) {
	  var ms = message.args[1];
	  console.log(ms);
	  if(ms){
		  var cheeramnt = isCheerAmnt(ms);
		  console.log(cheeramnt);
		  if(cheeramnt > 0 || (message.nick == "wombo_combo_happy_feet" && cheeramnt == 0)){
		  	ws.send(ms+'|'+message.nick);
			  //say message here
			  //io.emit(ms);
		  }
	  }
  });
}
function isCheerAmnt(msg){
	  var cheerReg = /^cheer([0-9]+)$/;
	  parts = msg.split(" ");
	  for(var i = 0; i < parts.length; i++){
		   if(cheerReg.test(parts[i])){
			    var amount = parseInt(msg.replace(/[a-z]/g, ''));
			    if(amount < 100000){
				     console.log(amount);
				     return amount;
			     }
		    }
	   }
	  return -1;
}
