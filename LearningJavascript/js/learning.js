//Javascript file
var el, today, hour, greetings;
el=document.getElementById('shutter');
el.innerHTML='Howdy hi wassup';
today= new Date();
hour=today.getHours();
if(hour<12){greetings='Good Morning';}
else if(hour <18){greetings='Good Afternoon';}
else if(hour<24){greetings='Good Evening';}
else{greetings='Welcome';}
el.innerHTML="<p>"+greetings+"</p>";
var colors=['white', 'black', 'yellow', 'red', 'green', 'blue', 'orange'];
var elcolor=document.getElementById('color');
elcolor.innerHTML='<p>'+ colors[5] +'<p>';

var message="Welcome to our site. click here to sign up for our news letter";
function welcome(m){
	var el=document.getElementById('message');
	el.textContent=m;
}

welcome(message);

// working with object
//literal notation
var hotel={
	name: 'Quay',
	rooms: 45,
	booked: 20,
	checkAvailability: function(){return this.rooms-this.booked;} 
}
document.write(hotel.checkAvailability());
//constructor notation
hotel = new Object();
hotel.name="Park";
hotel.rooms=500;
hotel.booked=456;
hotel.checkAvailability=function(){return this.rooms - this.booked;};
document.write('<p>'+hotel.checkAvailability() +' This object was created using constructor notation</p>' );

//creating function using function template
function createObject(name, rooms, booked){
	this.rooms=rooms;
	this.name=name;
	this.booked=booked;
	this.checkAvailability= function(){return this.rooms-this.booked;};
}
var Quay= new createObject('Quay', 'rooms', 'booked');
document.write(Quay.name);