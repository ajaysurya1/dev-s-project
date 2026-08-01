import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from api_client import get_documents, ask_question


def show():
    st.markdown("## Ask a Question")
    st.markdown("Type a question and get an answer from your uploaded documents.")
    st.markdown("---")

    documents_response = get_documents()

    if documents_response.status_code != 200:
        st.error("Could not load documents. Is the backend running?")
        return

    documents = documents_response.json()

    if len(documents) == 0:
        st.info("No documents found. Upload a document first before asking questions.")
        return

    st.markdown("**Filter by document (optional)**")
    document_options = {doc["name"]: doc["id"] for doc in documents}
    selected_names = st.multiselect(
        "Select documents to search in (leave blank to search all)",
        options=list(document_options.keys()),
        label_visibility="collapsed"
    )

    selected_ids = [document_options[name] for name in selected_names]

    st.markdown("")
    st.markdown("**Your question**")
    question = st.text_area(
        "Enter your question here",
        placeholder="What is this document about? What are the main findings?",
        height=100,
        label_visibility="collapsed"
    )

    st.markdown("")

    if st.button("Get Answer"):
        if not question.strip():
            st.warning("Please enter a question before submitting.")
            return

        with st.spinner("Finding answer..."):
            ids_to_send = selected_ids if selected_ids else None
            response = ask_question(question, ids_to_send)

        if response.status_code == 200:
            result = response.json()
            answer = result.get("answer", "No answer returned.")
            sources = result.get("sources", [])
            confidence = result.get("confidence", 0.0)
            confidence_percent = round(confidence * 100, 1)

            st.markdown("### Answer")
            st.markdown(
                "<div class='answer-box'>" + answer + "</div>",
                unsafe_allow_html=True
            )

            st.markdown("")
            st.metric(label="Confidence Score", value=str(confidence_percent) + "%")

            if sources:
                st.markdown("")
                st.markdown("### Sources")
                seen_names = []
                for source in sources:
                    if source["document_name"] not in seen_names:
                        seen_names.append(source["document_name"])
                        st.markdown(
                            "<span class='source-tag'>" + source["document_name"] + "</span>",
                            unsafe_allow_html=True
                        )

                st.markdown("")
                for index in range(len(sources)):
                    source = sources[index]
                    with st.expander("Source " + str(index + 1) + " - " + source["document_name"]):
                        score_text = str(round(source["relevance_score"], 3))
                        st.markdown("**Relevance score:** " + score_text)
                        st.markdown("**Chunk index:** " + str(source["chunk_index"]))
                        st.markdown("**Excerpt:**")
                        st.text(source["excerpt"])
            else:
                st.info("No sources were found for this answer.")

        else:
            error_message = "Request failed."
            try:
                error_message = response.json().get("detail", error_message)
            except Exception:
                pass
            st.error(error_message)
