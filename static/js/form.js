"use strict";

//Plaeholder handler
$(function() {
	
if(!Modernizr.input.placeholder){             //placeholder for old brousers and IE
 
  $('[placeholder]').focus(function() {
   var input = $(this);
   if (input.val() == input.attr('placeholder')) {
    input.val('');
    input.removeClass('placeholder');
   }
  }).blur(function() {
   var input = $(this);
   if (input.val() == '' || input.val() == input.attr('placeholder')) {
    input.addClass('placeholder');
    input.val(input.attr('placeholder'));
   }
  }).blur();
  $('[placeholder]').parents('form').submit(function() {
   $(this).find('[placeholder]').each(function() {
    var input = $(this);
    if (input.val() == input.attr('placeholder')) {
     input.val('');
    }
   })
  });
 }
  
$('#contact-form').submit(function(e) {
      
		e.preventDefault();	
		var error = 0;
		var self = $(this);
		
	    var $name = self.find('[name=user-name]');
	    var $email = self.find('[type=email]');
	    var $message = self.find('[name=user-message]');
		
				
		var emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
		
  		if(!emailRegex.test($email.val())) {
			createErrTult('Error! Wrong email!', $email)
			error++;	
		}

		if( $name.val().length>1 &&  $name.val()!= $name.attr('placeholder')  ) {
			$name.removeClass('invalid_field');			
		} 
		else {
			createErrTult('Error! Write your name!', $name)
			error++;
		}

		if($message.val().length>2 && $message.val()!= $message.attr('placeholder')) {
			$message.removeClass('invalid_field');
		} 
		else {
			createErrTult('Error! Write message!', $message)
			error++;
		}
		
		
		
		if (error!=0){
			self.find('[type=submit]').attr('disabled', 'disabled');
			return;
		}

		self.children().fadeOut(300,function(){ $(this).remove() })
		$('<p class="success"><span class="success-huge">Thank you!</span> <br> your message successfully sent</p>').appendTo(self)
		.hide().delay(300).fadeIn();


		var formInput = self.serialize();
		$.post(self.attr('action'),formInput, function(data){}); // end post
}); // end submit

$('#login-form').submit(function(e) {
      
		e.preventDefault();	
		var error = 0;
		var self = $(this);
		
	    var $email = self.find('[type=email]');
	    var $pass = self.find('[type=password]');
		
				
		var emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
		
  		if(!emailRegex.test($email.val())) {
			createErrTult("Error! correo incorrecto!", $email)
			error++;	
		}

		if( $pass.val().length>1 &&  $pass.val()!= $pass.attr('placeholder')  ) {
			$pass.removeClass('invalid_field');			
		} 
		else {
			createErrTult('Error! password incorrecto!', $pass)
			error++;
		}
	    
	    if (error!=0){
			self.find('[type=submit]').attr('disabled', 'disabled');
			setTimeout(function(){
				self.find('[type=submit]').removeAttr('disabled');}, 4000);
			return;
	    }
	    
		//self.children().fadeOut(300,function(){ $(this).remove() })
		//$('<p class="login__title">sign in <br><span class="login-edition">welcome to A.Movie</span></p><p class="success">You have successfully<br> signed in!</p>').appendTo(self)
		//.hide().delay(300).fadeIn();


		// var formInput = self.serialize();
		// $.post(self.attr('action'),formInput, function(data){}); // end post
}); // end submit


$('#register-form').submit(function(e) {
    
	e.preventDefault();	
	var error = 0;
	var self = $(this);
	
    var $email = self.find('[name=email]');
    
    var $inputs = $('#register-form :input');
			
	var emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
	if(!emailRegex.test($email.val())) {
		createErrTult("Error! correo incorrecto!", $email)
		error++;	
	}

    // not sure if you wanted this, but I thought I'd add it.
    // get an associative array of just the values.
    $inputs.each(function() {
    	if($(this)[0].type === 'text' || $(this)[0].type === 'password'){
    		validate($(this), error);
    	}
    });
    
    if (error!=0){
		self.find('[type=submit]').attr('disabled', 'disabled');
		setTimeout(function(){
			self.find('[type=submit]').removeAttr('disabled');}, 4000);
		return;
    }
	
});


$('#btn-register').click(function(e){
	var self = $(this);
	var registerForm = $('#register-form');
	var loginForm = $('#login-form');
	
	loginForm.hide();
	
	limpiarForm(loginForm);
	
	registerForm.show();
});		
		
$('#btn-login').click(function(e){
	var self = $(this);
	var registerForm = $('#register-form');
	var loginForm = $('#login-form');
	
	limpiarForm(registerForm);
	
	loginForm.show();
	registerForm.hide();
});		


function limpiarForm(form)
{
	$(':input',form).not(':button, :submit, :reset, :hidden').val('').removeAttr('checked').removeAttr('selected');
}

function validate($elem, error){

	if( $elem.val().length>1) {
		$elem.removeClass('invalid_field');			
	} 
	else {
		createErrTult('Error! '+ $elem.attr('placeholder')+'  incorrecto!', $elem)
		error++;
	}
	
}

function createErrTult(text, $elem){
			$elem.focus();
			$('<p />', {
				'class':'inv-em alert alert-danger',
				'html':'<span class="icon-warning"></span>' + text + ' <a class="close" data-dismiss="alert" href="#" aria-hidden="true"></a>',
			})
			.appendTo($elem.addClass('invalid_field').parent()) 
			.insertAfter($elem)
			.delay(4000).animate({'opacity':0},300, function(){ $(this).slideUp(400,function(){ $(this).remove() }) });
	}
});
