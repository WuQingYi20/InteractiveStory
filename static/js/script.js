window.onload = function() {
	const story = document.querySelector('.story');
	const choices = document.querySelector('.choices');
	story.classList.add('bg-dark', 'text-light', 'p-3', 'rounded');
	choices.classList.add('bg-dark', 'text-light', 'p-3', 'rounded');
	const choicesList = document.querySelectorAll('.choice');
	choicesList.forEach(function(choice) {
	  choice.classList.add('btn', 'btn-outline-light', 'me-2', 'mb-2');
	});
  
	function updateStoryAndChoices(response) {
	  const data = JSON.parse(response);
	  const storyContent = data.story;
	  const choicesContent = data.choices;
	  console.log(choicesContent);
	  const choicesList = choicesContent.split('###').slice(1, 4);
	  //console.log(choicesList);
	
	  story.innerHTML = storyContent;
	  choices.innerHTML = '';
	  choicesList.forEach(function(choiceText) {
		//console.log("choiceText: "+choiceText);
		const li = document.createElement('li');
		const a = document.createElement('a');
		a.href = '#';
		a.innerHTML = choiceText;
		a.classList.add('btn', 'btn-outline-light', 'me-2', 'mb-2');
		li.appendChild(a);
		choices.appendChild(li);
	  });
	}
	
	// Load the initial story and choices when the page first loads
	const request = new XMLHttpRequest();
	request.open('GET', '/');
	request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
	request.onload = function() {
	  if (request.status === 200) {
		updateStoryAndChoices(request.responseText);
	  }
	};
	request.send();
  
	// Listen for clicks on the choices and update the story and choices accordingly
	// Listen for clicks on the choices and update the story and choices accordingly
choices.addEventListener('click', function(event) {
	if (event.target.tagName === 'A') {
	  event.preventDefault();
	  const choice = event.target.innerText;
	  const url = '/next-page/' + choice;
	  const request = new XMLHttpRequest();
	  request.open('GET', url);
  
	  // Add loading element to the DOM
	  const loading = document.createElement('div');
	  loading.id = 'loading';
	  loading.innerText = 'Loading...';
	  choices.appendChild(loading);
  
	  // Show loading element while waiting for response
	  loading.classList.add('d-block');
  
	  request.onload = function() {
		// Remove loading element from the DOM
		loading.remove();
  
		// Update story and choices
		updateStoryAndChoices(request.responseText);
	  };
	  request.send();
	}
  });
  
	  
  };
  