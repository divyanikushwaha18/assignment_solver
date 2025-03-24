class BaseProcessor:
    """
    Base class for all processors.
    """
    def process(self, question, file=None):
        """
        Process the question and file and return an answer.
        
        Args:
            question (str): The question text
            file: The uploaded file
            
        Returns:
            dict: Response with answer key
        """
        raise NotImplementedError("Subclasses must implement this method")