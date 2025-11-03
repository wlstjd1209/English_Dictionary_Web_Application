import streamlit as st
import requests

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

col1, col2, col3, col4 = st.columns([5,1,2,1])

with col1:
    # wordinput 받고 st.session_state["word"]에 저장
    wordinput = st.text_input(
        "영어 단어 입력:",
        key="word"
        
        )
#만약 wordinput받으면 기록추가
if wordinput:
    addhistory()

with col2:
    st.write("")
    st.write("")
    button1 = st.button("🔍", key="button1")
    if button1:
        addhistory()
        st.rerun()

with col3:
    selected = None
    if st.session_state["history"]:
        options = ["---선택---"] + st.session_state["history"]
        selected = st.selectbox("검색기록", options, index=0)
    elif selected == "---선택---":
        st.caption("검색할 단어를 선택하세요")
    else:
        st.caption("검색기록없음")
        
    


with col4:
    if st.session_state["history"]:
        st.write("")
        st.write("")
        button2 = st.button("🔍", key="button2")
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
        st.title(f"**✅ :blue[[*{wordinput}*]] 검색결과**")
        
        for num, data in enumerate(data1, start = 1):
            "---"
            st.info(f"#### 📌 결과 {num}")
            i+=1
            

            for mean in data["meanings"]:
                
                if "partOfSpeech" in mean:
                    meanpos = mean["partOfSpeech"]

                    if meanpos == "noun":
                        st.subheader(f"🍳:orange[**명사**]")

                    elif meanpos == "pronoun":
                        st.subheader(f"🍳:orange[**대명사**]")

                    elif meanpos == "verb":
                        st.subheader(f"🍳:orange[**동사**]")

                    elif meanpos == "adjective":
                        st.subheader(f"🍳:orange[**형용사**]")

                    elif meanpos == "adverb":
                        st.subheader(f"🍳:orange[**부사**]")   

                    elif meanpos == "preposition":
                        st.subheader(f"🍳:orange[**전치사**]")
                        
                    elif meanpos == "conjunction":
                        st.subheader(f"🍳:orange[**접속사**]")

                    elif meanpos == "interjection":
                        st.subheader(f"🍳:orange[**감탄사**]")

                    else:
                        st.subheader(f"🍳:orange[**{meanpos}**]")
                
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













