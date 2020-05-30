// JavaScript Document
function handleAjax(file){
	document.write(ajax.readyState);
	document.write("This is my Ajax");
	ajax.send(file);
	
}
ajax=getXMLHttpRequestObject();
ajax.open("GET", "file:///C:/Users/Visitor/Documents/LearningJavascript/ajax.html", true );
ajax.onreadystatechange=handleAjax("message.txt");

//Just doing another stuff
document.write("</br>"+document.lastModified);
document.write("</br>"+document.title);
document.write("</br>"+window.location);
var timeStam= new Date();
var hours=timeStam.getHours();
if(hours<12){
	document.write("Good Morning");
}
else if(hours>12 && hours<18){
	document.write("<p> Good Afternoon </p>");
}
else{document.write("Good Evening");}

var i=1;
var x=10;
/*
while(i<=10){
	var ii=1;
	var msg="";
	
	while(ii<=i){
		msg+="*";
		ii++;
	}
	var sp="";
	while(x>0){
		sp+=" ";
		x++;
	}
	
	document.write(sp+ msg+ "<br />");
	i++;
	x--;
}
*/
