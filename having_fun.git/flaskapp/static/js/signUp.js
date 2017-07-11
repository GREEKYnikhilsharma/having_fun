$(function(){
	$('#btnSignUp').click(function(){
		
		$.ajax({
			url: '/signUp',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
	$('#signinBtn').click(function()
          {
            auth2.grantOfflineAccess({'redirect_uri': 'postmessage'}).then(signInCallback);
           });

	 function signInCallback(json) {
		console.log('inside callback fuction');
		console.log(json);
		authResult = json;
		if (authResult['code']) {
			$('#signinBtn').attr('style', 'display: none');
             // $('#result').html('One-Time Auth Code:</br>'+ authResult['code'] + '<br>Now json'+JSON.stringify(json))
             // Send the code to the server
			$.ajax({
			type: 'POST',
			url: '/oauth/send',
			processData: false,
			data: authResult['code'],
      //contentType: 'application/json;charset=UTF-8',
			contentType: 'application/octet-stream; charset=utf-8',
			success: function(result) {
       
			if (result) { 
                console.log('Login Successful!</br>'+ JSON.stringify(result )+'and key'+authResult['code']) 
			} 
			else if (authResult['error']) {
				console.log('There was an error: ' + authResult['error']);
			}
				}
					});
						}
							}


});
