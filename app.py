import openai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates')

# Set up the OpenAI API credentials
openai.api_key = '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'

@app.route('/')
def index():
    # Generate the initial story description using the OpenAI API
    initial_story = generate_story()
    return render_template('index.html', story=initial_story)

@app.route('/story')
def story():
    choice1 = request.args.get('choice1')
    choice2 = request.args.get('choice2')
    choice3 = request.args.get('choice3')
    # Generate the updated story description and canvas data using the OpenAI API
    updated_story, canvas_data = generate_story(choice1, choice2, choice3)
    return jsonify({'story': updated_story, 'canvas': canvas_data})

def generate_story(choice1=None, choice2=None, choice3=None):
    # Set the starting prompt for the OpenAI API
    prompt = "Once upon a time, there was a detective named John who was investigating a series of mysterious crimes. As he delved deeper into the case, he discovered that there was more to the crimes than initially met the eye. The story should be both credible and full of tension, with elements of both detective and wuxia genres. Please generate a story that balances these elements well."
    # Add the player's choices to the prompt, if provided
    if choice1:
        prompt += " He decided to " + choice1 + " and found a clue that led him to the next part of the story."
    if choice2:
        prompt += " He then " + choice2 + " and discovered another clue that led him even further."
    if choice3:
        prompt += " Finally, he " + choice3 + " and uncovered the truth behind the mysterious crimes."
    # Call the OpenAI API to generate the story content
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )
    story_text = response.choices[0].text.strip()
    # Parse the story text to extract the canvas data
    canvas_data = []
    for line in story_text.split('\n'):
        if line.startswith('canvas:'):
            parts = line.split(':')
            canvas_data.append({
                'x': int(parts[1]),
                'y': int(parts[2]),
                'radius': int(parts[3]),
                'color': parts[4]
            })
    # Remove the canvas data from the story text
    story_text = story_text.split('\n\n')[0]
    return story_text, canvas_data

if __name__ == '__main__':
    app.run(debug=True)
