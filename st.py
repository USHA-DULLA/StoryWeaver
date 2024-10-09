import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
import time

# Function to get a response from LLama 2 model
def getLLamaresponse(input_text, no_words, blog_style, characters, age_group, tone):
    # LLama2 model
    llm = CTransformers(
        model='C:\\Users\\91630\\OneDrive\\Desktop\\DL projects\\llama-2-7b-chat.ggmlv3.q8_0.bin',
        model_type='llama',
        config={
            'max_new_tokens': 256,
            'temperature': 0.01
        }
    )

    # Prompt Template including additional variables like characters, age group, and tone
    template = """
        Write a {tone} story for {blog_style} kids in the age group {age_group}.
        The story should include the characters: {characters}.
        The story's topic is {input_text}, and it should be within {no_words} words.
    """
    
    prompt = PromptTemplate(
        input_variables=["blog_style", "input_text", "no_words", "characters", "age_group", "tone"],
        template=template
    )

    # Generate the response from the LLama 2 model
    response = llm(prompt.format(
        blog_style=blog_style,
        input_text=input_text,
        no_words=no_words,
        characters=characters,
        age_group=age_group,
        tone=tone
    ))
    return response

# Streamlit page configuration
st.set_page_config(
    page_title="StoryWeaver",
    page_icon='	✨',
    layout='centered',
    initial_sidebar_state='collapsed'
)

st.header("StoryWeaver: Tailored Tales for Kids ✨")

# Input field for story title
input_text = st.text_input("Enter the Story Title")

# Create two columns for word count and genre selection
col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input('No of Words')

with col2:
    blog_style = st.selectbox('Story genre', ('Fantasy', 'Adventure', 'Horror'), index=0)

# Additional inputs: characters, age group, and tone
characters = st.text_input('Enter character names (comma-separated)')
age_group = st.selectbox('Select the age group', ('3-5 years', '6-9 years', '10-12 years'))
tone = st.selectbox('Select the tone of the story', ('Funny', 'Serious', 'Mysterious','Fantasy','Horror'))

# Validate word count
if no_words.isdigit():
    no_words = int(no_words)
else:
    st.error("Please enter a valid number for the word count")
    no_words = None

# Button to trigger story generation
submit = st.button("Generate")

# Final response
if submit and input_text and no_words:
    with st.spinner('Generating your story...'):
        time.sleep(2)  # Simulate loading time
        story = getLLamaresponse(input_text, no_words, blog_style, characters, age_group, tone)
        st.success("Story generated successfully!")
        st.write(story)

        # Option to download the story as a text file
        st.download_button('Download Story as Text', data=story, file_name=f"{input_text}_story.txt")

        # Allow users to provide feedback on the generated story
        feedback = st.text_area("Do you like the story? Leave your feedback here!")

        # Allow users to edit the story directly in the app
        st.write("You can edit the story below if you'd like:")
        editable_story = st.text_area("Edit the Story:", story)
else:
    st.info("Please provide both a title and a valid word count.")

