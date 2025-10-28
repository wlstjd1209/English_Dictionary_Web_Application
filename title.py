import streamlit as st
import requests

st.columns(6)





st.title(":violet[영어 단어 사전]")

if "history" not in st.session_state:
    st.session_state["history"] = []
if "word" not in st.session_state:
    st.session_state["word"] = ""
    
col1, col2 = st.columns([3,1])

with col1:
    wordinput = st.text_input("영어 단어 입력:", st.session_state["word"])

with col2:
    if st.session_state["history"]:
        selected = st.selectbox("검색기록", st.session_state["history"])
        if selected and selected != st.session_state["word"]:
            st.session_state["word"] = selected
    
    
if wordinput:  # "" -> False, "bla-bla~" -> True
    if st.session_state["word"] not in st.session_state["history"]:
        st.session_state["history"].insert(0, wordinput)

    
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{wordinput}"
    response = requests.get(url)
    data1 = response.json()

    i=0

    upcountry = ["UK", "US"]
    lowcountry = ["uk", "us"]

    if response.status_code == 200:
        st.title(f"**:blue[[*{wordinput}*]]에 대한 정보**")
        
        for num, data in enumerate(data1, start = 1):
            "---"
            with st.container():
                st.write(num)
                i+=1
    
                for mean in data["meanings"]:
                    
                    if "partOfSpeech" in mean:
                        meanpos = mean["partOfSpeech"]
    
                        if meanpos == "noun":
                            st.subheader(f":orange[**명사**]")
    
                        elif meanpos == "pronoun":
                            st.subheader(f":orange[**대명사**]")
    
                        elif meanpos == "verb":
                            st.subheader(f":orange[**동사**]")
    
                        elif meanpos == "adjective":
                            st.subheader(f":orange[**형용사**]")
    
                        elif meanpos == "adverb":
                            st.subheader(f":orange[**부사**]")   
    
                        elif meanpos == "preposition":
                            st.subheader(f":orange[**전치사**]")
                            
                        elif meanpos == "conjunction":
                            st.subheader(f":orange[**접속사**]")
    
                        elif meanpos == "interjection":
                            st.subheader(f":orange[**감탄사**]")
    
                        else:
                            st.subheader(f":orange[**{meanpos}**]")
                    
                    with st.expander("🔽 정의&예문"):
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
                                        st.caption("EXAMPLE IS NOT PROVIDED")
                                    else:
                                        st.caption(f"ex) {meanex}")
                                                
                    with st.expander("🔽 유의어/동의어"):
                        if "synonyms" in mean:
                            
                            dbdmldjemf = mean["synonyms"]
    
                            if dbdmldjemf == []:
                                    st.caption(f"SYNONYM IS NOT FOUND")
                            else:
                                for kkkk, meansyn in enumerate(dbdmldjemf, start = 1):
                                    st.markdown(f"{kkkk}. :orange[{meansyn}]")
                        else:
                            st.caption(f"SYNONYM IS NOT FOUND")
    
                    with st.expander("🔽 반의어"):
                        if "antonyms" in mean:
                            
                            qksdmldjemf = mean["antonyms"]
    
                            if qksdmldjemf == []:
                                    st.caption(f"ANTONYM IS NOT FOUND")
                            else:
                                for kkkkk, meanant in enumerate(qksdmldjemf, start = 1):
                                    st.markdown(f"{kkkkk}. :orange[{meanant}]")
                        else:
                            st.caption(f"ANTONYM IS NOT FOUND")
    
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
                                    st.write(f"**🔊발음 : {textpho}**  :green[*(US)*]")
                                elif audiopho[-5] == "k":
                                    st.write(f"**🔊발음 : {textpho}**  :green[*(UK)*]")
                                else:
                                    continue
                                st.audio(audioresponse.content, format = "audio/mp3")


    else:
        st.error(f"""단어 정보를 가져오는 데 실패했습니다. (상태 코드 : **{response.status_code}**)""")
else:
    st.warning("단어를 입력해주세요.")

st.rerun()




