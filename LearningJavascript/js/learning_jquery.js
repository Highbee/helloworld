// JavaScript Document
box.innerText = $;
$(document).ready((function(){
	box.innerHTML= 'I got it!. Didn\'t I ?' ;
}()));
$(window).on('scroll', function(ev){
	$('#box').prepend('<p>You\'re scrolling this page</p>');}
	);
$(window).on('resize', function(ev){
	$('#box').append('<p>You resized the browser and the new width is '+ 
	window.outerWidth + ' and the new height is '+ window.outerHeight+'</p>');});