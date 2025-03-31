import re
import os
import json

def extract_keywords(text):
    """Extract important keywords from question text"""
    # Remove common words and punctuation
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    words = text.split()
    
    # Remove common stop words
    stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'if', 'on', 'in', 'with', 'to', 'from', 'is', 'are', 'what', 'how', 'when', 'where', 'why', 'who'}
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Return unique keywords
    return list(set(keywords))

def process_files(files):
    questions_data = []
    
    for file_path in files:
        if not os.path.exists(file_path):
            print(f'File not found: {file_path}')
            continue
            
        print(f'Processing file: {file_path}')
        
        # Extract assignment number from filename
        match = re.search(r'assignment(\d+)', os.path.basename(file_path), re.IGNORECASE)
        if match:
            assignment_number = int(match.group(1))
        else:
            assignment_number = 0
            
        # Read the markdown file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Split content by heading level 2 (## section)
        sections = re.split(r'(?m)^## ', content)
        
        # Process each section
        question_number = 0
        for section in sections:
            if not section.strip():
                continue
                
            # Process each section for questions and answers
            question_lines = []
            answer_lines = []
            in_answer = False
            lines = section.split('\n')
            
            if lines and lines[0].strip():
                section_title = lines[0].strip()
                question_number += 1
                print(f'  Processing section: {section_title}')
            
            for line in lines[1:]:
                if line.startswith('**Question:**'):
                    in_answer = False
                    question_text = line.replace('**Question:**', '').strip()
                    question_lines.append(question_text)
                elif line.startswith('**Answer:**'):
                    in_answer = True
                elif in_answer:
                    answer_lines.append(line)
                else:
                    question_lines.append(line)
            
            if question_lines and answer_lines:
                question_text = '\n'.join(question_lines).strip()
                answer_text = '\n'.join(answer_lines).strip()
                
                # Generate keywords from question text
                keywords = extract_keywords(question_text)
                
                # Add to questions data
                questions_data.append({
                    'assignment_number': assignment_number,
                    'question_number': question_number,
                    'question_text': question_text,
                    'answer_text': answer_text,
                    'keywords': keywords
                })
                
                print(f'    Added question {question_number}')
    
    # Create output directory if it doesn't exist
    os.makedirs('solver/data', exist_ok=True)
    
    # Write to JSON file
    output_file = 'solver/data/questions.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions_data, f, indent=2)
        
    print(f'Exported {len(questions_data)} questions to {output_file}')

if __name__ == "__main__":
    # List your markdown files here
    files = [
        "assignment1-md.md",
        "assignment2-md.md",
        "assignment3-md.md", 
        "assignment4-md-complete.md",
        "assignment5-md.md"
    ]
    process_files(files)