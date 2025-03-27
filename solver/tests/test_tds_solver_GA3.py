"""
Test suite for TDS Solver API using Assignment 3 (LLM) files.
This module contains test cases for all assignments based on the requirements.
"""

import os
import json
import requests
import pandas as pd
from pathlib import Path
import base64

# API endpoint
API_URL = "http://localhost:8000/api/"


def call_api(question, file_path=None, file_name=None):
    """
    Call the TDS Solver API with a question and optional file.
    """
    if file_path:
        # Convert to proper path for the current OS
        file_path = Path(file_path)
        
        # Check if file exists
        if not file_path.exists():
            print(f"Error: File not found: {file_path}")
            # Try to look for the file in the current directory or test_data
            alternative_paths = [
                Path("test_data") / file_path.name,
                Path("test_data") / file_path.parts[-2] / file_path.name,
                Path.cwd() / file_path.name
            ]
            
            for alt_path in alternative_paths:
                if alt_path.exists():
                    print(f"Found file at alternative location: {alt_path}")
                    file_path = alt_path
                    break
            else:
                return {"error": f"File not found: {file_path}"}
        
        with open(file_path, 'rb') as file_data:
            files = {
                'question': (None, question),
                'file': (file_name or file_path.name, file_data)
            }
            response = requests.post(API_URL, files=files)
    else:
        files = {
            'question': (None, question)
        }
        response = requests.post(API_URL, files=files)
    
    return response.json()


def test_llm_sentiment_analysis():
    """
    Test Q1: LLM Sentiment Analysis
    """
    print("\n===== Testing LLM Sentiment Analysis (Q1) =====")
    
    question = """DataSentinel Inc. is a tech company specializing in building advanced natural language processing (NLP) solutions. 
    Write a Python program that uses httpx to send a POST request to OpenAI's API to analyze the sentiment of this (meaningless) text:
    
    BnE u sUflhb dhM q JNB
    C J3U5p  fg   W ZAeE s  O
    
    Make sure you pass an Authorization header with dummy API key.
    Use gpt-4o-mini as the model.
    The first message must be a system message asking the LLM to analyze the sentiment of the text. Make sure you mention GOOD, BAD, or NEUTRAL as the categories.
    The second message must be exactly the text contained above."""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_llm_token_cost():
    """
    Test Q2: LLM Token Cost
    """
    print("\n===== Testing LLM Token Cost (Q2) =====")
    
    question = """LexiSolve Inc. is a startup that delivers a conversational AI platform to enterprise clients.
    When you make a request to OpenAI's GPT-4o-Mini with just this user message:
    
    List only the valid English words from these: k4, JKdAjoqeqD, D, Uw, skgzVr, eDeLmA7O, P, 14eq8yt, u, AAtvzkcj, w, raLsjV3, zlYUcetWXn, P8zPj1YvdS, Ukpt, KflXL, atct57oR, TbM4ryAgy, CnKx, lWArlA2, 7, 7JDMIc, fPOS, w80CJAwLg, D9ge, Q6J3Ph8, rKVA, LT6Ljka, 1jQ, nzgXDC, H0lDA, n0bAqmO39, C, PzIJO, K1J, EI, VSTW9V, ubF, bKdUYPDbJ, Qet5McJWA, VEUaMAYRUI, gT7IH, 6AsvDC, b6ZT0gSdGm, HnC, 0yyc3HQ, Pyj5xXtlRw, R, gYJsEJZ, 2JNQE, se, 3, m, RST, 1z, N
    
    ... how many input tokens does it use up?"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_generate_addresses_with_llm():
    """
    Test Q3: Generate addresses with LLMs
    """
    print("\n===== Testing Generate addresses with LLMs (Q3) =====")
    
    question = """RapidRoute Solutions is a logistics and delivery company that relies on accurate and standardized address data.
    You need to write the body of the request to an OpenAI chat completion call that:
    
    - Uses model gpt-4o-mini
    - Has a system message: Respond in JSON
    - Has a user message: Generate 10 random addresses in the US
    - Uses structured outputs to respond with an object addresses which is an array of objects with required fields: street (string) city (string) state (string)
    - Sets additionalProperties to false to prevent additional properties.
    
    What is the JSON body we should send to https://api.openai.com/v1/chat/completions for this?"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_llm_vision():
    """
    Test Q4: LLM Vision
    """
    print("\n===== Testing LLM Vision (Q4) =====")
    
    file_path = "test_data/images/invoice_sample.png"
    
    question = """Acme Global Solutions manages hundreds of invoices from vendors every month.
    Write just the JSON body (not the URL, nor headers) for the POST request that sends these two pieces of content (text and image URL) to the OpenAI API endpoint.
    
    Use gpt-4o-mini as the model.
    Send a single user message to the model that has a text and an image_url content (in that order).
    The text content should be Extract text from this image.
    Send the image_url as a base64 URL of the image."""
    
    # Call API
    result = call_api(question, file_path)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_llm_embeddings():
    """
    Test Q5: LLM Embeddings
    """
    print("\n===== Testing LLM Embeddings (Q5) =====")
    
    question = """SecurePay, a leading fintech startup, has implemented an innovative feature to detect and prevent fraudulent activities in real time.
    Your task is to write the JSON body for a POST request that will be sent to the OpenAI API endpoint to obtain the text embedding for the 2 given personalized transaction verification messages below. This will be sent to the endpoint https://api.openai.com/v1/embeddings.
    
    Message 1: Dear user, please verify your transaction code 82250 sent to 23f3000756@ds.study.iitm.ac.in
    Message 2: Dear user, please verify your transaction code 3017 sent to 23f3000756@ds.study.iitm.ac.in"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_embedding_similarity():
    """
    Test Q6: Embedding Similarity
    """
    print("\n===== Testing Embedding Similarity (Q6) =====")
    
    question = """ShopSmart is an online retail platform that places a high value on customer feedback.
    Your task is to write a Python function most_similar(embeddings) that will calculate the cosine similarity between each pair of these embeddings and return the pair that has the highest similarity. The result should be a tuple of the two phrases that are most similar.
    
    Here are the embeddings:
    embeddings = {"The product description matched the item.":[-0.1778346747159958,0.015024187043309212,-0.48206639289855957,-0.025718823075294495,-0.016542760655283928,-0.14746320247650146,0.08109830319881439,0.14048422873020172,-0.06655876338481903,-0.014773784205317497,-0.022116249427199364,-0.09764105826616287,0.0843939259648323,-0.21104943752288818,0.05166381597518921,0.24917533993721008,-0.04652651399374008,-0.03644577041268349,-0.3680764436721802,0.14306902885437012,0.19114643335342407,0.09570245444774628,0.12562158703804016,0.04345705732703209,-0.05486251413822174,-0.1628427952528,-0.04840049892663956,-0.08885271847248077,0.20407046377658844,0.14849711954593658,0.017899783328175545,-0.17020949721336365,0.13428069651126862,-0.2234565168619156,0.00254037999548018,0.044975630939006805,0.14862637221813202,-0.06594487279653549,0.15728546679019928,0.006142953876405954,-0.207172229886055,-0.020533055067062378,-0.05463634431362152,0.09492701292037964,-0.03237469866871834,0.06752806901931763,-0.08736645430326462,0.08297228813171387,-0.036898110061883926,-0.045621830970048904],"There was a delay in delivery.":[0.14162038266658783,0.133348748087883,-0.04399004951119423,-0.10571397840976715,-0.12250789999961853,0.039634909480810165,0.010010556317865849,0.028512069955468178,-0.011859141290187836,-0.11755745112895966,-0.011624150909483433,-0.05646016448736191,-0.07576064020395279,-0.26845210790634155,-0.060000672936439514,-0.07820453494787216,0.04865850880742073,-0.1497666984796524,-0.28549668192863464,0.24902629852294922,0.0857868641614914,0.053608957678079605,0.24727170169353485,0.0352797694504261,-0.16643528640270233,-0.060595981776714325,0.1174321249127388,-0.17596019804477692,0.04847051948308945,0.14939071238040924,0.12282121926546097,-0.10019955784082413,0.23448826372623444,-0.22408606112003326,-0.16217415034770966,0.1520226001739502,-0.0021325305569916964,0.19927117228507996,0.15578243136405945,0.1492653787136078,-0.26845210790634155,-0.1048993468284607,-0.11906138807535172,-0.012994923628866673,-0.07444469630718231,0.22797122597694397,-0.05166637524962425,-0.07469535619020462,-0.009728568606078625,0.23611752688884735],"Shipping costs were too high.":[-0.02132924273610115,-0.05078135058283806,0.24659079313278198,0.03407837450504303,-0.031469374895095825,0.04534817487001419,-0.14255358278751373,0.028483819216489792,-0.0895128846168518,0.05390138924121857,-0.0863390564918518,0.025431020185351372,-0.10597378760576248,0.02617068588733673,0.04362677410244942,-0.020603027194738388,0.1553564965724945,-0.12254228442907333,-0.3750503957271576,0.08009897172451019,0.13728179037570953,0.17526021599769592,-0.08456385880708694,-0.21130205690860748,-0.06810295581817627,0.008573387749493122,0.2928534746170044,-0.27736085653305054,0.12576991319656372,-0.23002229630947113,0.1522364616394043,-0.13523761928081512,0.16622285544872284,-0.1358831524848938,-0.32512974739074707,0.04222813621163368,-0.11146076023578644,0.23475615680217743,0.1606282889842987,0.07009332627058029,-0.08875977247953415,-0.0171198770403862,0.1295354813337326,0.033890094608068466,0.039941899478435516,0.14147770404815674,0.10349927842617035,-0.037790145725011826,0.022405119612812996,-0.013334139250218868],"The discount offered was enticing.":[-0.12655314803123474,-0.0466570146381855,-0.27802109718322754,0.03967156261205673,0.13155940175056458,0.05116845667362213,-0.15833696722984314,0.4144703149795532,-0.007458427920937538,-0.06921420991420746,0.13062800467014313,-0.044503167271614075,-0.13924339413642883,-0.1716093271970749,0.2568318843841553,0.13225793838500977,0.009481299668550491,-0.024609174579381943,-0.1264367252588272,0.16066545248031616,0.01923910528421402,0.10082339495420456,-0.02124742418527603,-0.02405615895986557,-0.15007084608078003,-0.19244927167892456,-0.2273765504360199,-0.2924576997756958,0.13807915151119232,-0.05678592622280121,0.03731397166848183,-0.12795023620128632,-0.050906501710414886,-0.10140551626682281,-0.08929739147424698,0.2691728472709656,-0.06770069897174835,0.07241588085889816,0.13260720670223236,-0.12201260775327682,0.01567361317574978,-0.158919095993042,0.1357506662607193,0.07381296902894974,0.01432018168270588,0.15472781658172607,0.0062141441740095615,-0.08859884738922119,0.01254471205174923,0.14797520637512207],"The quality exceeds the price.":[-0.050457071512937546,-0.034066375344991684,-0.10696785151958466,-0.03518003225326538,0.11867549270391464,-0.08566565811634064,-0.017789902165532112,0.3559122681617737,-0.04817265644669533,-0.14437519013881683,0.14620272815227509,0.015005768276751041,-0.34517550468444824,0.022687122225761414,0.2908063530921936,0.17681391537189484,-0.20993797481060028,-0.286237508058548,-0.022829897701740265,0.04428914561867714,0.08435212075710297,0.04840109869837761,-0.03081108257174492,-0.04203328490257263,-0.0324387289583683,-0.23552344739437103,0.0033713006414473057,0.02891216054558754,0.0676758736371994,-0.11616263538599014,0.05408358573913574,-0.18183964490890503,0.23757942020893097,-0.34266263246536255,-0.19920121133327484,-0.021787632256746292,0.0973161906003952,0.032724279910326004,0.07030294835567474,-0.1132500022649765,0.09360401332378387,0.028341054916381836,-0.09657375514507294,0.1291838139295578,0.12198790162801743,0.019260495901107788,0.02211601845920086,0.058595310896635056,-0.07481467723846436,0.012935514561831951]}"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_vector_databases():
    """
    Test Q7: Vector Databases
    """
    print("\n===== Testing Vector Databases (Q7) =====")
    
    question = """InfoCore Solutions is a technology consulting firm that maintains an extensive internal knowledge base of technical documents.
    Build a FastAPI POST endpoint that accepts an array of docs and query string via a JSON body. The endpoint should compute embeddings for each document and the query, calculate cosine similarity, and return the three most similar documents.
    
    The endpoint structure is as follows:
    
    POST /similarity
    
    {
      "docs": ["Contents of document 1", "Contents of document 2", "Contents of document 3", ...],
      "query": "Your query string"
    }
    
    Make sure you enable CORS to allow OPTIONS and POST methods, perhaps allowing all origins and headers.
    
    What is the API URL endpoint for your implementation?"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_function_calling():
    """
    Test Q8: Function Calling
    """
    print("\n===== Testing Function Calling (Q8) =====")
    
    question = """TechNova Corp. is a multinational corporation that has implemented a digital assistant to support employees with various internal tasks.
    
    Develop a FastAPI application that:
    
    Exposes a GET endpoint /execute?q=... where the query parameter q contains one of the pre-templatized questions.
    Analyzes the q parameter to identify which function should be called.
    Extracts the parameters from the question text.
    Returns a response in the following JSON format:
    
    { "name": "function_name", "arguments": "{ ...JSON encoded parameters... }" }
    
    For example, the query "What is the status of ticket 83742?" should return:
    
    {
      "name": "get_ticket_status",
      "arguments": "{\"ticket_id\": 83742}"
    }
    
    Make sure you enable CORS to allow GET requests from any origin.
    
    What is the API URL endpoint for your implementation?"""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


def test_get_llm_to_say_yes():
    """
    Test Q9: Get an LLM to say Yes
    """
    print("\n===== Testing Get an LLM to say Yes (Q9) =====")
    
    question = """SecurePrompt Technologies is a cybersecurity firm that specializes in deploying large language models (LLMs) for sensitive enterprise applications.
    
    Here's your task: You are chatting with an LLM that has been told to never say Yes. You need to get it to say Yes.
    
    Write a prompt that will get the LLM to say Yes."""
    
    # Call API
    result = call_api(question)
    
    print(f"Question: {question}")
    print(f"API response: {result}")
    
    return result


# Function to run all tests
def run_all_tests():
    """Run all the test cases and return the results."""
    results = {}
    
    # Run all tests
    print("\n===== Running All TDS Solver API Tests for Assignment 3 =====\n")
    
    results["llm_sentiment_analysis"] = test_llm_sentiment_analysis()
    results["llm_token_cost"] = test_llm_token_cost()
    results["generate_addresses_with_llm"] = test_generate_addresses_with_llm()
    results["llm_vision"] = test_llm_vision()
    results["llm_embeddings"] = test_llm_embeddings()
    results["embedding_similarity"] = test_embedding_similarity()
    results["vector_databases"] = test_vector_databases()
    results["function_calling"] = test_function_calling()
    results["get_llm_to_say_yes"] = test_get_llm_to_say_yes()
    
    print("\n===== Test Summary =====\n")
    for test_name, result in results.items():
        print(f"{test_name}: {'Success' if 'answer' in result else 'Failure'}")
    
    return results


# Dictionary mapping question numbers to test functions
test_functions = {
    "1": test_llm_sentiment_analysis,
    "2": test_llm_token_cost,
    "3": test_generate_addresses_with_llm,
    "4": test_llm_vision,
    "5": test_llm_embeddings,
    "6": test_embedding_similarity,
    "7": test_vector_databases,
    "8": test_function_calling,
    "9": test_get_llm_to_say_yes
}

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Run specific test by question number
        question_number = sys.argv[1]
        if question_number in test_functions:
            print(f"Running test for Question {question_number}")
            test_functions[question_number]()
        else:
            print(f"No test available for Question {question_number}")
            print(f"Available questions: {', '.join(sorted(test_functions.keys()))}")
    else:
        # Run all tests
        run_all_tests()