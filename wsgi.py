from flask import Flask, render_template, jsonify, request
import openai
import re

app = Flask(__name__)
initialCall = True
currentDescription = ""

# Initialize OpenAI API with your API key
openai.api_key = "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"

# Define a dictionary to store user progress data
user_data = {}

# Global variable to track initialization status
initialized = False

@app.route('/')
def index():
    global initialized
    global currentDescription
    if initialized:
        # Initialization has already been done, return JSON response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(story=user_data['story'], choices=user_data['choices'])
        # Initialization has already been done, return HTML response
        else:
            return render_template('index.html', story=user_data['story'], choices=user_data['choices'])
    else:
        # Initialization code
        systemRoleAuto = """you are a detective novelist who is good at writing detective story balanced with tension and credibility as well as creating atmosphere"""
        promptStory = """Create an initial setting for a detective story that balances tension and credibility. 
        The setting should establish a world view that is believable and creates a sense of intrigue or mystery. 
        The story should be set in a specific location, and the setting should establish the tone and atmosphere of the story. 
        Use specific details and sensory descriptions to make the setting vivid and compelling. 
        The setting should be open-ended and allow for a variety of possible storylines and outcomes. 
        your writing shouldn't include these key world like normal detective novel, such as setting, atmosphere, character, plot, etc.
        at the end of description, you should leave conflict or problem or puzzle that player should solve in the story.
        don't make it too long.
        """
        storyResponse = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{systemRoleAuto}"},
            {"role": "user", "content": f"{promptStory}"},
            #{"role": "assistant", "content": f"{contentAssistant}"},
        ],
        max_tokens= 1500,
    )
        story = storyResponse.choices[0].message['content']
        currentDescription = story
        choicesPrompt  = """Create the initial 3 choices for this detective story that balance tension and credibility. 
        The choices should be believable and consistent with the established world view. 
        Each choice should have a distinct consequence that leads the story in a different direction. 
        Use specific language and details to make the choices compelling and engaging. 
        The choices should create a sense of urgency and keep the player invested in the story. 
        The choices in the response should be separated by the text ###, which should be placed before each choice, including the first one."""
        choiceResponse = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{systemRoleAuto}"},
            {"role": "user", "content": f"{story} {choicesPrompt}"},
            #{"role": "assistant", "content": f"{contentAssistant}"},
        ],
        max_tokens= 1500,
    )
        
        # Split the text into paragraphs using a regular expression
        paragraphs = re.split(r"\n\s*\n", story)
        #Insert <p> tags around each paragraph
        formatted_story = "\n".join([f"<p>{paragraph}</p>" for paragraph in paragraphs])
        user_data['story'] = formatted_story
        user_data['choices'] = choiceResponse.choices[0].message['content']
        print("initial calling")
        initialized = True
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(story=story, choices=user_data['choices'])
        else:
            return render_template('index.html', story=story, choices=user_data['choices'])

# Define a route to handle user choices and update the story
@app.route('/next-page/<choice>')
def next_page(choice):
    systemRoleAuto = "you are a detective novelist who is good at writing detective story balanced with tension and credibility as well as creating atmosphere"
    originalStory = user_data['story'] + "\n" + choice
    contentAssistant = "consequence of your choice and next events or description"
    contentAssistantChoices = "3 totally different choices"
    prompt_story = originalStory + "\n" + " Create the next description that should include consequnce of player's movement and next events for this detective story that balances tension and credibility. The description should build on the established world view and the player's previous choices. It should create a sense of tension or urgency and reveal new information or clues that move the story forward. Use specific details and sensory descriptions to make the description vivid and engaging. The description should be open-ended and allow for a variety of possible storylines and outcomes. "
    response_story = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{systemRoleAuto}"},
            {"role": "user", "content": f"{prompt_story}"},
            {"role": "assistant", "content": f"{contentAssistant}"},
        ],
        max_tokens= 1500,
    )
    prompt_choices = originalStory + response_story.choices[0].message['content'] + "\n" + "Create 3 choices for next possibe player's choices of this detective story that balance tension and credibility. The choices should be consistent with the established world view and the player's previous choices. Each choice should have a distinct consequence that leads the story in a different direction. Use specific language and details to make the choices compelling and engaging. The choices should create a sense of urgency and keep the player invested in the story.The choices in the response should be separated by the text ###, which should be placed before each choice, including the first one."
    response_choices = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{systemRoleAuto}"},
            {"role": "user", "content": f"{prompt_choices}"},
            {"role": "assistant", "content": f"{contentAssistantChoices}"},
        ],
        max_tokens= 1500,
    )
    story = response_story.choices[0].message['content']
    choices = response_choices.choices[0].message['content']
    # get summary of previous story and actions by gpt-3.5-turbo and original story
    prompt_summary = originalStory + "\n" + "Create a summary of the previous story and actions. The summary should be concise and include the most important details of the story. It should be written in the third person and should not include any dialogue. The summary should be open-ended and allow for a variety of possible storylines and outcomes.However, it should not be longer than 3 sentences."
    response_summary = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{systemRoleAuto}"},
            {"role": "user", "content": f"{prompt_summary}"},
            #{"role": "assistant", "content": f"{contentAssistant}"},
        ],
        max_tokens= 1500,
    )

    user_data['story'] = story
    user_data['choices'] = choices
    user_data['summary'] = response_summary.choices[0].message['content']
    return jsonify(story=story, choices=choices, summary=user_data['summary'])

if __name__ == '__main__':
    app.run(debug=True)
