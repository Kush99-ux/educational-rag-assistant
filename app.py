import os
import streamlit as st
import re

from src.core.service_container import (
    ServiceContainer
)

from src.models.quiz_request import (
    QuizRequest
)

from src.models.quiz_attempt import (
    QuizAttempt
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

if "quiz_result" not in st.session_state: 
    st.session_state.quiz_result = ""

if "quiz_evaluation" not in st.session_state:

    st.session_state.quiz_evaluation = None

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

    if st.button(
        "🗑 Clear Knowledge Base"
    ):

        try:

            # Delete persisted files

            if os.path.exists(
                "vector_store/faiss.index"
            ):

                os.remove(
                    "vector_store/faiss.index"
                )

            if os.path.exists(
                "vector_store/chunks.pkl"
            ):

                os.remove(
                    "vector_store/chunks.pkl"
                )

            # Reset session state

            st.session_state.documents = []

            st.session_state.total_chunks = 0

            st.session_state.chat_history = []

            st.session_state.quiz_result = ""

            st.session_state.quiz_evaluation = None

            st.session_state.loaded_from_disk = False

            # Fresh container

            st.session_state.container = (
                ServiceContainer()
            )

            st.success(
                "Knowledge Base Cleared"
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Error clearing knowledge base: {e}"
            )

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

    # ----------------------------------------------
    # Quiz Section 
    # ----------------------------------------------

    st.divider()

    with st.expander(
        "🧠 Quiz Generator",
        expanded=False
    ):

        quiz_difficulty = st.selectbox(
            "Difficulty",
            [
                "easy",
                "medium",
                "hard",
                "mixed"
            ]
        )

        quiz_length = st.selectbox(
            "Questions",
            [
                5,
                10,
                20,
                50
            ]
        )

        quiz_topics = st.text_input(
            "Topics (comma separated)"
        )

        quiz_exam_mode = st.checkbox(
            "Exam Focused"
        )

        generate_quiz = st.button(
            "Generate Quiz"
        )

        if st.button("Clear Quiz"): 
            st.session_state.quiz_result = ""
            st.session_state.quiz_evaluation = None
            st.rerun()

        if generate_quiz:

            if len(
                st.session_state.documents
            ) == 0:

                st.warning(
                    "Please index a document first."
                )

            else:

                topic_list = []

                if quiz_topics.strip():

                    topic_list = [

                        topic.strip()

                        for topic in quiz_topics.split(",")
                    ]

                request = QuizRequest(

                    difficulty=
                    quiz_difficulty,

                    length=
                    quiz_length,

                    topics=
                    topic_list,

                    exam_focused=
                    quiz_exam_mode
                )

                try:

                    with st.spinner(
                        "Generating quiz..."
                    ):

                        result = (

                            st.session_state
                            .container
                            .quiz_service
                            .generate_quiz(
                                request
                            )

                        )

                    for key in list(st.session_state.keys()):
                        if key.startswith("quiz_choice_"):
                            del st.session_state[key]

                    st.session_state.quiz_result = (
                        result.quiz_text
                    )

                    st.session_state.quiz_evaluation = None

                except Exception as e:

                    st.error(
                        f"Error generating quiz: {e}"
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

chat_tab, quiz_tab = st.tabs(["💬 Q&A Chat", "🧠 Interactive Quiz"])

with quiz_tab:

    if st.session_state.quiz_result:

        st.subheader(
            "📝 Generated Quiz"
        )

        st.markdown(
            st.session_state.quiz_result
        )

        st.divider()

        questions = re.findall(

            r"Question\s+\d+:",

            st.session_state.quiz_result

        )

        if len(questions) == 0:

            st.warning(
                "Could not cleanly extract distinct question tokens from the quiz. Please try re-generating."
            )

        else:

            user_answers = []

            for i in range(
                len(questions)
            ):

                default_opts = ["A", "B", "C", "D"]
                saved_key = f"quiz_choice_{i}"

                answer = st.selectbox(

                    f"Question {i+1} Answer",

                    default_opts,

                    key=saved_key

                )

                user_answers.append(
                    answer
                )

            if st.button(
                "Submit Quiz"
            ):

                attempt = QuizAttempt(

                    quiz_text=
                    st.session_state.quiz_result,

                    user_answers=
                    user_answers
                )

                evaluation = (

                    st.session_state
                    .container
                    .quiz_evaluator
                    .evaluate(
                        attempt
                    )

                )

                st.session_state.quiz_evaluation = (
                    evaluation
                )

                st.rerun()

        if (
            st.session_state.quiz_evaluation
        ):

            st.divider()

            evaluation = (
                st.session_state.quiz_evaluation
            )

            st.subheader(
                "📊 Quiz Results"
            )

            st.success(

                f"Score: "

                f"{evaluation.score}/"

                f"{evaluation.total_questions}"
            )

            st.metric(

                "Accuracy",

                f"{evaluation.accuracy:.2f}%"
            )

            st.info(
                evaluation.feedback
            )

            st.write(
                "Correct Answers:"
            )

            for i, answer in enumerate(

                evaluation.correct_answers,

                start=1

            ):

                st.write(
                    f"Q{i}: {answer}"
                )

            if len(
                evaluation.incorrect_questions
            ) > 0:

                st.warning(

                    "Incorrect Questions: "

                    + ", ".join(

                        str(q)

                        for q in
                        evaluation.incorrect_questions
                    )
                )

            if st.button("🗑 Dismiss Results"):
                st.session_state.quiz_evaluation = None
                st.rerun()

    else:

        st.info("No active quiz. Generate a quiz from the sidebar.")

with chat_tab:

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

            if "sources" in message and message["sources"]:

                st.markdown(
                    "#### Sources"
                )

                for source in (
                    message["sources"]
                ):

                    with st.expander(
                        f"📄 {source['source_name']} | Chunk {source['chunk_index']}"
                    ):

                        st.write(
                            f"Similarity Score: {source['score']:.3f}"
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
            # SAVE USER MESSAGE TO STATE
            # ------------------------------------------

            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": question
                }
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
                        question,
                        st.session_state.chat_history[:-1]
                    )
                )


            # ------------------------------------------
            # SAVE ASSISTANT MESSAGE & SOURCES TO STATE
            # ------------------------------------------

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": response.answer,
                    "sources": response.sources
                }
            )

            st.rerun()