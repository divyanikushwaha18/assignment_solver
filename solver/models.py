from django.db import models

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Solution(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='solutions')
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Solution for {self.assignment.title}"
    
class QuestionRepository(models.Model):
    assignment_number = models.IntegerField()
    question_number = models.IntegerField()
    question_text = models.TextField()
    answer_text = models.TextField()
    # Store keywords for basic matching
    keywords = models.TextField(blank=True, help_text="Comma-separated keywords")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Assignment {self.assignment_number}, Question {self.question_number}"