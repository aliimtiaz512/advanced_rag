import streamlit as st

st.set_page_config(page_title="Naive RAG Q&A",layout="wide")

hide_st_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
from ingestion import collection     
from generation import generate_answer, evaluate_query, generate_query_options

st.title("📚 The Great Gatsby Q&A Explorer")
st.markdown("Ask questions, explore themes, and analyze characters from **The Great Gatsby**. \n\n*Our intelligent pre-retrieval system checks query clarity before searching the text!*")

try:
    count = collection.count()
    st.caption(f"Documents in vector store: **{count:,}** chunks")
except:
    st.caption("Could not read collection size")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question about your documents …"):
    # Clear any pending states
    st.session_state.pending_options = None
    st.session_state.selected_query = None
    
    st.session_state.messages.append({"role":"user","content":prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Evaluating query meaning and spelling..."):
        score = evaluate_query(prompt)

    # Display Confidence Score on frontend
    if score >= 80:
        st.success(f"**Confidence Score:** {score}% - *Good question! Searching the novel...*", icon="✅")
    else:
        st.warning(f"**Confidence Score:** {score}% - *Query unclear or not related to Gatsby.*", icon="⚠️")

    if score >= 80:
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                try:
                    answer = generate_answer(prompt)
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.caption("Make sure GROQ_API_KEY is set and Chroma is running.")
    else:
        with st.spinner("Refining your query..."):
            options = generate_query_options(prompt)
            if options:
                st.session_state.pending_options = options
                st.rerun()
            else:
                # Fallback if options generation fails
                with st.chat_message("assistant"):
                    with st.spinner("Thinking…"):
                        try:
                            answer = generate_answer(prompt)
                            st.markdown(answer)
                            st.session_state.messages.append({"role": "assistant", "content": answer})
                        except Exception as e:
                            st.error(f"Error: {str(e)}")

# Display options if any
if st.session_state.get("pending_options"):
    with st.chat_message("assistant"):
        st.markdown("Your query might be unclear or have spelling errors. Did you mean one of these?")
        for opt in st.session_state.pending_options:
            if st.button(opt):
                st.session_state.pending_options = None
                st.session_state.messages.append({"role": "user", "content": opt})
                st.session_state.selected_query = opt
                st.rerun()
        if st.button("Cancel & Try Again", type="secondary"):
            st.session_state.pending_options = None
            st.rerun()

# Process selected query
if st.session_state.get("selected_query") is not None:
    q = st.session_state.selected_query
    st.session_state.selected_query = None
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                answer = generate_answer(q)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Sidebar Styling
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("---")
    st.markdown("**About this App:**")
    st.markdown("This system evaluates your query first. If it's clear and related to Gatsby, it retrieves the answer. Otherwise, it helps refine your question.")
    st.markdown("---")
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages=[]
        st.rerun()