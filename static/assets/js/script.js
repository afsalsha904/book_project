function showAlert(){

var username=document.getElementById('username').ariaValueMax;
var first_name=document.getElementById('first_name').ariaValueMax;
var last_name=document.getElementById('last_name').ariaValueMax;
var email=document.getElementById('email').ariaValueMax;
var password=document.getElementById('password').ariaValueMax;
var password1=document.getElementById('password1').ariaValueMax;


if(!username || !first_name || !last_name || !email || !password || !password1 ){
    alert('please fill out the required field');
}
else{

    alert('Registration successful. Now you can login');
    
    }
}

