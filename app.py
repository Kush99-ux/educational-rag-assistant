import os
import streamlit as st

from src.core.service_container import (
    ServiceContainer
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Educational RAG Assistant",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "container" not in st.session_state:

    st.session_state.container = (
        ServiceContainer()
    )

    try:

        st.session_state.container.vector_store.load(
            "vector_store"
        )

        loaded_chunks = (
            st.session_state.container
            .vector_store
            .embedded_chunks
        )

        st.session_state.total_chunks = (
            len(loaded_chunks)
        )

        documents = set()

        for chunk in loaded_chunks:

            documents.add(
                chunk.metadata[
                    "source_name"
                ]
            )

        st.session_state.documents = (
            list(documents)
        )

        st.session_state.loaded_from_disk = True

    except Exception:

        st.session_state.loaded_from_disk = False

if "documents" not in st.session_state:
    st.session_state.documents = []

if "total_chunks" not in st.session_state:
    st.session_state.total_chunks = 0

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title(
        "📚 Knowledge Base"
    )

    if st.session_state.get(
        "loaded_from_disk",
        False
    ):

        st.success(
            "Knowledge Base Loaded"
        )

    else:

        st.info(
            "No Saved Knowledge Base"
        )

    # ----------------------------------------------
    # FILE UPLOAD
    # ----------------------------------------------

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file:

        save_path = os.path.join(
            "data",
            "raw",
            uploaded_file.name
        )

        os.makedirs(
            "data/raw",
            exist_ok=True
        )

        with open(
            save_path,
            "wb"
        ) as f:

            f.write(
                uploaded_file.getbuffer()
            )

        st.success(
            f"{uploaded_file.name} uploaded."
        )

        if st.button(
            "Index Document"
        ):

            with st.spinner(
                "Indexing document..."
            ):

                chunk_count = (
                    st.session_state.container
                    .ingestion_service
                    .ingest(save_path)
                )

            if uploaded_file.name not in (
                st.session_state.documents
            ):

                st.session_state.documents.append(
                    uploaded_file.name
                )

            st.session_state.total_chunks += (
                chunk_count
            )

            st.session_state.container.vector_store.save(
                "vector_store"
            )

            st.success(
                f"Indexed {chunk_count} chunks."
            )

    st.divider()

    # ----------------------------------------------
    # CHAT CONTROLS
    # ----------------------------------------------

    if st.button(
        "🧹 Clear Chat History"
    ):

        st.session_state.chat_history = []

        st.rerun()

    st.divider()

    # ----------------------------------------------
    # DOCUMENT LIST
    # ----------------------------------------------

    st.subheader(
        "Indexed Documents"
    )

    if len(
        st.session_state.documents
    ) == 0:

        st.info(
            "No documents indexed yet."
        )

    else:

        for doc in (
            st.session_state.documents
        ):

            st.write(
                f"📄 {doc}"
            )

    st.divider()

    # ----------------------------------------------
    # STATS
    # ----------------------------------------------

    st.subheader(
        "Knowledge Base Stats"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Documents",
            len(
                st.session_state.documents
            )
        )

    with col2:

        st.metric(
            "Chunks",
            st.session_state.total_chunks
        )

# --------------------------------------------------
# MAIN AREA
# --------------------------------------------------

st.title(
    "🎓 Educational RAG Assistant"
)

st.caption(
    "Ask questions about your uploaded documents."
)

# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in (
    st.session_state.chat_history
):

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )

# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

question = st.chat_input(
    "Ask a question about your documents..."
)

# --------------------------------------------------
# QUESTION ANSWERING
# --------------------------------------------------

if question:

    if len(
        st.session_state.documents
    ) == 0:

        st.warning(
            "Please index a document first."
        )

    else:

        # ------------------------------------------
        # SHOW USER MESSAGE
        # ------------------------------------------

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message(
            "user"
        ):

            st.write(
                question
            )

        # ------------------------------------------
        # GENERATE ANSWER
        # ------------------------------------------

        with st.spinner(
            "Generating answer..."
        ):

            response = (
                st.session_state.container
                .rag_pipeline
                .answer(
                    question
                )
            )

        # ------------------------------------------
        # DEBUG OUTPUT
        # ------------------------------------------

        print("\nRAW SOURCES")

        for source in response.sources:

            print(source)

        # ------------------------------------------
        # SAVE ASSISTANT MESSAGE
        # ------------------------------------------

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": response.answer
            }
        )

        # ------------------------------------------
        # SHOW ASSISTANT MESSAGE
        # ------------------------------------------

        with st.chat_message(
            "assistant"
        ):

            st.write(
                response.answer
            )

            st.markdown(
                "#### Sources"
            )

            for source in (
                response.sources
            ):

                with st.expander(
                    f"📄 {source['source_name']} | Chunk {source['chunk_index']}"
                ):

                    st.write(
                        f"Similarity Score: {source['score']:.3f}"
                    )