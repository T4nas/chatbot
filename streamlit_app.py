# streamlit_app.py

import streamlit as st
import requests

# IBM Watson X API details
url = "https://eu-de.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJraWQiOiIyMDI0MDkwMjA4NDIiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02OTIwMDBKRUY0IiwiaWQiOiJJQk1pZC02OTIwMDBKRUY0IiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiYzk0ODljMTQtYjQwNi00NzgzLWE2ODUtNDQ0YTVjZTQ5N2EyIiwiaWRlbnRpZmllciI6IjY5MjAwMEpFRjQiLCJnaXZlbl9uYW1lIjoiQW5lcyIsImZhbWlseV9uYW1lIjoiVGFpY2hhIiwibmFtZSI6IkFuZXMgVGFpY2hhIiwiZW1haWwiOiJ0aG5leXRpQHByb3Rvbm1haWwuY29tIiwic3ViIjoidGhuZXl0aUBwcm90b25tYWlsLmNvbSIsImF1dGhuIjp7InN1YiI6InRobmV5dGlAcHJvdG9ubWFpbC5jb20iLCJpYW1faWQiOiJJQk1pZC02OTIwMDBKRUY0IiwibmFtZSI6IkFuZXMgVGFpY2hhIiwiZ2l2ZW5fbmFtZSI6IkFuZXMiLCJmYW1pbHlfbmFtZSI6IlRhaWNoYSIsImVtYWlsIjoidGhuZXl0aUBwcm90b25tYWlsLmNvbSJ9LCJhY2NvdW50Ijp7InZhbGlkIjp0cnVlLCJic3MiOiJkZWQ2MzljOGQxMGY0NGIzYWU0NTg4NmU3OGYxZDJjYSIsImltc191c2VyX2lkIjoiMTI2NzY5NzUiLCJmcm96ZW4iOnRydWUsImltcyI6IjI3NDY0MTYifSwiaWF0IjoxNzI2MjQ2MjMzLCJleHAiOjE3MjYyNDk4MzMsImlzcyI6Imh0dHBzOi8vaWFtLmNsb3VkLmlibS5jb20vaWRlbnRpdHkiLCJncmFudF90eXBlIjoidXJuOmlibTpwYXJhbXM6b2F1dGg6Z3JhbnQtdHlwZTphcGlrZXkiLCJzY29wZSI6ImlibSBvcGVuaWQiLCJjbGllbnRfaWQiOiJkZWZhdWx0IiwiYWNyIjoxLCJhbXIiOlsicHdkIl19.QrEA0Ft_Vqr_BHAPiIuBmC99F_hAftMwyACLoSUPFdElAXrBbrRq8phEPOgfiVyhjxOUnDjrf0f5ECcODtv0oaqtOf9-1vskkrYjpqWLhEjYAzF3sKFLoiFmLcqNBppSBLsITg7_V-ux4CZ7yx7uR_EQbhFwIjv6X_iL-SEUZT_3-D4_zB2wgWVkTo6PeF79sE9YQ7sllkXc9_C7VaYknMBELM-y75l0DdppRZY2yHCFxn_t_0DzvMFAkJbDG-_DmUs1bYmwgqJKPzTKPPU8nSlmyzzsuofCRTMwze93nc97WDiIMgBlp0aCCaVvQ3TRa6zMbpnHtM8V6TZo7veebQ"
}

# Streamlit interface
st.title("AjurrumAI ¢")
st.write("Discute avec le plus grand spécialiste de grammaire arabe !")

# Input text from user
user_input = st.text_area("Pose ta question, ou dit ce qui te passe par la tête : ")

# Button to send the request
if st.button("Réponse"):
    if user_input.strip() == "":
        st.error("Veuillez entrer quelque-chose.")
    else:
        # Prepare the request body
        body = {
            "input": user_input,
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
                    st.success("Response:")
                    st.write(data)
                else:
                    st.warning("Pas de réponse")
            else:
                st.error(f"Error: {response.status_code}\n{response.text}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
