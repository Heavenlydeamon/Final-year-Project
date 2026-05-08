from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ----------------------------
# SECTION MODEL
# ----------------------------
class Section(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)
    is_general = models.BooleanField(default=False, help_text="General sections (Environment, Heritage, Cultural) are shown on home page and can only be edited by admin")
    class_obj = models.ForeignKey('Class', on_delete=models.CASCADE, null=True, blank=True, related_name='class_sections', help_text="Link section to a specific class if it's class-specific content")

    def __str__(self):
        return self.name


# ----------------------------
# TOPIC MODEL
# ----------------------------
class Topic(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(blank=True)
    audio_url = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    is_general = models.BooleanField(default=False, help_text="General topics are visible to all students")
    # Self-referential foreign key for tree structure (Knowledge Bloom)
    parent_topic = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='sub_topics',
        help_text="Parent topic in the Knowledge Bloom tree (leave empty for root topics)"
    )

    def __str__(self):
        return self.name
    
    def get_children(self):
        """Get all direct children of this topic"""
        return self.sub_topics.all().order_by('order')
    
    def get_all_descendants(self):
        """Get all descendants recursively"""
        descendants = []
        for child in self.sub_topics.all():
            descendants.append(child)
            descendants.extend(child.get_all_descendants())
        return descendants
    
    def is_root(self):
        """Check if this is a root topic (no parent)"""
        return self.parent_topic is None
    
    def get_root(self):
        """Get the root ancestor of this topic"""
        if self.parent_topic:
            return self.parent_topic.get_root()
        return self


# ----------------------------
# CONCEPT TAG MODEL
# ----------------------------
class ConceptTag(models.Model):
    """Concept tags for AI-based recommendations and content organization"""
    name = models.CharField(max_length=100, unique=True, help_text="e.g., Carbon Cycle, Biodiversity, Wildlife Conservation")
    description = models.TextField(blank=True, help_text="Brief description of the concept")
    
    def __str__(self):
        return self.name


# ----------------------------
# STUDY MATERIAL MODEL
# ----------------------------
class StudyMaterial(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    ESTIMATED_TIME_CHOICES = [
        ('short', 'Short (5 min)'),
        ('medium', 'Medium (10-15 min)'),
        ('long', 'Long (20 min)'),
    ]
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='study_materials')
    title = models.CharField(max_length=200)
    content_text = models.TextField(help_text="Content with sections: Definition, Explanation, Example, Case Study, Summary")
    
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner', 
                                  help_text="Beginner=Basics, Intermediate=Process&Details, Advanced=Case Studies")
    estimated_time = models.CharField(max_length=20, choices=ESTIMATED_TIME_CHOICES, default='short',
                                     help_text="Short=5min, Medium=10-15min, Long=20min")
    summary = models.TextField(blank=True, help_text="AI-generated summary of the material")
    concept_tags = models.ManyToManyField(ConceptTag, blank=True, related_name='study_materials',
                                         help_text="Tags for AI recommendations")
    
    image_url = models.URLField(blank=True)
    audio_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='study_materials/images/', blank=True, null=True)
    audio = models.FileField(upload_to='study_materials/audio/', blank=True, null=True)
    video = models.FileField(upload_to='study_materials/video/', blank=True, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    def get_difficulty_label(self):
        return dict(self.DIFFICULTY_CHOICES).get(self.difficulty, 'Beginner')
    
    def get_time_label(self):
        return dict(self.ESTIMATED_TIME_CHOICES).get(self.estimated_time, '5 min')


# ----------------------------
# MATERIAL VIEW MODEL
# ----------------------------
class MaterialView(models.Model):
    """Track student viewing of study materials for personalization"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='material_views')
    material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE, related_name='views')
    time_spent = models.IntegerField(default=0, help_text="Time spent in seconds")
    completion_status = models.BooleanField(default=False, help_text="Whether user completed viewing")
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-viewed_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.material.title} - {self.time_spent}s"


# ----------------------------
# MATERIAL ATTEMPT MODEL
# ----------------------------
class MaterialAttempt(models.Model):
    """Track before/after quiz scores - Impact Score = After Score - Before Score"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='material_attempts')
    material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE, related_name='attempts')
    
    before_score = models.IntegerField(default=0)
    after_score = models.IntegerField(default=0)
    before_total = models.IntegerField(default=0)
    after_total = models.IntegerField(default=0)
    
    studied_at = models.DateTimeField(auto_now_add=True)
    quiz_taken_at = models.DateTimeField(null=True, blank=True)
    
    @property
    def impact_score(self):
        before_pct = (self.before_score / self.before_total * 100) if self.before_total > 0 else 0
        after_pct = (self.after_score / self.after_total * 100) if self.after_total > 0 else 0
        return round(after_pct - before_pct, 1)
    
    @property
    def impact_label(self):
        score = self.impact_score
        if score >= 20:
            return 'Highly Effective'
        elif score >= 10:
            return 'Moderate'
        return 'Low'
    
    def __str__(self):
        return f"{self.user.username} - {self.material.title} - Impact: {self.impact_score}%"


# ----------------------------
# QUESTION MODEL
# ----------------------------
class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='questions')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True, related_name='questions')
    question_text = models.CharField(max_length=500)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')

    def __str__(self):
        return self.question_text


# ----------------------------
# CHOICE MODEL
# ----------------------------
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


# ----------------------------
# MATCH QUIZ MODELS (Lower Class)
# ----------------------------
class MatchQuiz(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='match_quizzes')
    title = models.CharField(max_length=200, help_text="e.g., Match the Artform to the Region")
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.topic.name} - {self.title}"

class MatchPair(models.Model):
    quiz = models.ForeignKey(MatchQuiz, on_delete=models.CASCADE, related_name='pairs')
    left_item = models.CharField(max_length=150, help_text="e.g., Theyyam")
    left_image = models.ImageField(upload_to='match_quiz/', blank=True, null=True)
    right_item = models.CharField(max_length=150, help_text="e.g., North Malabar")
    right_image = models.ImageField(upload_to='match_quiz/', blank=True, null=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return f"{self.left_item} <-> {self.right_item}"


# ----------------------------
# QUIZ ATTEMPT MODEL
# ----------------------------
class QuizAttempt(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    class_obj = models.ForeignKey('Class', on_delete=models.CASCADE, null=True, blank=True, related_name='quiz_attempts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='quiz_attempts')
    user_identifier = models.CharField(max_length=100)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    date_attempted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        topic_name = self.topic.name if self.topic else self.section.name
        return f"{self.user_identifier} - {topic_name} - {self.score}/{self.total_questions}"


# ----------------------------
# INSTITUTION MODEL
# ----------------------------
class Institution(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


# ----------------------------
# CLASS MODEL
# ----------------------------
class Class(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100, blank=True, help_text="Subject taught in this class")
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='classes', null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_classes')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_lower_class = models.BooleanField(default=False)
    projection_topic = models.ForeignKey('content.Topic', on_delete=models.SET_NULL, null=True, blank=True, related_name='linked_classes_main')
    projection_story = models.ForeignKey('content.Story', on_delete=models.SET_NULL, null=True, blank=True, related_name='linked_classes_main')
    
    class Meta:
        # unique_together = ('name', 'institution')
        pass
    
    def __str__(self):
        inst_name = self.institution.name if self.institution else "Independent"
        return f"{self.name} - {inst_name}"
    
    def get_total_students(self):
        return Enrollment.objects.filter(class_obj=self, is_active=True).count()
    
    def get_students(self):
        return User.objects.filter(enrollments__class_obj=self, enrollments__is_active=True).distinct()


# ----------------------------
# USER PROFILE MODEL
# ----------------------------
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachers')
    student_class = models.ManyToManyField(Class, blank=True, related_name='students')
    
    email = models.EmailField(max_length=254, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, help_text="Profile picture")
    position = models.CharField(max_length=100, blank=True, help_text="e.g., Professor, Lecturer, Head of Department")
    
    # XP Reward System fields
    xp = models.IntegerField(default=0, help_text="Current XP points")
    level = models.IntegerField(default=1, help_text="Current level based on XP")
    total_xp_earned = models.IntegerField(default=0, help_text="Total XP earned all time")
    
    # Feature Loop System fields
    points = models.IntegerField(default=0, help_text="Points used for higher class feature loop (performance, leaderboard, challenges)")
    
    # Streak & Activity fields
    current_streak = models.IntegerField(default=0, help_text="Current daily login streak")
    max_streak = models.IntegerField(default=0, help_text="Highest daily login streak achieved")
    last_activity_date = models.DateField(null=True, blank=True, help_text="Last date user was active")
    
    # Daily Challenge specific fields
    challenge_streak = models.IntegerField(default=0, help_text="Current daily challenge streak")
    max_challenge_streak = models.IntegerField(default=0, help_text="Highest daily challenge streak achieved")
    last_challenge_date = models.DateField(null=True, blank=True, help_text="Last date user completed a daily challenge")
    challenge_points = models.IntegerField(default=0, help_text="Points earned from daily challenges")
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    def award_quiz_points(self, score_percentage):
        if score_percentage >= 90:
            earned = 15
        elif score_percentage >= 70:
            earned = 10
        elif score_percentage >= 50:
            earned = 5
        else:
            earned = 0
            
        if earned > 0:
            self.points += earned
            self.save(update_fields=['points'])
        return earned
    
    def get_xp_for_next_level(self):
        """Get XP needed for next level"""
        return self.level * 100
    
    def get_xp_progress(self):
        """Get XP progress percentage to next level"""
        xp_in_current_level = self.xp - ((self.level - 1) * 100)
        xp_needed = self.get_xp_for_next_level()
        return min(100, int((xp_in_current_level / xp_needed) * 100))
    
    def get_xp_ring_offset(self):
        """Get the stroke-dasharray offset for the XP circular progress ring (Total 339.29)"""
        progress = self.get_xp_progress()
        return round((progress / 100) * 339.29, 2)


# ----------------------------
# TEACHER MODEL
# ----------------------------
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    
    CLASS_LEVEL_CHOICES = [
        ('LP', 'Lower Primary'),
        ('UP', 'Upper Primary'),
        ('HS', 'High School'),
        ('HSS', 'Higher Secondary'),
    ]

    class_level = models.CharField(
        max_length=10, 
        choices=CLASS_LEVEL_CHOICES,
        default='HS',
        help_text="Primary teaching level for dashboard customization"
    )
    
    id_card_number = models.CharField(
        max_length=50, 
        unique=True, 
        null=True, 
        blank=True, 
        help_text="Official Teacher Identification Number"
    )
    is_approved = models.BooleanField(
        default=False, 
        help_text="Whether this teacher has been approved by an administrator"
    )

    def __str__(self):
        return f"Teacher: {self.user.username} ({self.get_class_level_display()})"


# ----------------------------
# STUDENT MARKS MODEL
# ----------------------------
class StudentMarks(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marks')
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='class_marks', null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    marks = models.IntegerField(default=0)
    max_marks = models.IntegerField(default=100)
    remarks = models.TextField(blank=True)
    date_assigned = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_marks')

    def __str__(self):
        return f"{self.student.username} - {self.section.name} - {self.marks}/{self.max_marks}"


# ----------------------------
# TOPIC PROGRESS MODEL (Knowledge Bloom)
# ----------------------------
class TopicProgress(models.Model):
    """Track student progress through topics in the Knowledge Bloom"""
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_progress')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='student_progress')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    is_studied = models.BooleanField(default=False, help_text="User has explicitly marked the theory material as studied")
    activity_completed = models.BooleanField(default=False, help_text="User has successfully completed the interactive activity")
    quiz_score = models.IntegerField(default=0, help_text="Best quiz score for this topic")
    quiz_total = models.IntegerField(default=0, help_text="Total questions in the quiz")
    quiz_percentage = models.FloatField(default=0, help_text="Quiz score percentage")
    
    study_time_minutes = models.IntegerField(default=0, help_text="Total time spent studying")
    
    # NEW Valuation fields for higher class students
    VALUATION_STATUS_CHOICES = [
        ('pending_review', 'Pending Review'),
        ('published', 'Published'),
    ]
    manual_marks = models.FloatField(default=0, help_text="Optional manual marks from teacher")
    composite_marks = models.FloatField(default=0, help_text="Total marks (Auto + Manual)")
    valuation_status = models.CharField(max_length=20, choices=VALUATION_STATUS_CHOICES, default='pending_review')
    
    last_accessed = models.DateTimeField(auto_now=True, help_text="Last time student accessed this topic")
    completed_at = models.DateTimeField(null=True, blank=True, help_text="When topic was completed")
    
    class Meta:
        unique_together = ('user', 'topic')
        ordering = ['-last_accessed']
    
    def __str__(self):
        return f"{self.user.username} - {self.topic.name} - {self.status}"

    
    def is_unlocked(self):
        """Check if this topic is unlocked based on parent's completion"""
        if self.topic.is_root():
            return True  # Root topics are always unlocked
        
        # Check parent's progress
        try:
            parent_progress = TopicProgress.objects.get(user=self.user, topic=self.topic.parent_topic)
            return parent_progress.status == 'completed'
        except TopicProgress.DoesNotExist:
            return False  # Parent not completed = locked
    
    def can_access(self):
        """Check if student can access this topic"""
        return self.status != 'not_started' or self.is_unlocked()


# ----------------------------
# CHALLENGE ATTEMPT MODEL
# ----------------------------
class ChallengeAttempt(models.Model):
    CHALLENGE_TYPES = [
        ('timed', 'Timed Challenge'),
        ('rapid', 'Rapid Fire'),
        ('adaptive', 'Adaptive Difficulty'),
        ('eco_rush', 'Eco-Rush (Timed)'),
        ('survival', 'Survival Mode (3 Strikes)'),
        ('sprint', 'Heritage Sprint'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_attempts')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True, related_name='challenge_attempts')
    class_obj = models.ForeignKey('Class', on_delete=models.CASCADE, null=True, blank=True, related_name='challenge_attempts')
    challenge_type = models.CharField(max_length=10, choices=CHALLENGE_TYPES, default='timed')
    
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    time_limit_per_question = models.IntegerField(default=15)
    total_time_limit = models.IntegerField(null=True, blank=True, help_text="Total time for the challenge in seconds (for Eco-Rush)")
    
    score = models.IntegerField(default=0)
    total_xp_earned = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    strikes_count = models.IntegerField(default=0, help_text="Number of wrong answers in this session")
    current_streak = models.IntegerField(default=0)
    max_streak = models.IntegerField(default=0)
    
    current_difficulty = models.CharField(max_length=10, choices=Question.DIFFICULTY_CHOICES, default='easy')
    
    is_completed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.challenge_type} - {self.score}/{self.total_questions}"


# ----------------------------
# CHALLENGE QUESTION MODEL
# ----------------------------
class ChallengeQuestion(models.Model):
    challenge = models.ForeignKey(ChallengeAttempt, on_delete=models.CASCADE, related_name='challenge_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    question_order = models.IntegerField(default=0)
    
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    time_taken = models.FloatField(default=0)
    points_earned = models.IntegerField(default=0)
    
    shown_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['question_order']
    
    def __str__(self):
        return f"Challenge {self.challenge.id} - Q{self.question_order}: {self.question.question_text[:50]}"


# ----------------------------
# CLASS JOIN REQUEST MODEL
# ----------------------------
class ClassJoinRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='join_requests')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='join_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, help_text="Optional message from the student")
    request_date = models.DateTimeField(auto_now_add=True)
    processed_date = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_requests')
    
    class Meta:
        unique_together = ('student', 'class_obj')
        ordering = ['-request_date']
    
    def __str__(self):
        return f"{self.student.username} - {self.class_obj.name} - {self.status}"


# ----------------------------
# ENROLLMENT MODEL
# ----------------------------
class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='enrollments')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('student', 'class_obj')
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.class_obj.name}"


# ============================================
# AI QUIZ GENERATOR MODELS
# ============================================

class AIGeneratedQuiz(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    CONTENT_TYPE_CHOICES = [
        ('general', 'General Content (Admin)'),
        ('class', 'Class-specific (Teacher)'),
    ]
    
    title = models.CharField(max_length=200, help_text="Title for the generated quiz")
    description = models.TextField(blank=True, help_text="Optional description")
    
    study_material = models.ForeignKey(
        StudyMaterial, 
        on_delete=models.CASCADE, 
        related_name='ai_generated_quizzes',
        help_text="Source study material used for generation"
    )
    
    content_type = models.CharField(
        max_length=20, 
        choices=CONTENT_TYPE_CHOICES, 
        default='general',
        help_text="General content requires admin approval, class content uses teacher approval"
    )
    
    section = models.ForeignKey(
        Section, 
        on_delete=models.CASCADE, 
        related_name='ai_generated_quizzes'
    )
    topic = models.ForeignKey(
        Topic, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='ai_generated_quizzes'
    )
    class_obj = models.ForeignKey(
        Class, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='ai_generated_quizzes',
        help_text="Class this quiz belongs to (for class-specific content)"
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft',
        help_text="Current approval status"
    )
    
    generated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='generated_quizzes',
        help_text="User who generated this quiz"
    )
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approved_quizzes',
        help_text="User who approved this quiz"
    )
    
    generated_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True, help_text="When submitted for approval")
    reviewed_at = models.DateTimeField(null=True, blank=True, help_text="When reviewed/approved")
    
    rejection_reason = models.TextField(blank=True, help_text="Reason if rejected")
    used_count = models.IntegerField(default=0, help_text="Number of times this quiz was used")
    
    class Meta:
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.title} - {self.status}"


class AIGeneratedQuestion(models.Model):
    """
    Store individual questions from AI-generated quizzes.
    
    Includes is_verified field for review workflow:
    - False: AI-generated, requires admin/teacher review
    - True: Verified and approved for use
    """
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    quiz = models.ForeignKey(
        AIGeneratedQuiz, 
        on_delete=models.CASCADE, 
        related_name='questions'
    )
    question_text = models.CharField(max_length=500)
    difficulty = models.CharField(
        max_length=10, 
        choices=DIFFICULTY_CHOICES, 
        default='medium'
    )
    order = models.IntegerField(default=0, help_text="Order of question in quiz")
    
    # Review workflow - AI saves as False, admin/teachers verify before use
    is_verified = models.BooleanField(
        default=False, 
        help_text="Question has been reviewed and verified (not a generic placeholder)"
    )
    
    # Source fact for tracking which fact this question tests
    source_fact = models.CharField(
        max_length=200, 
        blank=True,
        help_text="The specific fact or data point this question tests"
    )
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Q{self.order}: {self.question_text[:50]}"


class AIGeneratedChoice(models.Model):
    """Store choices for AI-generated questions."""
    question = models.ForeignKey(
        AIGeneratedQuestion, 
        on_delete=models.CASCADE, 
        related_name='choices'
    )
    choice_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.choice_text


# ============================================
# GAMIFICATION & REWARD MODELS
# ============================================

class CollectibleItem(models.Model):
    CATEGORY_CHOICES = [
        ('flora', 'Flora (Botanical)'),
        ('fauna', 'Fauna (Wildlife)'),
        ('folklore', 'Folklore (Legend)'),
        ('artifact', 'Artifact (History)'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='collectibles/', blank=True, null=True)
    icon = models.CharField(max_length=50, default='fa-gem', help_text="FontAwesome icon class")
    rarity = models.CharField(max_length=20, choices=[('common', 'Common'), ('rare', 'Rare'), ('epic', 'Epic'), ('legendary', 'Legendary')], default='common')
    xp_value = models.IntegerField(default=50)
    associated_topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, help_text="Topic that unlocks this collectible on the progress map")
    
    def __str__(self):
        return f"{self.name} ({self.category})"

class UserCollectible(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='collectibles', null=True, blank=True)
    item = models.ForeignKey(CollectibleItem, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('profile', 'item')

    def __str__(self):
        return f"{self.profile.user.username if self.profile else 'Unknown'} unlocked {self.item.name}"

class ArtifactShard(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    parent_artifact = models.ForeignKey(CollectibleItem, on_delete=models.CASCADE, limit_choices_to={'category': 'artifact'})
    shard_index = models.IntegerField(help_text="Position of this shard in the reconstruction (e.g., 1 of 4)")
    total_shards = models.IntegerField(default=4)
    image = models.ImageField(upload_to='artifacts/shards/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} (Shard {self.shard_index}/{self.total_shards} of {self.parent_artifact.name})"

class UserArtifactShard(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='artifact_shards', null=True, blank=True)
    shard = models.ForeignKey(ArtifactShard, on_delete=models.CASCADE)
    found_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('profile', 'shard')

class League(models.Model):
    name = models.CharField(max_length=100)
    min_xp = models.IntegerField(default=0)
    max_xp = models.IntegerField(default=1000)
    icon = models.CharField(max_length=50, default='fa-trophy', help_text="FontAwesome icon class")
    
    def __str__(self):
        return self.name

class UserLeague(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='current_league', null=True, blank=True)
    league = models.ForeignKey(League, on_delete=models.SET_NULL, null=True)
    points_this_week = models.IntegerField(default=0)
    rank_last_week = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.profile.user.username if self.profile else 'Unknown'} in {self.league.name if self.league else 'No League'}"


class LeagueNotification(models.Model):
    """Track league promotions, relegations, and other league events."""
    NOTIFICATION_TYPES = [
        ('promotion', 'Promotion'),
        ('relegation', 'Relegation'),
        ('new_league', 'New League Joined'),
    ]

    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='league_notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    old_league = models.ForeignKey(League, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    new_league = models.ForeignKey(League, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    message = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.profile.user.username} — {self.get_notification_type_display()}"


# ============================================
# NARRATIVE STORY COMPANION MODELS
# ============================================

class Story(models.Model):
    """
    Represents a narrative story used for educational purposes.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CollectibleItem.CATEGORY_CHOICES, default='folklore')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='stories/', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Stories"

class StoryNode(models.Model):
    """
    A single node in a narrative story.
    """
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='nodes')
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="Narrative text for this part of the story")
    order = models.IntegerField(default=0)
    image = models.ImageField(upload_to='story_nodes/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.story.title} - {self.title} ({self.order})"

    class Meta:
        ordering = ['order']

class StoryProgress(models.Model):
    """
    Tracks a student's progress through a story.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_progress')
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='user_progress')
    current_node = models.ForeignKey(StoryNode, on_delete=models.SET_NULL, null=True, blank=True)
    completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.story.title} - Node {self.current_node.order if self.current_node else 'N/A'}"

    class Meta:
        unique_together = ('user', 'story')


# ============================================
# INTERACTIVE LEARNING MODES (STORY + COMIC)
# ============================================

class StoryScene(models.Model):
    """
    A single scene in Story Mode for a given topic.
    """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='story_scenes')
    scene_number = models.IntegerField(default=1)
    text = models.TextField(help_text="Narrative text for this scene")
    image = models.ImageField(upload_to='story/scenes/', blank=True, null=True)
    teacher_prompt = models.TextField(blank=True, help_text="Prompts for the teacher to ask students (e.g., 'Why does rain fall here?')")
    
    class Meta:
        ordering = ['scene_number']
        verbose_name = "Story Scene"
        verbose_name_plural = "Story Scenes"

    def __str__(self):
        return f"{self.topic.name} - Scene {self.scene_number}"






# ============================================
# INTERACTIVE DISTRICT MAP
# ============================================

class District(models.Model):
    """
    Represents a district in Kerala linked to a specific topic.
    """
    name = models.CharField(max_length=100, unique=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='districts', help_text="General content topic for this district")
    folklore_topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='folklore_districts', help_text="Specific folklore/myth topic for this district")
    coords = models.CharField(max_length=500, help_text="Image map coordinates (x1,y1,x2,y2 or poly coords)")
    
    class Meta:
        verbose_name = "District"
        verbose_name_plural = "Districts"

    def __str__(self):
        return f"{self.name} - {self.topic.name}"


# ----------------------------
# DAILY TOPIC CHALLENGE MODELS
# ----------------------------

class DailyTopicChallenge(models.Model):
    """
    A daily challenge for a specific topic.
    Expires in 8 hours and awards bonus points.
    """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='daily_challenges')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    expiry_time = models.DateTimeField(help_text="When this challenge expires")
    points_bonus = models.IntegerField(default=15)
    
    class Meta:
        ordering = ['-date']

    def is_expired(self):
        return timezone.now() > self.expiry_time

    def time_remaining_seconds(self):
        diff = self.expiry_time - timezone.now()
        return max(0, int(diff.total_seconds()))

    def __str__(self):
        return f"Daily Challenge: {self.topic.name} ({self.date})"

class DailyChallengeSubmission(models.Model):
    """
    Tracks user submissions for daily challenges.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_submissions')
    challenge = models.ForeignKey(DailyTopicChallenge, on_delete=models.CASCADE, related_name='submissions')
    is_correct = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'challenge')

    def __str__(self):
        return f"{self.user.username} - {self.challenge.topic.name} - {'Correct' if self.is_correct else 'Incorrect'}"
