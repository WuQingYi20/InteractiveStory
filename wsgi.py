from flask import Flask, render_template, jsonify, request
import openai

app = Flask(__name__)
initialCall = True

# Initialize OpenAI API with your API key
openai.api_key = "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"

# Define a dictionary to store user progress data
user_data = {}

# Global variable to track initialization status
initialized = False

@app.route('/')
def index():
    global initialized
    if initialized:
        # Initialization has already been done, return JSON response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(story=user_data['story'], choices=user_data['choices'])
        # Initialization has already been done, return HTML response
        else:
            return render_template('index.html', story=user_data['story'], choices=user_data['choices'])
    else:
        # Initialization code
        prompt = "Create an initial setting for a detective story that balances tension and credibility. The setting should establish a world view that is believable and creates a sense of intrigue or mystery. The story should be set in a specific location, and the setting should establish the tone and atmosphere of the story. Use specific details and sensory descriptions to make the setting vivid and compelling. The setting should be open-ended and allow for a variety of possible storylines and outcomes."
        storyResponse = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        story = storyResponse.choices[0].text
        choicesPrompt  = "Create the initial 3 choices for this detective story that balance tension and credibility. The choices should be believable and consistent with the established world view. Each choice should have a distinct consequence that leads the story in a different direction. Use specific language and details to make the choices compelling and engaging. The choices should create a sense of urgency and keep the player invested in the story. The choices in the response should be separated by the text ###, which should be placed before each choice, including the first one."
        choiceResponse = openai.Completion.create(
            engine="text-davinci-003",
            prompt = story + choicesPrompt ,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        user_data['story'] = story
        user_data['choices'] = choiceResponse.choices[0].text
        print("initial calling")
        initialized = True
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(story=story, choices=user_data['choices'])
        else:
            return render_template('index.html', story=story, choices=user_data['choices'])

# Define a route to handle user choices and update the story
@app.route('/next-page/<choice>')
def next_page(choice):
    originalStory = user_data['story'] + "\n" + choice
    prompt_story = originalStory + "\n" + " Create the next description that should include consequnce of player's movement and next events for this detective story that balances tension and credibility. The description should build on the established world view and the player's previous choices. It should create a sense of tension or urgency and reveal new information or clues that move the story forward. Use specific details and sensory descriptions to make the description vivid and engaging. The description should be open-ended and allow for a variety of possible storylines and outcomes. "
    response_story = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt_story,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    prompt_choices = originalStory + response_story.choices[0].text + "\n" + "Create 3 choices for next possibe player's choices of this detective story that balance tension and credibility. The choices should be consistent with the established world view and the player's previous choices. Each choice should have a distinct consequence that leads the story in a different direction. Use specific language and details to make the choices compelling and engaging. The choices should create a sense of urgency and keep the player invested in the story.The choices in the response should be separated by the text ###, which should be placed before each choice, including the first one."
    response_choices = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt_choices,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    story = response_story.choices[0].text
    choices = response_choices.choices[0].text
    user_data['story'] = story
    user_data['choices'] = choices
    #print("story: "+story) # Print the value of story for debugging
    #print("choices: "+choices) # Print the value of choices for debugging
    return jsonify(story=story, choices=choices)


if __name__ == '__main__':
    app.run(debug=True)
