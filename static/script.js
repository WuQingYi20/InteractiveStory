$(document).ready(function() {
	// Set up the canvas element
	var canvas = document.getElementById('canvas');
	var ctx = canvas.getContext('2d');
	var radius = 10;
	var dragging = false;
	var lastX;
	var lastY;
	var canvasData = [];
	
	// Add mouse event listeners to the canvas
	canvas.addEventListener('mousedown', function(e) {
		dragging = true;
		lastX = e.offsetX;
		lastY = e.offsetY;
	});

	canvas.addEventListener('mousemove', function(e) {
		if (dragging) {
			ctx.beginPath();
			ctx.moveTo(lastX, lastY);
			ctx.lineTo(e.offsetX, e.offsetY);
			ctx.lineWidth = radius * 2;
			ctx.stroke();
			canvasData.push({x: e.offsetX, y: e.offsetY, radius: radius, color: '#000000'});
			lastX = e.offsetX;
			lastY = e.offsetY;
		}
	});

	canvas.addEventListener('mouseup', function(e) {
		dragging = false;
	});

	canvas.addEventListener('mouseout', function(e) {
		dragging = false;
	});

	// Add form submission event listener
	$('#choices-form').submit(function(event) {
		event.preventDefault();
		// Get the user's choices from the form
		var choice1 = $('#choice1').val();
		var choice2 = $('#choice2').val();
		var choice3 = $('#choice3').val();
		// Send an AJAX request to the Flask server to generate the updated story and canvas data
		$.ajax({
			type: 'GET',
			url: '/story',
			data: {choice1: choice1, choice2: choice2, choice3: choice3},
			success: function(response) {
				// Update the story content on the page
				$('#story').html(response.story);
				// Redraw the canvas based on the new canvas data
				ctx.clearRect(0, 0, canvas.width, canvas.height);
				for (var i = 0; i < response.canvas.length; i++) {
					var circle = response.canvas[i];
					ctx.beginPath();
					ctx.arc(circle.x, circle.y, circle.radius, 0, 2 * Math.PI, false);
					ctx.fillStyle = circle.color;
					ctx.fill();
				}
				// Clear the canvas data array
				canvasData = [];
			},
			error: function(error) {
				console.log(error);
			}
		});
	});

	// Add clear button event listener
	$('#clear-button').click(function() {
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		canvasData = [];
	});
});
