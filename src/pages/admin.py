import streamlit as st
import requests

st.title("📄 Admin")
# Input box
# sample_prompt = "Generate 10 mathematics practice questions suitable for a student in Class 4 (age 9–10). Include a mix of topics such as addition, subtraction, multiplication, division, word problems, fractions, and basic geometry. Ensure the questions are clear, age-appropriate, and follow the curriculum typically taught in Class 4. Do not include the answers."
sample_prompt = "e.g. Generate 10 mathematics practice questions"
user_input = st.text_area("Enter your question:", height=150, placeholder=sample_prompt)

if st.button("Generate Questions"):
    if not user_input.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"input_text": user_input})
                if response.status_code == 200:
                    result = response.json()
        
                    st.session_state.questions = result.get("response", []).get("questions", [])
                    st.session_state.answers = [""] * len(st.session_state.questions)
                    #st.success(f"{result["response"]}")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")

# Show questions if available
if "questions" in st.session_state:
    st.subheader("📋 Questions")
    #st.write(f"Here are the generated questions: {st.session_state.questions}")
    for i, question in enumerate(st.session_state.questions):
        st.markdown(f"**{i+1}. {question.get('question', 'No question found')}**")
        #st.session_state.answers[i] = st.text_input(f"Your Answer to Q{i+1}", key=f"answer_{i}")

    # if st.button("Submit Answers"):
    #     st.success("✅ Your answers have been submitted!")
    #     for i, answer in enumerate(st.session_state.answers):
    #         st.write(f"**Q{i+1} Answer:** {answer}")