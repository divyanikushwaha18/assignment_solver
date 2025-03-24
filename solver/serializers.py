from rest_framework import serializers
from .models import Assignment, Solution

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ['id', 'question', 'answer', 'created_at']

class AssignmentSerializer(serializers.ModelSerializer):
    solutions = SolutionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'solutions']