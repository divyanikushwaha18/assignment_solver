# Assignment 2: Web and Hosting

## 1. Write documentation in Markdown

**Question:** Write documentation in Markdown for an imaginary analysis of the number of steps you walked each day for a week, comparing over time and with friends. The Markdown must include specific formatting elements.

**Answer:**
```markdown
# Weekly Step Count Analysis
 
## Data Collection
 
Used `FitbitAPI` to collect daily step data for myself and 3 friends from January 15-21, 2024.
 
## Methodology
 
The analysis was performed using Python with the following packages:
 
```python
import pandas as pd
import matplotlib.pyplot as plt
from fitbit import FitbitAPI
 
def analyze_steps(user_data):
    return pd.DataFrame(user_data).mean()
```
 
## Results
 
### Personal Achievement
> Exceeded my daily goal of 10,000 steps on 5 out of 7 days!
 
### Daily Breakdown
 
| Day       | My Steps | Friend A | Friend B | Friend C |
|-----------|----------|----------|----------|----------|
| Monday    | 12,345   | 8,901    | 10,234   | 9,876    |
| Tuesday   | 9,876    | 11,234   | 8,765    | 10,543   |
| Wednesday | 11,234   | 9,876    | 12,345   | 8,901    |
 
### Key Findings
 
1. Highest step count: **12,345** (Monday)
2. Average daily steps: *10,798*
3. Group ranking: First place!
 
## Visual Data
 
![Weekly Step Count Graph](/images/step_graph.png)
 
### Contributing Factors
 
* Walking meetings
* Evening jogs
* Weekend hikes
 
Find more fitness tracking tips on [FitTracker Blog](https://fittracker.example.com).
 
## Technical Notes
 
See implementation details in our [GitHub repository](https://github.com/example/steptracker).
```

## 2. Compress an image

**Question:** Download the image and compress it losslessly to an image that is less than 1,500 bytes.

**Answer:** [A compressed image file less than 1,500 bytes]

## 3. Host your portfolio on GitHub Pages

**Question:** What is the GitHub Pages URL for your portfolio containing your email address?

**Answer:** https://divyanikushwaha18.github.io/divyani.github.io/

## 4. Use Google Colab

**Question:** Run this authentication program on Google Colab with your email ID. What is the result?

**Answer:** 19c20

## 5. Use an Image Library in Google Colab

**Question:** Run the code (after fixing a mistake) to calculate the number of pixels with a certain minimum brightness. What is the result?

**Answer:** 171017

## 6. Deploy a Python API to Vercel

**Question:** Create and deploy a Python app to Vercel that returns marks for specified names. What is the Vercel URL?

**Answer:** https://projects-alpha-flax.vercel.app/api

## 7. Create a GitHub Action

**Question:** Create a GitHub action with a step that contains your email address. What is your repository URL?

**Answer:** https://github.com/divyanikushwaha18/projects

## 8. Push an image to Docker Hub

**Question:** Create and push an image to Docker Hub with a tag named 23f3000756. What is the Docker image URL?

**Answer:** https://hub.docker.com/repository/docker/divyani18/myapp/tags

## 9. Write a FastAPI server to serve data

**Question:** Write a FastAPI server that serves student data with filtering by class. What is the API URL endpoint?

**Answer:** http://127.0.0.1:8000/api

## 10. Run a local LLM with Llamafile

**Question:** Run the Llama-3.2-1B-Instruct.Q6_K.llamafile model and create a tunnel using ngrok. What is the ngrok URL?

**Answer:** https://dfa4-2401-4900-889c-3732-1967-be4f-af50-5d44.ngrok-free.app/
