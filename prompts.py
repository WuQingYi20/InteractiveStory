prompts = {
    "index":{
        "story": """Create an initial setting for a detective story that balances tension and credibility. 
        The setting should establish a world view that is believable and creates a sense of intrigue or mystery. 
        The story should be set in a specific location, and the setting should establish the tone and atmosphere of the story. 
        Use specific details and sensory descriptions to make the setting vivid and compelling. 
        The setting should be open-ended and allow for a variety of possible storylines and outcomes. 
        your writing shouldn't include these key world like normal detective novel, such as setting, atmosphere, character, plot, etc.
        at the end of description, you should leave conflict or problem or puzzle that player should solve in the story.
        don't make it too long.
        """,

        "choices": """Create the initial 3 choices for this detective story that balance tension and credibility. 
        The choices should be believable and consistent with the established world view. 
        Each choice should have a distinct consequence that leads the story in a different direction. 
        Use specific language and details to make the choices compelling and engaging. 
        The choices should create a sense of urgency and keep the player invested in the story. 
        The choices in the response should be separated by the text ###, which should be placed before each choice, including the first one.""",

        "System": """you are a detective novelist who is good at writing detective story balanced with tension and credibility 
        as well as creating atmosphere"""
    },
    "next-page": {
        "story": """Create the next description that should include consequnce of player's movement and next events for this detective story that balances tension and credibility. 
        The description should build on the established world view and the player's previous choices. 
        It should create a sense of tension or urgency and reveal new information or clues that move the story forward. 
        Use specific details and sensory descriptions to make the description vivid and engaging. 
        The description should be open-ended and allow for a variety of possible storylines and outcomes.""",

        "choices": """Create 3 choices for next possibe player's choices of this detective story that balance tension and credibility. 
        The choices should be consistent with the established world view and the player's previous choices. 
        Each choice should have a distinct consequence that leads the story in a different direction. 
        Use specific language and details to make the choices compelling and engaging. 
        The choices should create a sense of urgency and keep the player invested in the story.
        The choices in the response should be separated by the text ###, which should be placed before each choice, including the first one.""",

        "System": """you are a detective novelist who is good at writing detective story balanced with tension and credibility 
        as well as creating atmosphere""",

        "storyAssistant": """consequence of your choice and next events or description""",

        "choicesAssistant": """3 totally different choices""",

        "summary": """Create a summary of the previous story and actions. 
        The summary should be concise and include the most important details of the story. 
        It should be written in the third person and should not include any dialogue. 
        The summary should be open-ended and allow for a variety of possible storylines and outcomes.
        However, it should not be longer than 3 sentences."""
    }
}