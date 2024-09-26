import streamlit as st
import requests

import database
import prompts
import config

# Page configuration
st.set_page_config(page_title="AjurrumAI 😃", layout="wide")
st.title("AjurrumAI 😃")
st.write("Chat with the greatest Arabic grammar expert! / تحدث مع أكبر متخصص في قواعد اللغة العربية!")

# Sidebar for navigation
with st.sidebar:
    st.header("Mode / الوضع")
    option = st.radio("Which mode would you like? / أي وضع تود استخدامه",
                      ["Continue the course / متابعة الدرس",
                       "Review a lesson / مراجعة درس",
                       "Free discussion / مناقشة حرة",
                       "Exam / امتحان"])
    if option == "Continue the course / متابعة الدرس":
        pass
    elif option == "Review a lesson / مراجعة درس":
        pass
    elif option == "Free discussion / مناقشة حرة":
        pass
    elif option == "Exam / امتحان":
        pass

### USER MANAGEMENT

user_var_set = {
    "connected": False,
    "username": "None",
    "age": 0,
    "chapter": "None"
}

st.header("Identification / تسجيل الدخول")

menu = st.sidebar.selectbox('Menu / القائمة', ['Login / تسجيل الدخول', 'Sign Up / تسجيل حساب'])

if menu == 'Sign Up / تسجيل حساب':
    st.subheader('Create an Account / إنشاء حساب')
    username = st.text_input('Username / اسم المستخدم')
    password = st.text_input('Password / كلمة المرور', type='password')
    age = st.slider("Choose your age / اختر عمرك", 0, 100, 20)
    if st.button('Sign Up / تسجيل'):
        message = database.register(username, password, age)

        if message == "USERNAME_TAKEN":
            st.fail("You can't use this username - لا يمكنك استخدام هذا الإسم")
        else:
            st.success("Account created successfully! / تم إنشاء الحساب بنجاح!")
            login_message = database.login(username, password)
            if login_message == "LOGIN_SUCCESS":
                user_var_set["connected"] = True
                user_var_set["username"] = username

elif menu == 'Login / تسجيل الدخول':
    st.subheader('Login / تسجيل الدخول')
    username = st.text_input('Username / اسم المستخدم')
    password = st.text_input('Password / كلمة المرور', type='password')
    if st.button('Login / تسجيل الدخول'):
        message = database.login(username, password)
        if message == "INCORRECT_CREDENTIALS":
            st.fail("Incorrect username or password - خطا في الاسم او كلمة المرور")
        else:
            st.success("Logged in successfully! / تم تسجيل الدخول بنجاح!")
            user_var_set["connected"] = True
            user_var_set["username"] = username
            user = database.get_user_by_username(username)
            if user:
                user_var_set["age"] = user.get("age", 0)

# Input text from user
user_input = st.text_area("Ask your question or say what's on your mind: / اطرح سؤالك أو قل ما يدور في ذهنك:")

# Button to send the request
if st.button("Submit / إرسال"):
    if user_input.strip() == "":
        st.error("Please enter something. / الرجاء إدخال شيء.")
    else:
        # Determine interaction mode
        interaction_mode = option.split(" / ")[0]  # Extract English part

        # Adapt prompt based on interaction mode and age
        prompt = ""
        if interaction_mode == "Continue the course":
            prompt = f"I am a {user_var_set['age']} year old student who wants to continue the course. Here is my question: {user_input}"
        elif interaction_mode == "Review a lesson":
            prompt = f"I am reviewing a lesson. Here is my question: {user_input}"
        elif interaction_mode == "Free discussion":
            prompt = f"I would like to have a free discussion. Here is my topic: {user_input}"
        elif interaction_mode == "Exam":
            prompt = f"I am taking an exam. Here is my question: {user_input}"

        # Prepare the request body
        body = {
            "input": prompt,
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": 1500,
                "repetition_penalty": 1
            },
            "model_id": "sdaia/allam-1-13b-instruct",
            "project_id": "cb0d224c-3a53-4fec-ab52-a5f3dd088ba2"
        }

        url = config.WATSON_API_URL  # Ensure this is defined in your config
        headers = {
            "Authorization": f"Bearer {config.WATSON_API_KEY}",  # Ensure this is defined in your config
            "Content-Type": "application/json"
        }

        # Make the request to the IBM Watson X API
        try:
            response = requests.post(url, headers=headers, json=body)

            # Check for successful response
            if response.status_code == 200:
                data = response.json().get('results', [{}])[0].get('generated_text', '').strip()
                if data:
                    st.success("Response / الرد:")
                    st.write(data)
                else:
                    st.warning("No response received / لم يتم استلام رد")
            else:
                st.error(f"Error: {response.status_code}\n{response.text} / خطأ: {response.status_code}\n{response.text}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)} / حدث خطأ: {str(e)}")
