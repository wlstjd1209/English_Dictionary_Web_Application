import streamlit as st
import requests
import streamlit_authenticator as stauth
import pandas as pd
import time

st.title("Login")

if "onoff" not in st.session_state:
    st.session_state["onoff"] = ""

data = pd.read_csv("members.csv")
data["PW"] = data["PW"].astype(str)

with st.form("login_form"):
    ID = st.text_input("ID", placeholder="아이디를 입력하세요")
    PW = st.text_input("Password", type="password", placeholder="비밀번호를 입력하세요")
    submit_button = st.form_submit_button("Login")

if submit_button:
    if not ID or not PW:
        st.warning("ID와 비밀번호를 모두 입력해주세요.")
    else:
        # 사용자 확인
        user = data[(data["ID"] == ID) & (data["PW"] == str(PW))]
        
        if not user.empty:
            
            st.success(f"Login successful")
            st.session_state["ID"]=ID
            
            progress_text = "로그인 중입니다."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            time.sleep(1)
            my_bar.empty()
            
            st.session_state["onoff"] = "True"
            
            
        else:
            st.error("아이디 또는 비밀번호가 일치하지 않습니다.")

"---"
"---"
if st.session_state["onoff"]:

    st.set_page_config(page_title="영어 단어 사전", page_icon="📚")

    st.title("📚 영어 단어 사전")
    # 
    if "history" not in st.session_state:
        st.session_state["history"] = []
    if "word" not in st.session_state:
        st.session_state["word"] = ""
    if "message" not in st.session_state:
        st.session_state["message"] = ""

    def addhistory():
        if st.session_state["word"] in st.session_state["history"]:
            st.session_state["history"].remove(st.session_state["word"])
            st.session_state["history"].insert(0, st.session_state["word"])
        elif st.session_state["word"] not in st.session_state["history"]:
            st.session_state["history"].insert(0, st.session_state["word"])

        # 10개 제한
        if len(st.session_state["history"]) > 10:
            st.session_state["history"].pop(-1)
        
    def historyinput():
        st.session_state["word"]

    # def set_word():

    col1, col2 = st.columns([4,1])

    with col1:
        # wordinput 받고 st.session_state["word"]에 저장
        wordinput = st.text_input(
            "📝 영어 단어 입력:",
            key="word"
            
            )
    #만약 wordinput받으면 기록추가
    if wordinput:
        addhistory()

    with col2:
        st.write("")
        st.write("")
        button1 = st.button("검색", key="button1", use_container_width=True)
        if button1:
            addhistory()
            st.rerun()

    col3, col4 = st.columns([4,1])

    with col3:
        selected = None
        if st.session_state["history"]:
            options = ["---선택---"] + st.session_state["history"]
            selected = st.selectbox("🕒 최근 검색 기록", options, index=0)
        elif selected == "---선택---":
            st.caption("검색할 단어를 선택하세요")
        else:
            st.caption("검색기록없음")
            
        


    with col4:
        if st.session_state["history"]:
            st.write("")
            st.write("")
            button2 = st.button("검색", key="button2", use_container_width=True)
            if button2:
                if selected == "---선택---":
                    st.session_state["message"] = "**검색할 단어를 선택하세요**"
                elif selected != "---선택---":
                    st.session_state["message"] = ""
                wordinput = selected
                # st.rerun()
                # addhistory()
    if st.session_state["message"]:
        st.markdown(
            f"<p style='text-align:right; color: #d97706; font-weight:600;'>{st.session_state['message']}</p>",
            unsafe_allow_html=True
        )


    if wordinput:  # "" -> False, "bla-bla~" -> True
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{wordinput}"

        response = requests.get(url)

        # st.write(response.status_code)
        data1 = response.json()
        # trial = response.json()[0]
        # st.write(data1)
        # st.write(trial)



        i=0


        upcountry = ["UK", "US"]
        lowcountry = ["uk", "us"]

        if response.status_code == 200:
            "---"
            st.markdown(f"## **✅ :blue[[*{wordinput}*]] 검색결과**")
            st.write("")
            for num, data in enumerate(data1, start = 1):
                if i > 0:
                    "---"
                st.markdown(f"#### 📌 결과 {num}")
                i+=1
                

                for mean in data["meanings"]:
                    
                    if "partOfSpeech" in mean:
                        meanpos = mean["partOfSpeech"]

                        if meanpos == "noun":
                            st.markdown(f"###### 🍳명사")

                        elif meanpos == "pronoun":
                            st.markdown(f"###### 🍳대명사")

                        elif meanpos == "verb":
                            st.markdown(f"###### 🍳동사")

                        elif meanpos == "adjective":
                            st.markdown(f"###### 🍳형용사")

                        elif meanpos == "adverb":
                            st.markdown(f"###### 🍳부사")   

                        elif meanpos == "preposition":
                            st.markdown(f"###### 🍳전치사")
                            
                        elif meanpos == "conjunction":
                            st.markdown(f"###### 🍳접속사")

                        elif meanpos == "interjection":
                            st.markdown(f"###### 🍳감탄사")

                        else:
                            st.markdown(f"###### 🍳{meanpos}")
                    
                    with st.expander("📖 정의&예문"):
                        kkk=0
                        if "definitions" in mean:

                            for wjddmlemf in mean["definitions"]:
                                kkk+=1
                                if "definition" in wjddmlemf:
                                    meandef = wjddmlemf["definition"]

                                    if "example" in wjddmlemf:
                                        meanex = wjddmlemf["example"]
                                    else:
                                        meanex = "NOT FOUND"
                                    st.markdown(f"{kkk}. :orange[{meandef}]")
                                    if meanex == "NOT FOUND":
                                        st.caption("EXAMPLE IS NOT FOUND")
                                    else:
                                        st.caption(f"ex) {meanex}")
                                                
                    with st.expander("📙 유의어"):
                        if "synonyms" in mean:
                            
                            dbdmldjemf = mean["synonyms"]

                            if dbdmldjemf == []:
                                    st.caption(f"SYNONYM IS NOT FOUND")
                            else:
                                for kkkk, meansyn in enumerate(dbdmldjemf, start = 1):
                                    st.markdown(f"{kkkk}. :orange[{meansyn}]")
                        else:
                            st.caption(f"SYNONYM IS NOT FOUND")


                    with st.expander("📘 반의어"):
                        if "antonyms" in mean:
                            
                            qksdmldjemf = mean["antonyms"]

                            if qksdmldjemf == []:
                                    st.caption(f"ANTONYM IS NOT FOUND")
                            else:
                                for kkkkk, meanant in enumerate(qksdmldjemf, start = 1):
                                    st.markdown(f"{kkkkk}. :orange[{meanant}]")
                        else:
                            st.caption(f"ANTONYM IS NOT FOUND")

                    # if "antonyms" in mean:
                    #     st.subheader(f"**반의어 :**")
                        
                    #     meanann = mean["antonyms"]

                    #     st.json(meanann)



                            
                # for pho in data["phonetics"]:
                #         if "text" in pho:
                #             textpho = pho["text"]
                            
                #             st.write(f"**발음 : {textpho}**  :green[*({upcountry[k]})*]")
                #             k+=1
                #         else:
                #             st.write(f"*:red[Text is Not Found]*")

                #         if "audio" in pho:
                #             audiopho = pho["audio"]
                #             audioresponse = requests.get(audiopho)
                #             st.audio(audioresponse.content, format = "audio/mp3")
                #         else:
                #             st.write(f"*:red[Audio is Not Found]*")

                for pho in data["phonetics"]:
                    if "text" in pho:
                        textpho = pho["text"]
                        if "audio" in pho:
                            audiopho = pho["audio"]
                            if audiopho == "":
                                continue
                            else:
                                audioresponse = requests.get(audiopho)

                                if audiopho[-5] == "s":
                                    st.write(f"**🔊 발음 : {textpho}**  :green[*(US)*]")
                                elif audiopho[-5] == "k":
                                    st.write(f"**🔊 발음 : {textpho}**  :green[*(UK)*]")
                                else:
                                    continue
                                st.audio(audioresponse.content, format = "audio/mp3")




                # for pho in data["phonetics"]:
                #         if "text" in pho:
                #             textpho = pho["text"]
                            # if "audio" in pho:
                            #     audiopho = pho["audio"]
                            #     audioresponse = requests.get(audiopho)

                            #     if audiopho[-5] == "s":
                            #         button = st.button(f"**🔊발음 : {textpho}**  :green[*(US)*]")
                            #     elif audiopho[-5] == "k":
                            #         button = st.button(f"**🔊발음 : {textpho}**  :green[*(UK)*]")
                            #     else:
                            #         continue


                #                 if button:
                #                     st.audio(audioresponse.content, format = "audio/mp3")


        else:
            st.error(f"""단어 정보를 가져오는 데 실패했습니다💦 (상태 코드 : **{response.status_code}**)""")
    else:
        st.warning("단어를 입력해주세요.")



        