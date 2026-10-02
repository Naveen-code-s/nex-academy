import os
from pathlib import Path

import streamlit as st

from config import UPLOAD_DIR
from rag.document_loader import load_document
from rag.chunker import split_documents
from rag.vector_store import create_vector_store
from rag.pipeline import answer_question
from rag.citations import generate_citations
from rag.citation_finder import find_citations
from rag.summarizer import summarize_documents
from rag.key_information import extract_key_information


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NEXUS AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "vector_store": None,
    "documents": [],
    "chunks": [],
    "uploaded_files": [],
    "chat_history": [],
    "index_ready": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# DIRECTORIES
# ============================================================

Path(UPLOAD_DIR).mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# CSS ONLY
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(
            circle at 15% 10%,
            rgba(220, 38, 38, 0.14),
            transparent 28%
        ),
        radial-gradient(
            circle at 85% 20%,
            rgba(127, 29, 29, 0.12),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #08090d 0%,
            #0d0e13 50%,
            #130607 100%
        );
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #090a0e,
            #10090b
        );
    border-right: 1px solid rgba(239,68,68,0.18);
}

section[data-testid="stSidebar"] * {
    color: #eeeeee;
}

.stButton > button {
    border-radius: 10px;
    border: 1px solid rgba(239,68,68,0.30);
    background: linear-gradient(
        135deg,
        #991b1b,
        #ef4444
    );
    color: white;
    font-weight: 700;
    min-height: 42px;
}

.stButton > button:hover {
    border-color: #ff8585;
    box-shadow: 0 8px 25px rgba(239,68,68,0.20);
}

.stTextInput input,
.stTextArea textarea {
    background-color: #111217 !important;
    color: white !important;
    border-radius: 10px !important;
}

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.025);
    border-radius: 14px;
}

.metric-box {
    padding: 20px;
    border-radius: 16px;
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.07);
}

.feature-box {
    padding: 22px;
    border-radius: 16px;
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.07);
    min-height: 150px;
}

.source-box {
    padding: 18px;
    margin-bottom: 12px;
    border-radius: 14px;
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.07);
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("✦ NEXUS AI")

    st.caption(
        "RESEARCH INTELLIGENCE PLATFORM"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "📊 Dashboard",
            "📄 Documents",
            "🔎 Global Search",
            "🤖 Ask AI",
            "📚 Citation Finder",
            "📝 Paper Summary",
            "🧠 Key Information",
            "📈 Analytics",
            "⚙️ Settings",
        ],
    )

    st.divider()

    if st.session_state.index_ready:
        st.success("● KNOWLEDGE BASE ONLINE")
    else:
        st.warning("● KNOWLEDGE BASE EMPTY")

    st.caption(
        f"{len(st.session_state.uploaded_files)} document(s)"
    )


# ============================================================
# HELPERS
# ============================================================

def get_documents_for_source(source):
    return [
        document
        for document in st.session_state.documents
        if document.metadata.get("source") == source
    ]


def display_citations(citations):

    if not citations:
        st.info("No supporting sources found.")
        return

    for index, citation in enumerate(
        citations,
        start=1,
    ):

        source = citation.get(
            "source",
            citation.get(
                "paper",
                "Unknown source",
            ),
        )

        page = citation.get(
            "page",
            "N/A",
        )

        content = citation.get(
            "content",
            citation.get(
                "passage",
                citation.get(
                    "text",
                    "",
                ),
            ),
        )

        with st.expander(
            f"📄 {index}. {source} — Page {page}"
        ):
            st.write(content)


# ============================================================
# DASHBOARD
# ============================================================

if page == "📊 Dashboard":

    # --------------------------------------------------------
    # HERO - NO HTML
    # --------------------------------------------------------

    st.caption("✦ AI RESEARCH ASSISTANT")

    st.title(
        "Turn your documents"
    )

    st.header(
        "into intelligence."
    )

    st.write(
        "Upload research papers, search across your complete "
        "knowledge base, ask questions, find citations and "
        "generate paper summaries with source-grounded AI."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.info("RAG POWERED")

    with col2:
        st.info("GLOBAL SEARCH")

    with col3:
        st.info("SOURCE CITATIONS")

    with col4:
        st.info("MULTI DOCUMENT")

    st.divider()

    # --------------------------------------------------------
    # UPLOAD
    # --------------------------------------------------------

    st.subheader(
        "Start with your research"
    )

    st.caption(
        "Upload your research papers directly from the dashboard."
    )

    uploaded_files = st.file_uploader(
        "Upload research papers",
        type=[
            "pdf",
            "docx",
            "txt",
        ],
        accept_multiple_files=True,
    )

    if uploaded_files:

        if st.button(
            "⚡ Upload & Build Knowledge Base",
            use_container_width=True,
        ):

            all_documents = []
            saved_names = []

            progress = st.progress(0)
            status = st.empty()

            total = len(uploaded_files)

            for index, uploaded_file in enumerate(
                uploaded_files,
                start=1,
            ):

                status.info(
                    f"Processing {uploaded_file.name}..."
                )

                file_path = (
                    Path(UPLOAD_DIR)
                    / uploaded_file.name
                )

                file_path.write_bytes(
                    uploaded_file.getbuffer()
                )

                documents = load_document(
                    str(file_path)
                )

                all_documents.extend(
                    documents
                )

                saved_names.append(
                    uploaded_file.name
                )

                progress.progress(
                    int(
                        (index / total) * 50
                    )
                )

            status.info(
                "Creating chunks..."
            )

            chunks = split_documents(
                all_documents
            )

            progress.progress(70)

            status.info(
                "Building semantic index..."
            )

            vector_store = create_vector_store(
                chunks
            )

            progress.progress(100)

            st.session_state.documents = all_documents
            st.session_state.chunks = chunks
            st.session_state.vector_store = vector_store
            st.session_state.uploaded_files = saved_names
            st.session_state.index_ready = True

            status.success(
                "Knowledge base created successfully."
            )

            st.rerun()

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    st.subheader("Knowledge Base")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "Documents",
            len(
                st.session_state.uploaded_files
            ),
        )

    with m2:
        st.metric(
            "Pages / Sections",
            len(
                st.session_state.documents
            ),
        )

    with m3:
        st.metric(
            "Chunks",
            len(
                st.session_state.chunks
            ),
        )

    with m4:
        st.metric(
            "Index",
            "READY"
            if st.session_state.index_ready
            else "EMPTY",
        )

    # --------------------------------------------------------
    # FEATURES
    # --------------------------------------------------------

    st.subheader(
        "Research Intelligence"
    )

    st.caption(
        "Everything you need to work across your research library."
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            """
            <div class="feature-box">
                <h3>🔎 Global Search</h3>
                <p>Search semantically across every indexed research document.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="feature-box">
                <h3>🤖 Ask AI</h3>
                <p>Ask questions and receive source-grounded answers.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
            <div class="feature-box">
                <h3>📚 Citation Finder</h3>
                <p>Find passages that support a research claim.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            """
            <div class="feature-box">
                <h3>📝 Paper Summary</h3>
                <p>Generate structured summaries from research papers.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    c5, c6, c7, c8 = st.columns(4)

    with c5:
        st.markdown(
            """
            <div class="feature-box">
                <h3>🧠 Key Information</h3>
                <p>Extract datasets, methods, models and findings.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c6:
        st.markdown(
            """
            <div class="feature-box">
                <h3>📈 Analytics</h3>
                <p>Understand your research collection.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c7:
        st.markdown(
            """
            <div class="feature-box">
                <h3>⚡ Multi Document</h3>
                <p>Build one knowledge base from multiple papers.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c8:
        st.markdown(
            """
            <div class="feature-box">
                <h3>🔐 Source Grounded</h3>
                <p>Connect answers to retrieved document evidence.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# DOCUMENTS
# ============================================================

elif page == "📄 Documents":

    st.title("📄 Research Documents")

    st.caption(
        "Manage the documents currently loaded into NEXUS AI."
    )

    uploaded_files = st.file_uploader(
        "Add documents",
        type=[
            "pdf",
            "docx",
            "txt",
        ],
        accept_multiple_files=True,
    )

    if uploaded_files:

        if st.button(
            "⚡ Add & Index Documents",
            use_container_width=True,
        ):

            all_documents = list(
                st.session_state.documents
            )

            names = list(
                st.session_state.uploaded_files
            )

            for uploaded_file in uploaded_files:

                file_path = (
                    Path(UPLOAD_DIR)
                    / uploaded_file.name
                )

                file_path.write_bytes(
                    uploaded_file.getbuffer()
                )

                docs = load_document(
                    str(file_path)
                )

                all_documents.extend(
                    docs
                )

                if uploaded_file.name not in names:
                    names.append(
                        uploaded_file.name
                    )

            chunks = split_documents(
                all_documents
            )

            vector_store = create_vector_store(
                chunks
            )

            st.session_state.documents = all_documents
            st.session_state.chunks = chunks
            st.session_state.vector_store = vector_store
            st.session_state.uploaded_files = names
            st.session_state.index_ready = True

            st.success(
                "Documents indexed successfully."
            )

            st.rerun()

    if not st.session_state.uploaded_files:

        st.info(
            "No documents indexed yet."
        )

    for filename in st.session_state.uploaded_files:

        docs = get_documents_for_source(
            filename
        )

        st.markdown(
            f"""
            <div class="source-box">
                <h4>📄 {filename}</h4>
                <p>{len(docs)} page/section(s)</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# GLOBAL SEARCH
# ============================================================

elif page == "🔎 Global Search":

    st.title(
        "🔎 Global Semantic Search"
    )

    st.caption(
        "Search across the complete research knowledge base."
    )

    if not st.session_state.index_ready:

        st.warning(
            "Upload and index research documents first."
        )

    else:

        query = st.text_input(
            "Search your research",
            placeholder=(
                "Example: transformer architecture "
                "for medical image classification"
            ),
        )

        top_k = st.slider(
            "Number of results",
            1,
            10,
            5,
        )

        if st.button(
            "🔎 Search Knowledge Base",
            use_container_width=True,
        ):

            if not query.strip():

                st.warning(
                    "Please enter a search query."
                )

            else:

                results = (
                    st.session_state.vector_store
                    .similarity_search(
                        query,
                        k=top_k,
                    )
                )

                st.success(
                    f"Found {len(results)} relevant passages."
                )

                for index, document in enumerate(
                    results,
                    start=1,
                ):

                    source = document.metadata.get(
                        "source",
                        "Unknown",
                    )

                    page_number = document.metadata.get(
                        "page",
                        "N/A",
                    )

                    st.markdown(
                        f"""
                        <div class="source-box">
                            <h4>
                                {index}. 📄 {source}
                            </h4>
                            <p>
                                Page {page_number}
                            </p>
                            <p>
                                {document.page_content}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


# ============================================================
# ASK AI
# ============================================================

elif page == "🤖 Ask AI":

    st.title("🤖 Ask NEXUS AI")

    st.caption(
        "Ask questions grounded in your uploaded research."
    )

    if not st.session_state.index_ready:

        st.warning(
            "Upload and index research documents first."
        )

    else:

        question = st.text_area(
            "Research Question",
            placeholder=(
                "Example: What methodology was used "
                "to evaluate the proposed model?"
            ),
            height=120,
        )

        if st.button(
            "🤖 Generate Research Answer",
            use_container_width=True,
        ):

            if not question.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                with st.spinner(
                    "Searching sources and generating answer..."
                ):

                    answer, documents = answer_question(
                        st.session_state.vector_store,
                        question,
                    )

                st.subheader("Answer")

                st.write(answer)

                st.divider()

                st.subheader(
                    "📚 Supporting Sources"
                )

                citations = generate_citations(
                    documents
                )

                display_citations(
                    citations
                )


# ============================================================
# CITATION FINDER
# ============================================================

elif page == "📚 Citation Finder":

    st.title(
        "📚 Citation Finder"
    )

    st.caption(
        "Find passages that support a research claim."
    )

    if not st.session_state.index_ready:

        st.warning(
            "Upload and index research documents first."
        )

    else:

        claim = st.text_area(
            "Research Claim",
            placeholder=(
                "Example: RAG reduces hallucination "
                "in domain-specific question answering."
            ),
            height=120,
        )

        top_k = st.slider(
            "Supporting passages",
            1,
            10,
            5,
        )

        if st.button(
            "📚 Find Supporting Citations",
            use_container_width=True,
        ):

            if not claim.strip():

                st.warning(
                    "Please enter a claim."
                )

            else:

                with st.spinner(
                    "Finding supporting evidence..."
                ):

                    citations = find_citations(
                        st.session_state.vector_store,
                        claim,
                        top_k=top_k,
                    )

                display_citations(
                    citations
                )


# ============================================================
# PAPER SUMMARY
# ============================================================

elif page == "📝 Paper Summary":

    st.title(
        "📝 Paper Summary"
    )

    st.caption(
        "Generate a structured summary from an indexed research paper."
    )

    if not st.session_state.uploaded_files:

        st.warning(
            "Upload a research paper first."
        )

    else:

        selected_source = st.selectbox(
            "Select paper",
            st.session_state.uploaded_files,
        )

        documents = get_documents_for_source(
            selected_source
        )

        if st.button(
            "📝 Generate Paper Summary",
            use_container_width=True,
        ):

            with st.spinner(
                "Analyzing paper..."
            ):

                summary = summarize_documents(
                    documents
                )

            st.markdown(summary)


# ============================================================
# KEY INFORMATION
# ============================================================

elif page == "🧠 Key Information":

    st.title(
        "🧠 Key Information Extraction"
    )

    st.caption(
        "Extract structured research information."
    )

    if not st.session_state.uploaded_files:

        st.warning(
            "Upload a research paper first."
        )

    else:

        selected_source = st.selectbox(
            "Select paper",
            st.session_state.uploaded_files,
        )

        documents = get_documents_for_source(
            selected_source
        )

        if st.button(
            "🧠 Extract Key Information",
            use_container_width=True,
        ):

            with st.spinner(
                "Extracting research information..."
            ):

                information = extract_key_information(
                    documents
                )

            st.markdown(information)


# ============================================================
# ANALYTICS
# ============================================================

elif page == "📈 Analytics":

    st.title(
        "📈 Research Analytics"
    )

    st.caption(
        "Overview of your indexed research collection."
    )

    if not st.session_state.documents:

        st.info(
            "Upload documents to generate analytics."
        )

    else:

        source_counts = {}

        for document in st.session_state.documents:

            source = document.metadata.get(
                "source",
                "Unknown",
            )

            source_counts[source] = (
                source_counts.get(
                    source,
                    0,
                )
                + 1
            )

        a, b, c = st.columns(3)

        with a:
            st.metric(
                "Documents",
                len(source_counts),
            )

        with b:
            st.metric(
                "Pages / Sections",
                len(
                    st.session_state.documents
                ),
            )

        with c:
            st.metric(
                "Chunks",
                len(
                    st.session_state.chunks
                ),
            )

        st.subheader(
            "Documents"
        )

        for source, count in source_counts.items():

            st.write(
                f"📄 **{source}** — {count} page/section(s)"
            )


# ============================================================
# SETTINGS
# ============================================================

elif page == "⚙️ Settings":

    st.title(
        "⚙️ Settings"
    )

    st.caption(
        "NEXUS AI configuration and system information."
    )

    st.subheader(
        "System"
    )

    st.info(
        "RAG Engine: FAISS + HuggingFace Embeddings"
    )

    st.info(
        "AI Engine: Groq Language Model"
    )

    st.info(
        "Supported files: PDF, DOCX, TXT"
    )

    st.subheader(
        "Knowledge Base"
    )

    st.write(
        f"Documents: {len(st.session_state.uploaded_files)}"
    )

    st.write(
        f"Pages / Sections: {len(st.session_state.documents)}"
    )

    st.write(
        f"Chunks: {len(st.session_state.chunks)}"
    )

    if st.button(
        "🗑️ Clear Current Knowledge Base",
        use_container_width=True,
    ):

        st.session_state.vector_store = None
        st.session_state.documents = []
        st.session_state.chunks = []
        st.session_state.uploaded_files = []
        st.session_state.chat_history = []
        st.session_state.index_ready = False

        st.success(
            "Knowledge base cleared."
        )

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "NEXUS AI • Research Intelligence Platform • RAG Powered • Source Grounded"
)