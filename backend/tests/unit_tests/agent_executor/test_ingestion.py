from langchain.text_splitter import RecursiveCharacterTextSplitter

from agent_executor.upload import IngestRunnable
from agent_executor.upload import _guess_mimetype
from tests.unit_tests.agent_executor.utils import InMemoryVectorStore
from tests.unit_tests.fixtures import list_fixtures


def test_ingestion_runnable() -> None:
    """Test ingestion runnable"""
    vectorstore = InMemoryVectorStore()
    splitter = RecursiveCharacterTextSplitter()
    runnable = IngestRunnable(
        text_splitter=splitter,
        vectorstore=vectorstore,
        input_key="file_contents",
        namespace="test1",
    )
    ids = runnable.invoke({"file_contents": "This is a test file."})
    assert len(ids) == 1


def test_mimetype_guessing() -> None:
    """Verify mimetype guessing for all fixtures."""
    name_to_mime = {}
    for file in sorted(list_fixtures()):
        data = file.read_bytes()
        name_to_mime[file.name] = _guess_mimetype(data)

    assert {
        "sample.docx": (
            "application/vnd.openxmlformats-officedocument." "wordprocessingml.document"
        ),
        "sample.epub": "application/epub+zip",
        "sample.html": "text/html",
        "sample.odt": "application/vnd.oasis.opendocument.text",
        "sample.pdf": "application/pdf",
        "sample.rtf": "text/rtf",
        "sample.txt": "text/plain",
    } == name_to_mime
