import streamlit as st
import requests

from database import *
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
        print("//")
    elif option == "Review a lesson / مراجعة درس":
        print("//")
    elif option == "Free discussion / مناقشة حرة":
        print("//")
    elif option == "Exam / امتحان":
        print("//")

### USER GESTION

user_var_set = {
    "connected" : False,
    "username" : "None",
    "age" : 0,
    "chapter" : "None"
}

st.header("Identification / تسجيل الدخول")

menu = st.sidebar.selectbox('Menu / القائمة',['Login / تسجيل الدخول','Sign Up / تسجيل حساب'])

if menu == 'Sign Up / تسجيل حساب':
    st.subheader('Create an Account / إنشاء حساب')
    username = st.text_input('Username / اسم المستخدم')
    password = st.text_input('Password / كلمة المرور', type='password')
    age = st.slider("Choose your age / اختر عمرك", 0, 100, 20)
    if st.button('Sign Up / تسجيل'):
        message = register(username, password, age)

        if message == EtatsDB.USERNAME_US:
            st.fail("You can't use this username - لا يمكنك استخدام هذا الإسم")
        else:
            st.success(message)
            login(username, password)

elif menu == 'Login / تسجيل الدخول':
    st.subheader('Login / تسجيل الدخول')
    username = st.text_input('Username / اسم المستخدم')
    password = st.text_input('Password / كلمة المرور', type='password')
    if st.button('Login / تسجيل الدخول'):
        message = login(username, password)
        if message  == EtatsDB.INCOR_CREDS:
            st.fail("Incorrect username or password - خطا في الاسم او كلمة المورور")
        else:
            st.success(message)
            user_var_set["connected"] = True
            user_var_set["username"] = username

# Input text from user
user_input = st.text_area("Ask your question or say what's on your mind: / اطرح سؤالك أو قل ما يدور في ذهنك:")
خطا في الاسم او كلمة المورور
# Button to send the request
if st.button("Submit / إرسال"):
    if user_input.strip() == "":
        st.error("Please enter something. / الرجاء إدخال شيء.")

    else:
        # Adapt prompt based on interaction mode and ag
        e
        prompt = ""
        # Prepare the request body
        body = {
            "input": prompt,
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": 900,
                "repetition_penalty": 1
            },
            "model_id": "sdaia/allam-1-13b-instruct",
            "project_id": "cb0d224c-3a53-4fec-ab52-a5f3dd088ba2"
        }

        # Make the request to the IBM Watson X API
        try:
            response = requests.post(url, headers=headers, json=body)

            # Check for successful response
            if response.status_code == 200:
                data = response.json().get('results', [{}])[0].get('generated_text', '').strip()
                if data:
                    st.success("Réponse :")
                    st.write(data)
                else:
                    st.warning("Pas de réponse")
            else:
                st.error(f"Erreur : {response.status_code}\n{response.text}")

        except Exception as e:
            st.error(f"Une erreur est survenue : {str(e)}")
    if interaction_mode == "Avancer dans le cours":
            prompt = f"Je suis un étudiant de {age} ans qui souhaite avancer dans le cours. Voici ma question : {user_input}"
        elif interaction_mode == "Discuter avec le professeur":
            prompt = f"Je suis un étudiant de {age} ans et je souhaite discuter avec le professeur. Voici ma question : {user_input}"

        # Prepare the request body
        body = {
            "input": prompt,
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": 900,
                "repetition_penalty": 1
            },
            "model_id": "sdaia/allam-1-13b-instruct",
            "project_id": "cb0d224c-3a53-4fec-ab52-a5f3dd088ba2"
        }

        # Make the request to the IBM Watson X API
        try:
            response = requests.post(url, headers=headers, json=body)

            # Check for successful response
            if response.status_code == 200:
                data = response.json().get('results', [{}])[0].get('generated_text', '').strip()
                if data:
                    st.success("Réponse :")
                    st.write(data)
                else:
                    st.warning("Pas de réponse")
            else:
                st.error(f"Erreur : {response.status_code}\n{response.text}")

        except Exception as e:
            st.error(f"Une erreur est survenue : {str(e)}")

    else:
        # Adapt prompt based on interaction mode and age
        prompt = ""
        if interaction_mode == "Avancer dans le cours":
            prompt = f"Je suis un étudiant de {age} ans qui souhaite avancer dans le cours. Voici ma question : {user_input}"
        elif interaction_mode == "Discuter avec le professeur":
            prompt = f"Je suis un étudiant de {age} ans et je souhaite discuter avec le professeur. Voici ma question : {user_input}"

        # Prepare the request body
        body = {
            "input": prompt,
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": 900,
                "repetition_penalty": 1
            },
            "model_id": "sdaia/allam-1-13b-instruct",
            "project_id": "cb0d224c-3a53-4fec-ab52-a5f3dd088ba2"
        }

        # Make the request to the IBM Watson X API
        try:
            response = requests.post(url, headers=headers, json=body)

            # Check for successful response
            if response.status_code == 200:
                data = response.json().get('results', [{}])[0].get('generated_text', '').strip()
                if data:
                    st.success("Réponse :")
                    st.write(data)
                else:
                    st.warning("Pas de réponse")
            else:
                st.error(f"Erreur : {response.status_code}\n{response.text}")

        except Exception as e:
            st.error(f"Une erreur est survenue : {str(e)}")
