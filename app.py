import streamlit as st
from recommendation_engine import load_books, recommend_books

st.set_page_config(page_title="BookWise", page_icon="📚", layout="wide")
st.title("📚 BookWise")
st.subheader("A Rule-Based Book Recommendation Expert System")
st.write("Choose reading preferences to receive explainable recommendations from a local sample knowledge base.")
st.caption("Educational prototype using explicit rules; it does not train a machine-learning model.")
try:
    books=load_books()
except (OSError,ValueError) as exc:
    st.error(f"Could not load books.csv: {exc}")
    st.stop()
genres=sorted({x.strip() for b in books for x in b["genres"].split(";")})
themes=sorted({x.strip() for b in books for x in b["themes"].split(";")})
moods=sorted({x.strip() for b in books for x in b["mood"].split(";")})
with st.form("preferences"):
    st.markdown("### Your reading preferences")
    c1,c2=st.columns(2)
    with c1:
        selected_genres=st.multiselect("Preferred genres",genres)
        selected_themes=st.multiselect("Themes of interest",themes)
        level=st.selectbox("Reading level (optional)",["No preference","Beginner","Intermediate","Advanced"])
    with c2:
        length=st.selectbox("Preferred length (optional)",["No preference","Short","Medium","Long"])
        mood=st.selectbox("Desired mood or purpose (optional)",["No preference"]+moods)
    submitted=st.form_submit_button("Recommend books",type="primary")
if submitted:
    if not any([selected_genres,selected_themes,level!="No preference",length!="No preference",mood!="No preference"]):
        st.warning("Choose at least one preference.")
    else:
        prefs={"genres":selected_genres,"themes":selected_themes,
               "reading_level":None if level=="No preference" else level,
               "length":None if length=="No preference" else length,
               "mood":None if mood=="No preference" else mood}
        results=recommend_books(books,prefs)
        if not results:
            st.info("No matching books found. Try broadening your preferences.")
        else:
            st.markdown("### Your recommendations")
            for rank,item in enumerate(results,1):
                with st.container(border=True):
                    a,b=st.columns([3,1])
                    with a:
                        st.markdown(f"**{rank}. {item['title']}** — {item['author']}")
                        st.write(item["description"])
                        st.caption(f"Genres: {item['genres']} | Language: {item['language']} | Level: {item['reading_level']} | Length: {item['length_category']}")
                        st.write("**Why recommended:** "+"; ".join(item["reasons"]))
                    with b:
                        st.metric("Rule match",f"{item['match_percentage']}%")
                        st.caption(f"Score: {item['score']} / {item['max_score']}")
            st.info("Match percentage measures matched rule weights, not the probability that you will enjoy a book.")
st.divider()
st.caption(f"Knowledge base: {len(books)} sample records.")
