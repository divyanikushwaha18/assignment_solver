import os
import json
import re
from difflib import SequenceMatcher
from collections import Counter
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QuestionMatcher:
    """Enhanced service to match incoming questions against the repository"""
    
    def __init__(self):
        self.questions_data = []
        self._load_questions()
        self.cache = {}  # Simple cache for frequent queries
        self.cache_limit = 200  # Limit cache size to prevent memory issues
        
        # Define assignment categories and specific terms
        self.assignment_categories = {
            1: {
                "name": "Developer Tools",
                "terms": ["code -s", "vs code", "visual studio", "httpie", "prettier", "google sheets", 
                         "excel", "devtools", "wednesdays", "zip", "json", "sort", "multi-cursor", 
                         "div", "css", "unicode", "github", "sha256sum", "file", "sql", "query"]
            },
            2: {
                "name": "Deployment & Cloud",
                "terms": ["markdown", "compress", "github pages", "google colab", "image", "vercel", 
                         "github action", "docker hub", "fastapi", "llamafile", "llm", "ngrok"]
            },
            3: {
                "name": "LLM Integration",
                "terms": ["sentiment", "httpx", "openai", "token", "response_format", "json_schema", 
                         "vision", "image_url", "embedding", "cosine", "similarity", "vector", 
                         "function", "jailbreak", "prompt"]
            },
            4: {
                "name": "Web Scraping",
                "terms": ["scrape", "espn", "imdb", "rating", "wikipedia", "outline", "bbc", "weather", 
                         "nominatim", "latitude", "hacker news", "github user", "pdf", "extract", 
                         "convert", "markdown"]
            },
            5: {
                "name": "Data Cleaning",
                "terms": ["clean", "excel", "sales", "margin", "student", "marks", "unique", "apache", "log", 
                         "request", "download", "bytes", "json", "parse", "nested", "duckdb", "sql", 
                         "transcribe", "reconstruct", "image"]
            }
        }
    
    def _load_questions(self):
        """Load questions from JSON file"""
        json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'questions.json')
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                self.questions_data = json.load(f)
                logger.info(f"Loaded {len(self.questions_data)} questions from repository")
        else:
            logger.warning(f"Questions data file not found at {json_path}")
    
    def match_question(self, query):
        """
        Match a query against the questions repository with improved handling for different question types.
        
        Args:
            query (str): The question text to match
            
        Returns:
            tuple: (matched, answer) where matched is a boolean and answer is the answer text if matched
        """
        if not self.questions_data:
            logger.warning("No questions data loaded, cannot perform matching")
            return False, None
        
        # Check cache first for frequent queries
        query_cache_key = query[:100].strip().lower()  # Use first 100 chars as cache key
        if query_cache_key in self.cache:
            return self.cache[query_cache_key]
        
        # Manage cache size
        if len(self.cache) > self.cache_limit:
            # Remove oldest 20% of entries when limit is reached
            remove_count = int(self.cache_limit * 0.2)
            keys_to_remove = list(self.cache.keys())[:remove_count]
            for key in keys_to_remove:
                self.cache.pop(key, None)
        
        # Log query for debugging (truncated for brevity)
        logger.info(f"Matching query: {query[:100]}...")
        
        # Extract technical commands and critical terms
        command_pattern = re.compile(r'`([^`]+)`')
        commands = command_pattern.findall(query)
        
        # Extract first paragraph or first 300 characters for matching
        # This helps with long technical questions that have examples/code
        first_paragraph = query.split('\n\n')[0].strip()
        if len(first_paragraph) > 300:
            first_paragraph = first_paragraph[:300]
        
        # Clean and normalize the query
        cleaned_query = re.sub(r'[^\w\s]', ' ', query.lower())
        cleaned_first_para = re.sub(r'[^\w\s]', ' ', first_paragraph.lower())
        
        best_match = None
        best_score = 0.0
        
        # Extract assignment context
        assignment_context = None
        assignment_pattern = re.compile(r'assignment\s*(\d+)', re.IGNORECASE)
        assignment_match = assignment_pattern.search(query)
        if assignment_match:
            assignment_context = int(assignment_match.group(1))
            logger.info(f"Detected assignment context: Assignment {assignment_context}")
        
        # Look for fictional company/scenario context (common in assignment questions)
        company_pattern = re.compile(r'([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)\s+(?:is|Inc\.|Corp\.|LLC|Ltd\.)', re.MULTILINE)
        company_matches = company_pattern.findall(query)
        company_context = company_matches[0] if company_matches else None
        
        if company_context:
            logger.info(f"Detected company context: {company_context}")
        
        # Create a set of critical terms from commands and commonly used technical terms
        critical_terms = set()
        for cmd in commands:
            # Extract individual command parts
            cmd_parts = re.split(r'[\s@|-]', cmd)
            for part in cmd_parts:
                if part and len(part) > 2:  # Skip very short parts
                    critical_terms.add(part.lower())
        
        # File extensions and formats
        file_extensions = ["csv", "json", "txt", "md", "html", "pdf", "xlsx", "db", "sql", "py", "js", "css", "svg", "png", "jpg"]
        for ext in file_extensions:
            if f".{ext}" in query.lower():
                critical_terms.add(ext)
        
        # Extract URL and API mentions
        url_pattern = re.compile(r'https?://\S+')
        urls = url_pattern.findall(query)
        for url in urls:
            domain = url.split('/')[2] if len(url.split('/')) > 2 else ''
            if domain:
                critical_terms.add(domain.split('.')[0].lower())
        
        # Add assignment-specific terms based on detected or implicit assignment context
        if assignment_context and assignment_context in self.assignment_categories:
            for term in self.assignment_categories[assignment_context]["terms"]:
                if term in cleaned_query:
                    critical_terms.add(term)
        else:
            # If no explicit assignment context, check for terms from all assignments
            for assignment, category in self.assignment_categories.items():
                for term in category["terms"]:
                    if term in cleaned_query:
                        critical_terms.add(term)
        
        # Add specific terms for each assignment type
        # Assignment 1: Developer Tools
        dev_tools_terms = [
            "code -s", "vs code", "httpie", "https", "prettier", "sheets", "formula", "excel", 
            "devtools", "hidden input", "wednesdays", "extract.csv", "json", "sort", "jsonhash", 
            "foo class", "div", "data-value", "unicode", "encoding", "github", "raw", "replace", 
            "ls", "grep", "sha256sum", "diff", "sql", "ticket", "gold"
        ]
        
        # Assignment 2: Deployment & Cloud
        deployment_terms = [
            "markdown", "compress", "github pages", "google colab", "brightness", "vercel", 
            "api", "github action", "docker hub", "tag", "fastapi", "llamafile", "ngrok"
        ]
        
        # Assignment 3: LLM Integration
        llm_terms = [
            "sentiment", "httpx", "openai", "token", "gpt-4o-mini", "structured outputs", 
            "vision", "image_url", "embeddings", "cosine similarity", "vector", "numpy", 
            "function calling", "yes"
        ]
        
        # Assignment 4: Web Scraping
        web_scraping_terms = [
            "scrape", "espn", "ducks", "imdb", "rating", "wikipedia", "outline", "bbc", "weather", 
            "nominatim", "latitude", "bounding box", "hacker news", "posts", "github user", 
            "followers", "github action", "pdf", "extract", "convert", "markdown"
        ]
        
        # Assignment 5: Data Cleaning
        data_cleaning_terms = [
            "clean", "excel", "sales", "margin", "student", "unique", "apache", "log", 
            "request", "download", "bytes", "json", "parse", "nested", "duckdb", "sql", 
            "transcript", "reconstruct", "image", "pieces"
        ]
        
        # Add all relevant terms to critical terms
        all_domain_terms = dev_tools_terms + deployment_terms + llm_terms + web_scraping_terms + data_cleaning_terms
        for term in all_domain_terms:
            # Use looser matching - check if the term words appear in the query
            term_words = term.split()
            if len(term_words) > 1:
                # For multi-word terms, check if all words appear close to each other
                term_word_pattern = r'\b' + r'\b.*?\b'.join(term_words) + r'\b'
                if re.search(term_word_pattern, cleaned_query, re.IGNORECASE):
                    critical_terms.add(term.lower())
            else:
                # For single-word terms, use direct matching
                if term.lower() in cleaned_query:
                    critical_terms.add(term.lower())
        
        # Add any potential command outputs mentioned 
        hex_pattern = re.compile(r'[0-9a-f]{10,}', re.IGNORECASE)
        hex_matches = hex_pattern.findall(query)
        if hex_matches:
            critical_terms.add("sha256sum")
            critical_terms.add("hash")
            critical_terms.add("checksum")
        
        # Detect specialized contexts
        contexts = {
            "developer_tools": any(term in cleaned_query for term in ["code", "vs code", "command", "terminal", "bash", "shell"]),
            "data_cleaning": any(term in cleaned_query for term in ["clean", "standardize", "normalize", "extract"]),
            "web_scraping": any(term in cleaned_query for term in ["scrape", "extract", "web", "html", "url"]),
            "llm_integration": any(term in cleaned_query for term in ["openai", "gpt", "llm", "embedding", "sentiment"]),
            "log_analysis": any(term in cleaned_query for term in ["log", "apache", "request", "get", "ip"]),
            "json_processing": any(term in cleaned_query for term in ["json", "parse", "nested", "key"]),
            "image_processing": any(term in cleaned_query for term in ["image", "reconstruct", "scrambled"]),
            "sql_query": any(term in cleaned_query for term in ["sql", "duckdb", "query"]),
            "cloud_deployment": any(term in cleaned_query for term in ["deploy", "vercel", "github pages", "docker"])
        }
        
        # Extract key technical terms for embedding questions
        embedding_terms = set()
        for term in ["cosine", "similarity", "embedding", "vector", "numpy", "calculate", 
                   "function", "python", "most_similar", "matrix", "array", "normalize",
                   "algorithm", "code", "implementation", "dictionary", "pairs", "highest"]:
            if term in cleaned_query:
                embedding_terms.add(term)
                critical_terms.add(term)
        
        # Try direct keyword matching
        query_keywords = set(cleaned_query.split())
        first_para_keywords = set(cleaned_first_para.split())
        
        # Measure keyword frequency to identify important terms
        keyword_freq = Counter(cleaned_query.split())
        important_keywords = {word for word, count in keyword_freq.items() if count > 1 and len(word) > 3}
        
        # For logging
        logger.debug(f"Critical terms: {critical_terms}")
        
        for question_data in self.questions_data:
            # Check assignment context if available
            if assignment_context and question_data.get('assignment_number') != assignment_context:
                continue
            
            # Get question keywords and text
            question_keywords = set(question_data.get('keywords', []))
            question_text = question_data['question_text'].lower()
            question_text_keywords = set(re.sub(r'[^\w\s]', ' ', question_text).split())
            all_question_keywords = question_keywords.union(question_text_keywords)
            
            # Check for critical term matches
            critical_term_matches = 0
            matched_critical_terms = []
            for term in critical_terms:
                if term in question_text or term in question_keywords:
                    critical_term_matches += 1
                    matched_critical_terms.append(term)
            
            # Check for embedding specific terms
            embedding_term_matches = 0
            for term in embedding_terms:
                if term in question_text or term in question_keywords:
                    embedding_term_matches += 1
            
            # Regular keyword overlap
            common_keywords = query_keywords.intersection(all_question_keywords)
            
            # Give higher weight to important keywords
            important_keyword_matches = important_keywords.intersection(all_question_keywords)
            important_keyword_bonus = len(important_keyword_matches) * 0.5
            
            # Also check overlap with first paragraph (for long questions)
            first_para_overlap = first_para_keywords.intersection(all_question_keywords)
            
            # For command-oriented questions, prioritize command pattern matches
            command_oriented_score = 0
            for cmd in commands:
                if cmd.lower() in question_text:
                    command_oriented_score += 0.2
            
            # Handle specialized contexts
            context_score = 0
            for context_name, is_active in contexts.items():
                if is_active:
                    # Check if question keywords indicate this context
                    context_terms = [term for term in self.assignment_categories.get(question_data.get('assignment_number', 0), {}).get("terms", []) 
                                   if term in ' '.join(question_keywords)]
                    if context_terms:
                        context_score += 0.3
                        logger.debug(f"Context match: {context_name} - {context_terms}")
            
            # Combined scoring factors
            effective_keyword_count = (
                len(common_keywords) + 
                len(first_para_overlap) + 
                critical_term_matches * 2 +
                important_keyword_bonus
            )
            
            # Check for specific question patterns
            is_embedding_question = embedding_term_matches >= 2
            is_command_question = len(commands) > 0 and critical_term_matches >= 1
            is_specialized_context = context_score > 0
            
            # Process questions that have enough matching elements
            # Lower thresholds for specialized contexts
            min_keyword_threshold = 2 if is_specialized_context else 3
            min_critical_threshold = 1 if is_specialized_context else 2
            
            if (effective_keyword_count > min_keyword_threshold or 
                critical_term_matches >= min_critical_threshold or 
                is_embedding_question or is_command_question or
                is_specialized_context):
                # Calculate similarity ratios
                para_similarity = SequenceMatcher(None, cleaned_first_para, question_text).ratio()
                query_similarity = SequenceMatcher(None, cleaned_query[:300], question_text).ratio()
                
                # Weighted score calculation
                keyword_ratio = effective_keyword_count / max(1, len(query_keywords))
                critical_ratio = critical_term_matches / max(1, len(critical_terms)) if critical_terms else 0
                
                # Determine scoring weights based on question type
                if is_embedding_question:
                    # For embedding questions, focus more on technical term matching
                    score = (keyword_ratio * 0.25) + (critical_ratio * 0.45) + (para_similarity * 0.15) + (query_similarity * 0.15)
                    threshold = 0.35
                elif is_command_question:
                    # For command questions, focus on command matching
                    score = (keyword_ratio * 0.3) + (critical_ratio * 0.4) + (para_similarity * 0.1) + (query_similarity * 0.1) + command_oriented_score
                    threshold = 0.35
                elif is_specialized_context:
                    # For specialized contexts, focus on context and critical term matching
                    score = (keyword_ratio * 0.4) + (critical_ratio * 0.3) + (para_similarity * 0.1) + (query_similarity * 0.1) + context_score
                    threshold = 0.33  # Lower threshold for specialized contexts
                else:
                    # For general questions
                    score = (keyword_ratio * 0.4) + (critical_ratio * 0.2) + (para_similarity * 0.2) + (query_similarity * 0.2)
                    threshold = 0.4
                
                # Check for assignment-specific boost
                if assignment_context:
                    if question_data.get('assignment_number') == assignment_context:
                        score *= 1.2  # 20% boost for matching assignment
                else:
                    # Try to detect assignment context from the query
                    for assignment, category in self.assignment_categories.items():
                        category_terms = set(category["terms"])
                        if len(category_terms.intersection(critical_terms)) >= 2:
                            if question_data.get('assignment_number') == assignment:
                                score *= 1.15  # 15% boost for implicit assignment match
                
                # Lower threshold for complex technical questions
                if contexts["image_processing"] or "transcribe" in cleaned_query:
                    threshold *= 0.9  # 10% reduction in threshold
                
                # Additional check for company/scenario similarity 
                if company_context and company_context.lower() in question_text:
                    score += 0.05  # Small boost for company context match
                
                if score > best_score and score > threshold:
                    best_score = score
                    best_match = question_data
                    logger.debug(f"New best match: Q{question_data.get('assignment_number')}.{question_data.get('question_number')} with score {score:.3f}")
        
        # Store result in cache
        result = (False, None) if best_match is None else (True, best_match['answer_text'])
        self.cache[query_cache_key] = result
        
        if best_match:
            logger.info(f"Matched query to A{best_match.get('assignment_number', 0)}.Q{best_match.get('question_number', 0)} with score {best_score:.3f}")
        else:
            logger.info(f"No match found for query. Best score: {best_score:.3f}")
        
        return result
    
    def get_matching_questions(self, query, limit=5):
        """
        Find multiple matching questions for a query, ranked by relevance.
        
        Args:
            query (str): The question text to match
            limit (int): Maximum number of matches to return
            
        Returns:
            list: List of (question_text, score) tuples for top matches
        """
        if not self.questions_data:
            return []
        
        # Extract commands
        command_pattern = re.compile(r'`([^`]+)`')
        commands = command_pattern.findall(query)
        
        # Extract first paragraph for matching
        first_paragraph = query.split('\n\n')[0].strip()
        if len(first_paragraph) > 300:
            first_paragraph = first_paragraph[:300]
        
        # Clean and normalize the query
        cleaned_query = re.sub(r'[^\w\s]', ' ', query.lower())
        cleaned_first_para = re.sub(r'[^\w\s]', ' ', first_paragraph.lower())
        
        # Create a set of critical terms for all assignments
        critical_terms = set()
        
        # Add command parts
        for cmd in commands:
            cmd_parts = re.split(r'[\s@|-]', cmd)
            for part in cmd_parts:
                if part and len(part) > 2:
                    critical_terms.add(part.lower())
        
        # Add terms from all assignment categories
        for assignment, category in self.assignment_categories.items():
            for term in category["terms"]:
                if term in cleaned_query:
                    critical_terms.add(term)
        
        # Add tech terms for embedding questions
        for term in ["cosine", "similarity", "embedding", "vector", "numpy", "function"]:
            if term in cleaned_query:
                critical_terms.add(term)
        
        # Extract assignment context
        assignment_context = None
        assignment_pattern = re.compile(r'assignment\s*(\d+)', re.IGNORECASE)
        assignment_match = assignment_pattern.search(query)
        if assignment_match:
            assignment_context = int(assignment_match.group(1))
        
        # Look for company/scenario context
        company_pattern = re.compile(r'([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)\s+(?:is|Inc\.|Corp\.|LLC|Ltd\.)', re.MULTILINE)
        company_matches = company_pattern.findall(query)
        company_context = company_matches[0] if company_matches else None
        
        # Detect specialized contexts
        contexts = {
            "developer_tools": any(term in cleaned_query for term in ["code", "vs code", "command", "terminal", "bash", "shell"]),
            "data_cleaning": any(term in cleaned_query for term in ["clean", "standardize", "normalize", "extract"]),
            "web_scraping": any(term in cleaned_query for term in ["scrape", "extract", "web", "html", "url"]),
            "llm_integration": any(term in cleaned_query for term in ["openai", "gpt", "llm", "embedding", "sentiment"]),
            "log_analysis": any(term in cleaned_query for term in ["log", "apache", "request", "get", "ip"]),
            "json_processing": any(term in cleaned_query for term in ["json", "parse", "nested", "key"]),
            "image_processing": any(term in cleaned_query for term in ["image", "reconstruct", "scrambled"]),
            "sql_query": any(term in cleaned_query for term in ["sql", "duckdb", "query"]),
            "cloud_deployment": any(term in cleaned_query for term in ["deploy", "vercel", "github pages", "docker"])
        }
        
        # Try direct keyword matching
        query_keywords = set(cleaned_query.split())
        first_para_keywords = set(cleaned_first_para.split())
        
        matches = []
        
        for question_data in self.questions_data:
            # Check assignment context if available
            if assignment_context and question_data.get('assignment_number') != assignment_context:
                continue
                
            question_keywords = set(question_data.get('keywords', []))
            question_text = question_data['question_text'].lower()
            question_text_keywords = set(re.sub(r'[^\w\s]', ' ', question_text).split())
            all_question_keywords = question_keywords.union(question_text_keywords)
            
            # Check for critical term matches
            critical_term_matches = 0
            for term in critical_terms:
                if term in question_text or term in question_keywords:
                    critical_term_matches += 1
            
            # Regular keyword overlap
            common_keywords = query_keywords.intersection(all_question_keywords)
            first_para_overlap = first_para_keywords.intersection(all_question_keywords)
            
            # Command pattern matching
            command_oriented_score = 0
            for cmd in commands:
                if cmd.lower() in question_text:
                    command_oriented_score += 0.2
            
            # Handle specialized contexts
            context_score = 0
            for context_name, is_active in contexts.items():
                if is_active:
                    # Check if question keywords indicate this context
                    context_terms = [term for term in self.assignment_categories.get(question_data.get('assignment_number', 0), {}).get("terms", []) 
                                   if term in ' '.join(question_keywords)]
                    if context_terms:
                        context_score += 0.3
            
            # Combined metrics
            effective_keyword_count = len(common_keywords) + len(first_para_overlap) + critical_term_matches * 2
            
            # Lower thresholds for specialized contexts
            min_keyword_threshold = 1 if any(contexts.values()) else 2
            
            if effective_keyword_count > min_keyword_threshold or critical_term_matches >= 1 or context_score > 0:
                # Calculate similarity ratios
                para_similarity = SequenceMatcher(None, cleaned_first_para, question_text).ratio()
                query_similarity = SequenceMatcher(None, cleaned_query[:300], question_text).ratio()
                
                # Score calculation
                keyword_ratio = effective_keyword_count / max(1, len(query_keywords))
                critical_ratio = critical_term_matches / max(1, len(critical_terms)) if critical_terms else 0
                
                # Determine scoring weights based on context
                if contexts["llm_integration"] and "embedding" in question_text:
                    # For embedding questions
                    score = (keyword_ratio * 0.25) + (critical_ratio * 0.45) + (para_similarity * 0.15) + (query_similarity * 0.15)
                elif contexts["developer_tools"] and len(commands) > 0:
                    # For command questions
                    score = (keyword_ratio * 0.3) + (critical_ratio * 0.4) + (para_similarity * 0.1) + (query_similarity * 0.1) + command_oriented_score
                elif any(contexts.values()):
                    # For specialized contexts
                    score = (keyword_ratio * 0.4) + (critical_ratio * 0.3) + (para_similarity * 0.1) + (query_similarity * 0.1) + context_score
                else:
                    # For general questions
                    score = (keyword_ratio * 0.4) + (critical_ratio * 0.2) + (para_similarity * 0.2) + (query_similarity * 0.2)
                
                # Check for assignment-specific boost
                if assignment_context:
                    if question_data.get('assignment_number') == assignment_context:
                        score *= 1.2  # 20% boost for matching assignment
                
                # Additional check for company/scenario similarity 
                if company_context and company_context.lower() in question_text:
                    score += 0.05  # Small boost for company context match
                
                matches.append((
                    question_data['question_text'], 
                    score, 
                    question_data.get('answer_text', ''), 
                    question_data.get('assignment_number'), 
                    question_data.get('question_number')
                ))
        
        # Sort by score (descending) and return top matches
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:limit]
    
    def debug_match(self, query):
        """
        Debugging function to see matching scores and details.
        
        Args:
            query (str): The question text to match
            
        Returns:
            dict: Debug information about the matching process
        """
        if not self.questions_data:
            return {"error": "No questions data loaded"}
        
        # Extract commands
        command_pattern = re.compile(r'`([^`]+)`')
        commands = command_pattern.findall(query)
        
        # Extract first paragraph
        first_paragraph = query.split('\n\n')[0].strip()
        if len(first_paragraph) > 300:
            first_paragraph = first_paragraph[:300]
        
        # Clean and normalize
        cleaned_query = re.sub(r'[^\w\s]', ' ', query.lower())
        cleaned_first_para = re.sub(r'[^\w\s]', ' ', first_paragraph.lower())
        
        # Identify critical terms from all assignments
        critical_terms = set()
        
        # Add command parts
        for cmd in commands:
            cmd_parts = re.split(r'[\s@|-]', cmd)
            for part in cmd_parts:
                if part and len(part) > 2:
                    critical_terms.add(part.lower())
        
        # Add all assignment category terms
        for assignment, category in self.assignment_categories.items():
            for term in category["terms"]:
                if term in cleaned_query:
                    critical_terms.add(term)
        
        # Add embedding terms
        embedding_terms = set()
        for term in ["cosine", "similarity", "embedding", "vector", "numpy", "calculate"]:
            if term in cleaned_query:
                embedding_terms.add(term)
                critical_terms.add(term)
        
        # Check for hex patterns suggesting hash outputs
        hex_pattern = re.compile(r'[0-9a-f]{10,}', re.IGNORECASE)
        hex_matches = hex_pattern.findall(query)
        if hex_matches:
            critical_terms.add("sha256sum")
            critical_terms.add("hash")
        
        # Extract assignment context
        assignment_context = None
        assignment_pattern = re.compile(r'assignment\s*(\d+)', re.IGNORECASE)
        assignment_match = assignment_pattern.search(query)
        if assignment_match:
            assignment_context = int(assignment_match.group(1))
        
        # Detect specialized contexts
        contexts = {
            "developer_tools": any(term in cleaned_query for term in ["code", "vs code", "command", "terminal", "bash", "shell"]),
            "data_cleaning": any(term in cleaned_query for term in ["clean", "standardize", "normalize", "extract"]),
            "web_scraping": any(term in cleaned_query for term in ["scrape", "extract", "web", "html", "url"]),
            "llm_integration": any(term in cleaned_query for term in ["openai", "gpt", "llm", "embedding", "sentiment"]),
            "log_analysis": any(term in cleaned_query for term in ["log", "apache", "request", "get", "ip"]),
            "json_processing": any(term in cleaned_query for term in ["json", "parse", "nested", "key"]),
            "image_processing": any(term in cleaned_query for term in ["image", "reconstruct", "scrambled"]),
            "sql_query": any(term in cleaned_query for term in ["sql", "duckdb", "query"]),
            "cloud_deployment": any(term in cleaned_query for term in ["deploy", "vercel", "github pages", "docker"])
        }
        
        # Look for company/scenario context
        company_pattern = re.compile(r'([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)\s+(?:is|Inc\.|Corp\.|LLC|Ltd\.)', re.MULTILINE)
        company_matches = company_pattern.findall(query)
        company_context = company_matches[0] if company_matches else None
        
        # Get keywords
        query_keywords = set(cleaned_query.split())
        first_para_keywords = set(cleaned_first_para.split())
        
        debug_info = {
            "query_first_para": first_paragraph,
            "commands_detected": commands,
            "critical_terms": list(critical_terms),
            "embedding_terms": list(embedding_terms),
            "hex_patterns": hex_matches,
            "assignment_context": assignment_context,
            "company_context": company_context,
            "contexts": {k: v for k, v in contexts.items() if v},
            "top_matches": []
        }
        
        for question_data in self.questions_data:
            # Check assignment context if available
            if assignment_context and question_data.get('assignment_number') != assignment_context:
                continue
                
            question_keywords = set(question_data.get('keywords', []))
            question_text = question_data['question_text'].lower()
            question_text_keywords = set(re.sub(r'[^\w\s]', ' ', question_text).split())
            all_question_keywords = question_keywords.union(question_text_keywords)
            
            # Critical term matches
            critical_terms_found = []
            for term in critical_terms:
                if term in question_text or term in question_keywords:
                    critical_terms_found.append(term)
            
            # Command matches
            command_matches = []
            for cmd in commands:
                if cmd.lower() in question_text:
                    command_matches.append(cmd)
            
            # Keyword overlap
            common_keywords = query_keywords.intersection(all_question_keywords)
            first_para_overlap = first_para_keywords.intersection(all_question_keywords)
            
            # Handle specialized contexts
            context_score = 0
            active_contexts = []
            for context_name, is_active in contexts.items():
                if is_active:
                    # Check if question keywords indicate this context
                    context_terms = [term for term in self.assignment_categories.get(question_data.get('assignment_number', 0), {}).get("terms", []) 
                                   if term in ' '.join(question_keywords)]
                    if context_terms:
                        context_score += 0.3
                        active_contexts.append(context_name)
            
            # Only include questions with some matching potential
            if len(critical_terms_found) > 0 or len(common_keywords) > 1 or context_score > 0:
                # Calculate similarity
                para_similarity = SequenceMatcher(None, cleaned_first_para, question_text).ratio()
                query_similarity = SequenceMatcher(None, cleaned_query[:300], question_text).ratio()
                
                # Basic metrics
                keyword_ratio = len(common_keywords) / max(1, len(query_keywords))
                critical_ratio = len(critical_terms_found) / max(1, len(critical_terms)) if critical_terms else 0
                command_score = 0.2 * len(command_matches)
                
                # Effective keyword count
                effective_keyword_count = len(common_keywords) + len(first_para_overlap) + len(critical_terms_found) * 2
                
                # Determine question type
                is_embedding = len(embedding_terms.intersection(set(critical_terms_found))) >= 2
                is_command = len(commands) > 0 and len(critical_terms_found) >= 1
                is_specialized = context_score > 0
                
                # Score calculation based on question type
                if is_embedding:
                    score = (keyword_ratio * 0.25) + (critical_ratio * 0.45) + (para_similarity * 0.15) + (query_similarity * 0.15)
                    threshold = 0.35
                    question_type = "embedding"
                elif is_command:
                    score = (keyword_ratio * 0.3) + (critical_ratio * 0.4) + (para_similarity * 0.1) + (query_similarity * 0.1) + command_score
                    threshold = 0.35
                    question_type = "command"
                elif is_specialized:
                    score = (keyword_ratio * 0.4) + (critical_ratio * 0.3) + (para_similarity * 0.1) + (query_similarity * 0.1) + context_score
                    threshold = 0.33  # Lower threshold for specialized contexts
                    question_type = "specialized"
                else:
                    score = (keyword_ratio * 0.4) + (critical_ratio * 0.2) + (para_similarity * 0.2) + (query_similarity * 0.2)
                    threshold = 0.4
                    question_type = "general"
                
                # Check for assignment-specific boost
                assignment_boost = 1.0
                if assignment_context:
                    if question_data.get('assignment_number') == assignment_context:
                        assignment_boost = 1.2
                        score *= assignment_boost
                
                # Additional check for company/scenario similarity 
                company_boost = 1.0
                if company_context and company_context.lower() in question_text:
                    company_boost = 1.05
                    score *= company_boost
                
                # Lower threshold for complex technical questions
                threshold_adjustment = 1.0
                if contexts["image_processing"] or "transcribe" in cleaned_query:
                    threshold_adjustment = 0.9  # 10% reduction in threshold
                    threshold *= threshold_adjustment
                
                debug_info["top_matches"].append({
                    "question": question_data['question_text'],
                    "assignment": question_data.get("assignment_number", "unknown"),
                    "question_number": question_data.get("question_number", "unknown"),
                    "score": score,
                    "threshold": threshold,
                    "question_type": question_type,
                    "would_match": score > threshold,
                    "common_keywords": list(common_keywords)[:10],  # Limit to 10 for readability
                    "critical_terms_matched": critical_terms_found,
                    "command_matches": command_matches,
                    "first_para_similarity": para_similarity,
                    "full_query_similarity": query_similarity,
                    "context_score": context_score,
                    "active_contexts": active_contexts,
                    "assignment_boost": assignment_boost,
                    "company_boost": company_boost,
                    "threshold_adjustment": threshold_adjustment
                })
        
        # Sort matches by score
        debug_info["top_matches"].sort(key=lambda x: x["score"], reverse=True)
        return debug_info