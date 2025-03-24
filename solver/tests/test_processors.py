import pytest
from ..services.processors.base_processor import BaseProcessor
from ..services.processors.file_processor import FileProcessor
from pathlib import Path

TEST_DATA_DIR = Path(__file__).parent.parent.parent / 'test_data'

def test_file_processor():
    processor = FileProcessor()
    test_file = TEST_DATA_DIR / 'sample.csv'
    assert processor.validate(test_file) is None
    result = processor.process(test_file)
    assert result is not None
