"""
Tests for AI Recommendation Functions
"""
from django.test import TestCase
from django.contrib.auth.models import User
from mainapp.models import (
    StudyMaterial, QuizAttempt, MaterialView, MaterialAttempt, 
    ConceptTag, Section, Topic
)
from mainapp.views.ai_recommendations import (
    get_weak_concepts,
    calculate_adaptive_difficulty,
    get_recommended_materials,
    get_concept_based_recommendations,
    get_new_user_recommendations,
    calculate_impact_score,
    get_material_effectiveness,
    get_personalized_dashboard_data,
    get_learning_progress_summary
)


class TestGetWeakConcepts(TestCase):
    """Test get_weak_concepts function"""
    
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create section and topic
        self.section = Section.objects.create(name='Test Section', description='Test')
        self.topic = Topic.objects.create(section=self.section, name='Test Topic', description='Test')
        
        # Create quiz attempts with low accuracy (<50%)
        QuizAttempt.objects.create(
            user=self.user,
            user_identifier=self.user.username,
            section=self.section,
            topic=self.topic,
            score=3,
            total_questions=10  # 30% accuracy
        )
    
    def test_get_weak_concepts_returns_weak_topics(self):
        """Test that weak concepts are detected correctly"""
        weak_topics = get_weak_concepts(self.user)
        
        self.assertEqual(len(weak_topics), 1)
        self.assertEqual(weak_topics[0]['topic'], self.topic)
        self.assertEqual(weak_topics[0]['accuracy'], 30.0)
    
    def test_get_weak_concepts_includes_attempt_count(self):
        """Test that total_attempts is included in results"""
        weak_topics = get_weak_concepts(self.user)
        
        self.assertIn('total_attempts', weak_topics[0])
        self.assertEqual(weak_topics[0]['total_attempts'], 1)
    
    def test_get_weak_concepts_sorted_by_accuracy(self):
        """Test that weak topics are sorted by accuracy (weakest first)"""
        # Add another topic with even lower accuracy
        topic2 = Topic.objects.create(section=self.section, name='Topic 2', description='Test')
        QuizAttempt.objects.create(
            user=self.user,
            user_identifier=self.user.username,
            section=self.section,
            topic=topic2,
            score=1,
            total_questions=10  # 10% accuracy
        )
        
        weak_topics = get_weak_concepts(self.user)
        
        self.assertEqual(len(weak_topics), 2)
        self.assertEqual(weak_topics[0]['accuracy'], 10.0)  # Should be first (weakest)
        self.assertEqual(weak_topics[1]['accuracy'], 30.0)


class TestCalculateAdaptiveDifficulty(TestCase):
    """Test calculate_adaptive_difficulty function"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser2', password='testpass')
        self.section = Section.objects.create(name='Section', description='Test')
        self.topic = Topic.objects.create(section=self.section, name='Topic', description='Test')
    
    def test_no_attempts_returns_beginner(self):
        """Test that new topics return beginner difficulty"""
        difficulty = calculate_adaptive_difficulty(self.user, self.topic)
        self.assertEqual(difficulty, 'beginner')
    
    def test_low_accuracy_returns_beginner(self):
        """Test that low accuracy returns beginner"""
        QuizAttempt.objects.create(
            user=self.user,
            user_identifier=self.user.username,
            section=self.section,
            topic=self.topic,
            score=3,
            total_questions=10
        )
        
        difficulty = calculate_adaptive_difficulty(self.user, self.topic)
        self.assertEqual(difficulty, 'beginner')
    
    def test_improving_trend_returns_higher_difficulty(self):
        """Test that improving trend leads to higher difficulty"""
        # First attempt - low score
        QuizAttempt.objects.create(
            user=self.user,
            user_identifier=self.user.username,
            section=self.section,
            topic=self.topic,
            score=3,
            total_questions=10
        )
        # Second attempt - better score
        QuizAttempt.objects.create(
            user=self.user,
            user_identifier=self.user.username,
            section=self.section,
            topic=self.topic,
            score=7,
            total_questions=10
        )
        
        difficulty = calculate_adaptive_difficulty(self.user, self.topic)
        self.assertEqual(difficulty, 'intermediate')
    
    def test_declining_trend_returns_lower_difficulty(self):
        """Test that declining trend leads to lower difficulty"""
        # First attempt - good score
        QuizAttempt.objects.create(
            user=self.user,
            user_identifier=self.user.username,
            section=self.section,
            topic=self.topic,
            score=8,
            total_questions=10
        )
        # Second attempt - lower score
        QuizAttempt.objects.create(
            user=self.user,
            user_identifier=self.user.username,
            section=self.section,
            topic=self.topic,
            score=4,
            total_questions=10
        )
        
        difficulty = calculate_adaptive_difficulty(self.user, self.topic)
        self.assertEqual(difficulty, 'beginner')


class TestGetRecommendedMaterials(TestCase):
    """Test get_recommended_materials function"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser3', password='testpass')
        self.section = Section.objects.create(name='Section', description='Test')
        self.topic = Topic.objects.create(section=self.section, name='Topic', description='Test')
        
        # Create weak topic
        QuizAttempt.objects.create(
            user=self.user,
            user_identifier=self.user.username,
            section=self.section,
            topic=self.topic,
            score=3,
            total_questions=10
        )
        
        # Create beginner material
        self.material = StudyMaterial.objects.create(
            topic=self.topic,
            title='Beginner Material',
            content_text='Test content',
            difficulty='beginner'
        )
    
    def test_returns_recommendations_for_weak_topics(self):
        """Test that recommendations are returned for weak topics"""
        weak_topics = get_weak_concepts(self.user)
        recommendations = get_recommended_materials(self.user, weak_topics)
        
        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0]['material'], self.material)
    
    def test_includes_fallback_flag(self):
        """Test that is_fallback flag is included"""
        weak_topics = get_weak_concepts(self.user)
        recommendations = get_recommended_materials(self.user, weak_topics)
        
        self.assertIn('is_fallback', recommendations[0])
    
    def test_includes_suggested_difficulty(self):
        """Test that suggested_difficulty is included"""
        weak_topics = get_weak_concepts(self.user)
        recommendations = get_recommended_materials(self.user, weak_topics)
        
        self.assertIn('suggested_difficulty', recommendations[0])


class TestCalculateImpactScore(TestCase):
    """Test calculate_impact_score function"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser4', password='testpass')
        self.section = Section.objects.create(name='Section', description='Test')
        self.topic = Topic.objects.create(section=self.section, name='Topic', description='Test')
        self.material = StudyMaterial.objects.create(
            topic=self.topic,
            title='Test Material',
            content_text='Test content'
        )
    
    def test_returns_dict_with_impact_score(self):
        """Test that function returns dict with calculated impact"""
        result = calculate_impact_score(
            self.user, self.material,
            before_score=3, before_total=10,
            after_score=7, after_total=10
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('impact_score', result)
        self.assertEqual(result['impact_score'], 40.0)  # 70% - 30% = 40%
    
    def test_impact_label_highly_effective(self):
        """Test highly effective label for >= 20% impact"""
        result = calculate_impact_score(
            self.user, self.material,
            before_score=3, before_total=10,
            after_score=7, after_total=10
        )
        
        self.assertEqual(result['impact_label'], 'Highly Effective')
    
    def test_impact_label_moderate(self):
        """Test moderate label for >= 10% impact"""
        result = calculate_impact_score(
            self.user, self.material,
            before_score=3, before_total=10,
            after_score=5, after_total=10
        )
        
        self.assertEqual(result['impact_label'], 'Moderate')
    
    def test_impact_label_low(self):
        """Test low label for < 10% impact"""
        result = calculate_impact_score(
            self.user, self.material,
            before_score=3, before_total=10,
            after_score=4, after_total=10
        )
        
        self.assertEqual(result['impact_label'], 'Low')
    
    def test_includes_percentages(self):
        """Test that before and after percentages are included"""
        result = calculate_impact_score(
            self.user, self.material,
            before_score=3, before_total=10,
            after_score=7, after_total=10
        )
        
        self.assertEqual(result['before_percentage'], 30.0)
        self.assertEqual(result['after_percentage'], 70.0)


class TestGetNewUserRecommendations(TestCase):
    """Test get_new_user_recommendations function"""
    
    def setUp(self):
        self.section = Section.objects.create(name='Section', description='Test')
        self.topic = Topic.objects.create(section=self.section, name='Topic', description='Test')
        
        # Create some materials
        for i in range(5):
            StudyMaterial.objects.create(
                topic=self.topic,
                title=f'Material {i}',
                content_text=f'Content {i}'
            )
    
    def test_returns_materials(self):
        """Test that materials are returned"""
        recommendations = get_new_user_recommendations()
        
        self.assertEqual(len(recommendations), 5)
    
    def test_respects_limit(self):
        """Test that limit is respected"""
        recommendations = get_new_user_recommendations(limit=3)
        
        self.assertEqual(len(recommendations), 3)


class TestGetPersonalizedDashboardData(TestCase):
    """Test get_personalized_dashboard_data function"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser5', password='testpass')
        self.section = Section.objects.create(name='Section', description='Test')
        self.topic = Topic.objects.create(section=self.section, name='Topic', description='Test')
    
    def test_new_user_flag(self):
        """Test that is_new_user flag is True for new users"""
        result = get_personalized_dashboard_data(self.user)
        
        self.assertTrue(result['is_new_user'])
    
    def test_new_user_gets_recommendations(self):
        """Test that new users get new_user_recommendations"""
        result = get_personalized_dashboard_data(self.user)
        
        self.assertIn('new_user_recommendations', result)
    
    def test_existing_user_flag(self):
        """Test that is_new_user flag is False for existing users"""
        # Create a quiz attempt
        QuizAttempt.objects.create(
            user=self.user,
            user_identifier=self.user.username,
            section=self.section,
            topic=self.topic,
            score=5,
            total_questions=10
        )
        
        result = get_personalized_dashboard_data(self.user)
        
        self.assertFalse(result['is_new_user'])
    
    def test_includes_weak_topics_for_existing_users(self):
        """Test that weak topics are included for existing users"""
        QuizAttempt.objects.create(
            user=self.user,
            user_identifier=self.user.username,
            section=self.section,
            topic=self.topic,
            score=3,
            total_questions=10
        )
        
        result = get_personalized_dashboard_data(self.user)
        
        self.assertIn('weak_topics', result)
        self.assertIn('recommended_materials', result)


class TestGetLearningProgressSummary(TestCase):
    """Test get_learning_progress_summary function"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser6', password='testpass')
        self.section = Section.objects.create(name='Section', description='Test')
        self.topic = Topic.objects.create(section=self.section, name='Topic', description='Test')
    
    def test_empty_for_no_attempts(self):
        """Test that empty summary is returned for no attempts"""
        result = get_learning_progress_summary(self.user)
        
        self.assertEqual(result['total_topics_attempted'], 0)
        self.assertEqual(result['total_quizzes_taken'], 0)
        self.assertEqual(result['overall_accuracy'], 0)
    
    def test_calculates_overall_accuracy(self):
        """Test that overall accuracy is calculated correctly"""
        QuizAttempt.objects.create(
            user=self.user,
            user_identifier=self.user.username,
            section=self.section,
            topic=self.topic,
            score=7,
            total_questions=10
        )
        
        result = get_learning_progress_summary(self.user)
        
        self.assertEqual(result['overall_accuracy'], 70.0)
    
    def test_mastery_levels_included(self):
        """Test that mastery levels are included"""
        QuizAttempt.objects.create(
            user=self.user,
            user_identifier=self.user.username,
            section=self.section,
            topic=self.topic,
            score=9,
            total_questions=10  # 90% = Mastered
        )
        
        result = get_learning_progress_summary(self.user)
        
        self.assertIn('mastery_levels', result)
        self.assertEqual(len(result['mastery_levels']), 1)
    
    def test_mastery_level_mastered(self):
        """Test that 80%+ accuracy gets 'Mastered' label"""
        QuizAttempt.objects.create(
            user=self.user,
            user_identifier=self.user.username,
            section=self.section,
            topic=self.topic,
            score=8,
            total_questions=10
        )
        
        result = get_learning_progress_summary(self.user)
        topic_id = list(result['mastery_levels'].keys())[0]
        
        self.assertEqual(result['mastery_levels'][topic_id]['level'], 'Mastered')
    
    def test_mastery_level_proficient(self):
        """Test that 60-79% accuracy gets 'Proficient' label"""
        QuizAttempt.objects.create(
            user=self.user,
            user_identifier=self.user.username,
            section=self.section,
            topic=self.topic,
            score=7,
            total_questions=10
        )
        
        result = get_learning_progress_summary(self.user)
        topic_id = list(result['mastery_levels'].keys())[0]
        
        self.assertEqual(result['mastery_levels'][topic_id]['level'], 'Proficient')
    
    def test_mastery_level_developing(self):
        """Test that 40-59% accuracy gets 'Developing' label"""
        QuizAttempt.objects.create(
            user=self.user,
            user_identifier=self.user.username,
            section=self.section,
            topic=self.topic,
            score=5,
            total_questions=10
        )
        
        result = get_learning_progress_summary(self.user)
        topic_id = list(result['mastery_levels'].keys())[0]
        
        self.assertEqual(result['mastery_levels'][topic_id]['level'], 'Developing')
    
    def test_mastery_level_beginning(self):
        """Test that <40% accuracy gets 'Beginning' label"""
        QuizAttempt.objects.create(
            user=self.user,
            user_identifier=self.user.username,
            section=self.section,
            topic=self.topic,
            score=3,
            total_questions=10
        )
        
        result = get_learning_progress_summary(self.user)
        topic_id = list(result['mastery_levels'].keys())[0]
        
        self.assertEqual(result['mastery_levels'][topic_id]['level'], 'Beginning')


class TestGetMaterialEffectiveness(TestCase):
    """Test get_material_effectiveness function"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser7', password='testpass')
        self.section = Section.objects.create(name='Section', description='Test')
        self.topic = Topic.objects.create(section=self.section, name='Topic', description='Test')
        self.material = StudyMaterial.objects.create(
            topic=self.topic,
            title='Test Material',
            content_text='Test content'
        )
    
    def test_no_data_returns_no_data_label(self):
        """Test that no attempts returns 'No Data' label"""
        result = get_material_effectiveness(self.material)
        
        self.assertEqual(result['effectiveness_label'], 'No Data')
        self.assertEqual(result['total_attempts'], 0)
    
    def test_highly_effective_label(self):
        """Test highly effective label"""
        # Create attempts with high impact
        calculate_impact_score(
            self.user, self.material,
            before_score=3, before_total=10,
            after_score=8, after_total=10
        )
        
        result = get_material_effectiveness(self.material)
        
        self.assertEqual(result['effectiveness_label'], 'Highly Effective')
    
    def test_moderate_label(self):
        """Test moderate effectiveness label"""
        calculate_impact_score(
            self.user, self.material,
            before_score=3, before_total=10,
            after_score=5, after_total=10
        )
        
        result = get_material_effectiveness(self.material)
        
        self.assertEqual(result['effectiveness_label'], 'Moderate')
    
    def test_includes_min_max_impact(self):
        """Test that min and max impact are included"""
        # Create multiple attempts
        calculate_impact_score(
            self.user, self.material,
            before_score=3, before_total=10,
            after_score=5, after_total=10  # +20%
        )
        
        result = get_material_effectiveness(self.material)
        
        self.assertIn('min_impact', result)
        self.assertIn('max_impact', result)


class TestConceptBasedRecommendations(TestCase):
    """Test get_concept_based_recommendations function"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser8', password='testpass')
        self.section = Section.objects.create(name='Section', description='Test')
        self.topic = Topic.objects.create(section=self.section, name='Topic', description='Test')
        
        # Create concept tags
        self.concept1 = ConceptTag.objects.create(name='Carbon Cycle', description='Test')
        self.concept2 = ConceptTag.objects.create(name='Biodiversity', description='Test')
        
        # Create materials with concepts
        self.material1 = StudyMaterial.objects.create(
            topic=self.topic,
            title='Material 1',
            content_text='Content 1'
        )
        self.material1.concept_tags.add(self.concept1)
        
        self.material2 = StudyMaterial.objects.create(
            topic=self.topic,
            title='Material 2',
            content_text='Content 2'
        )
        self.material2.concept_tags.add(self.concept1, self.concept2)
    
    def test_returns_related_concept_materials(self):
        """Test that related concept materials are returned"""
        # Get materials for topic2 that share concepts with topic1
        topic2 = Topic.objects.create(section=self.section, name='Topic 2', description='Test')
        material3 = StudyMaterial.objects.create(
            topic=topic2,
            title='Material 3',
            content_text='Content 3'
        )
        material3.concept_tags.add(self.concept1)  # Shares concept
        
        recommendations = get_concept_based_recommendations(self.user, topic2)
        
        self.assertTrue(len(recommendations) > 0)
    
    def test_exclude_topic_works(self):
        """Test that exclude_topic parameter works"""
        recommendations = get_concept_based_recommendations(
            self.user, self.topic, exclude_topic=True
        )
        
        # Should not include materials from the same topic
        for rec in recommendations:
            self.assertNotEqual(rec, self.material1)
    
    def test_respects_limit(self):
        """Test that limit parameter is respected"""
        recommendations = get_concept_based_recommendations(
            self.user, self.topic, limit=2
        )
        
        self.assertLessEqual(len(recommendations), 2)
