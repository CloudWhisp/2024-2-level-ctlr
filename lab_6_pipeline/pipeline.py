"""
Pipeline for CONLL-U formatting.
"""

# pylint: disable=too-few-public-methods, undefined-variable, too-many-nested-blocks
import pathlib
import os
import re

from networkx import DiGraph

from core_utils.article.article import Article
from core_utils.article.io import to_cleaned
from core_utils.pipeline import (
    AbstractCoNLLUAnalyzer,
    CoNLLUDocument,
    LibraryWrapper,
    PipelineProtocol,
    StanzaDocument,
    TreeNode,
    UDPipeDocument,
    UnifiedCoNLLUDocument,
)
from core_utils.constants import ASSETS_PATH

class InconsistentDatasetError(Exception):
    '''Data in directory is inconsistent'''

class EmptyDirectoryError(Exception):
    '''Directory is empty'''

class EmptyFileError(Exception):
    ''''''

class CorpusManager:
    """
    Work with articles and store them.
    """

    def __init__(self, path_to_raw_txt_data: pathlib.Path) -> None:
        """
        Initialize an instance of the CorpusManager class.

        Args:
            path_to_raw_txt_data (pathlib.Path): Path to raw txt data
        """
        self.path_to_raw_txt_data = path_to_raw_txt_data
        self._storage = {}
        self._validate_dataset()
        self._scan_dataset()

    def _validate_dataset(self) -> None:
        """
        Validate folder with assets.
        """

        if not self.path_to_raw_txt_data.exists():
            raise FileNotFoundError("File not found")

        if not self.path_to_raw_txt_data.is_dir():
            raise NotADirectoryError("Path leads to something other than Directory")

        files_list = list(map(str, self.path_to_raw_txt_data.iterdir()))
        if len(files_list) == 0:
            raise EmptyDirectoryError("Directory is empty")

        for file in self.path_to_raw_txt_data.iterdir():
            if os.stat(file).st_size == 0:
                raise InconsistentDatasetError("One of the files is empty")

        json_count = [file for file in files_list if '.json' in file]
        json_count = sorted(json_count, key=lambda m: int(m.split("\\")[-1].split('_')[0]))
        article_count = [file for file in files_list if 'raw.txt' in file]
        article_count = sorted(article_count, key=lambda m: int(m.split("\\")[-1].split('_')[0]))

        if len(json_count) != len(article_count):
            raise InconsistentDatasetError("Number of meta files doesn't match the number of articles")

        for file_id, file_name in enumerate(article_count):
            if file_name.startswith(str(file_id)) and json_count[file_id].startswith(str(file_id)):
                raise InconsistentDatasetError('Slip ups in ID detected')

        return None

    def _scan_dataset(self) -> None:
        """
        Register each dataset entry.
        """
        files_list = list(map(str, self.path_to_raw_txt_data.iterdir()))
        files_new = []
        for file in files_list:
            if file.endswith('raw.txt'):
                files_new.append(file)
        files_new = sorted(files_new, key=lambda m: int(m.split("\\")[-1].split('_')[0]))
        iter_count = 0
        for file_id, file in enumerate(files_new):
            if str(file).endswith('raw.txt'):
                f = open(file, 'r', encoding="UTF-8")
                iter_count += 1
                article = Article(url=None, article_id=iter_count)
                article.text = f.read()
                self._storage[iter_count] = article
                f.close()

    def get_articles(self) -> dict:
        """
        Get storage params.

        Returns:
            dict: Storage params
        """
        return self._storage

class TextProcessingPipeline(PipelineProtocol):
    """
    Preprocess and morphologically annotate sentences into the CONLL-U format.
    """

    def __init__(
        self, corpus_manager: CorpusManager, analyzer: LibraryWrapper | None = None
    ) -> None:
        """
        Initialize an instance of the TextProcessingPipeline class.

        Args:
            corpus_manager (CorpusManager): CorpusManager instance
            analyzer (LibraryWrapper | None): Analyzer instance
        """
        self.corpus_manager = corpus_manager
        self.analyzer = analyzer
    def run(self) -> None:
        """
        Perform basic preprocessing and write processed text to files.
        """
        articles = self.corpus_manager.get_articles()
        for _, article in articles.items():
            article.text = article.text.lower()
            article.text = re.sub(r'[^\w\s]', '', article.text)
            article.text = re.sub(r' ', '', article.text)
            to_cleaned(article)

class UDPipeAnalyzer(LibraryWrapper):
    """
    Wrapper for udpipe library.
    """

    #: Analyzer
    _analyzer: AbstractCoNLLUAnalyzer

    def __init__(self) -> None:
        """
        Initialize an instance of the UDPipeAnalyzer class.
        """

    def _bootstrap(self) -> AbstractCoNLLUAnalyzer:
        """
        Load and set up the UDPipe model.

        Returns:
            AbstractCoNLLUAnalyzer: Analyzer instance
        """

    def analyze(self, texts: list[str]) -> list[UDPipeDocument | str]:
        """
        Process texts into CoNLL-U formatted markup.

        Args:
            texts (list[str]): Collection of texts

        Returns:
            list[UDPipeDocument | str]: List of documents
        """

    def to_conllu(self, article: Article) -> None:
        """
        Save content to ConLLU format.

        Args:
            article (Article): Article containing information to save
        """

    def from_conllu(self, article: Article) -> UDPipeDocument:
        """
        Load ConLLU content from article stored on disk.

        Args:
            article (Article): Article to load

        Returns:
            UDPipeDocument: Document ready for parsing
        """

    def get_document(self, doc: UDPipeDocument) -> UnifiedCoNLLUDocument:
        """
        Present ConLLU document's sentence tokens as a unified structure.

        Args:
            doc (UDPipeDocument): ConLLU document

        Returns:
            UnifiedCoNLLUDocument: Dictionary of token features within document sentences
        """


class StanzaAnalyzer(LibraryWrapper):
    """
    Wrapper for stanza library.
    """

    #: Analyzer
    _analyzer: AbstractCoNLLUAnalyzer

    def __init__(self) -> None:
        """
        Initialize an instance of the StanzaAnalyzer class.
        """

    def _bootstrap(self) -> AbstractCoNLLUAnalyzer:
        """
        Load and set up the Stanza model.

        Returns:
            AbstractCoNLLUAnalyzer: Analyzer instance
        """

    def analyze(self, texts: list[str]) -> list[StanzaDocument]:
        """
        Process texts into CoNLL-U formatted markup.

        Args:
            texts (list[str]): Collection of texts

        Returns:
            list[StanzaDocument]: List of documents
        """

    def to_conllu(self, article: Article) -> None:
        """
        Save content to ConLLU format.

        Args:
            article (Article): Article containing information to save
        """

    def from_conllu(self, article: Article) -> StanzaDocument:
        """
        Load ConLLU content from article stored on disk.

        Args:
            article (Article): Article to load

        Returns:
            StanzaDocument: Document ready for parsing
        """

    def get_document(self, doc: StanzaDocument) -> UnifiedCoNLLUDocument:
        """
        Present ConLLU document's sentence tokens as a unified structure.

        Args:
            doc (StanzaDocument): ConLLU document

        Returns:
            UnifiedCoNLLUDocument: Document of token features within document sentences
        """


class POSFrequencyPipeline:
    """
    Count frequencies of each POS in articles, update meta info and produce graphic report.
    """

    def __init__(self, corpus_manager: CorpusManager, analyzer: LibraryWrapper) -> None:
        """
        Initialize an instance of the POSFrequencyPipeline class.

        Args:
            corpus_manager (CorpusManager): CorpusManager instance
            analyzer (LibraryWrapper): Analyzer instance
        """

    def _count_frequencies(self, article: Article) -> dict[str, int]:
        """
        Count POS frequency in Article.

        Args:
            article (Article): Article instance

        Returns:
            dict[str, int]: POS frequencies
        """

    def run(self) -> None:
        """
        Visualize the frequencies of each part of speech.
        """


class PatternSearchPipeline(PipelineProtocol):
    """
    Search for the required syntactic pattern.
    """

    def __init__(
        self, corpus_manager: CorpusManager, analyzer: LibraryWrapper, pos: tuple[str, ...]
    ) -> None:
        """
        Initialize an instance of the PatternSearchPipeline class.

        Args:
            corpus_manager (CorpusManager): CorpusManager instance
            analyzer (LibraryWrapper): Analyzer instance
            pos (tuple[str, ...]): Root, Dependency, Child part of speech
        """

    def _make_graphs(self, doc: CoNLLUDocument) -> list[DiGraph]:
        """
        Make graphs for a document.

        Args:
            doc (CoNLLUDocument): Document for patterns searching

        Returns:
            list[DiGraph]: Graphs for the sentences in the document
        """

    def _add_children(
        self, graph: DiGraph, subgraph_to_graph: dict, node_id: int, tree_node: TreeNode
    ) -> None:
        """
        Add children to TreeNode.

        Args:
            graph (DiGraph): Sentence graph to search for a pattern
            subgraph_to_graph (dict): Matched subgraph
            node_id (int): ID of root node of the match
            tree_node (TreeNode): Root node of the match
        """

    def _find_pattern(self, doc_graphs: list) -> dict[int, list[TreeNode]]:
        """
        Search for the required pattern.

        Args:
            doc_graphs (list): A list of graphs for the document

        Returns:
            dict[int, list[TreeNode]]: A dictionary with pattern matches
        """

    def run(self) -> None:
        """
        Search for a pattern in documents and writes found information to JSON file.
        """


def main() -> None:
    """
    Entrypoint for pipeline module.
    """
    corpus_manager = CorpusManager(path_to_raw_txt_data=ASSETS_PATH)
    pipeline = TextProcessingPipeline(corpus_manager)
    pipeline.run()

if __name__ == "__main__":
    main()
