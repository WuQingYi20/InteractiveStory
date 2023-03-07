window.onload = function() {
	const story = document.querySelector('.story');
	const choices = document.querySelector('.choices');
	const recordList = document.getElementById('record-list');
  
	story.classList.add('bg-dark', 'text-light', 'p-3', 'rounded');
	choices.classList.add('bg-dark', 'text-light', 'p-3', 'rounded');
  
	const choicesList = document.querySelectorAll('.choice');
	choicesList.forEach(function(choice) {
	  choice.classList.add('btn', 'btn-outline-light', 'me-2', 'mb-2');
	});
  
	// Define the previousStories array
	let previousStories = [];
  
	function addSummaryToPreviousStories(summaryContent) {
	  if (summaryContent != null) {
		previousStories.push(`<b>previous action:</b> ${summaryContent}`);
	  }
	}
  
	function showPreviousStories() {
	  if (previousStories.length === 0) {
		const defaultItem = document.createElement('li');
		defaultItem.classList.add('list-group-item');
		defaultItem.innerHTML = 'You just started your journey.';
		recordList.appendChild(defaultItem);
	  } else {
		recordList.innerHTML = '';
		for (let i = 0; i < previousStories.length; i++) {
		  const item = document.createElement('li');
		  item.classList.add('list-group-item');
		  item.innerHTML = previousStories[i];
		  recordList.appendChild(item);
		}
	  }
	}
  
	function formatStory() {
	  const paragraphs = document.querySelectorAll('.story p');
	  for (let i = 0; i < paragraphs.length; i++) {
		paragraphs[i].classList.add('text-light', 'p-3', 'rounded');
	  }
	}
  
	function createChoiceButton(choiceText) {
	  const li = document.createElement('li');
	  const a = document.createElement('a');
	  a.href = '#';
	  a.innerHTML = choiceText;
	  a.classList.add('btn', 'btn-outline-light', 'me-2', 'mb-2');
	  li.appendChild(a);
	  return li;
	}
  
	function updateStoryAndChoices(response) {
	  const data = JSON.parse(response);
	  const storyContent = data.story;
	  const choicesContent = data.choices;
	  const summaryContent = data.summary;
  
	  addSummaryToPreviousStories(summaryContent);
	  showPreviousStories();
  
	  const choicesList = choicesContent.split('###').slice(1, 4);
  
	  story.innerHTML = storyContent;
	  formatStory();
  
	  choices.innerHTML = '';
	  choicesList.forEach(function(choiceText) {
		const choiceButton = createChoiceButton(choiceText);
		choices.appendChild(choiceButton);
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
			if (request.status === 200) {
			  updateStoryAndChoices(request.responseText);
			} else {
			  console.error('Failed to load data');
			}
		  };
		};
	});
	  };