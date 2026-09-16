import re


class InsightEDTranslator:
    """
    Converts raw ML/XAI feature names into understandable explanations
    and actionable pedagogical recommendations.
    """

    @staticmethod
    def extract_feature_name(feature_str):
        """
        Extract the actual feature name from a LIME rule.

        Example:
        '-0.79 < G2 <= 0.16' -> 'G2'
        'age <= -0.59' -> 'age'
        """
        feature_str = str(feature_str)

        feature_names = [
            'Grade_Momentum',
            'absences',
            'studytime',
            'failures',
            'freetime',
            'goout',
            'traveltime',
            'health',
            'Medu',
            'Fedu',
            'G1',
            'G2',
            'age'
        ]

        # Check longer names first
        for feature in sorted(feature_names, key=len, reverse=True):
            if re.search(r'\b' + re.escape(feature) + r'\b', feature_str):
                return feature

        # Fallback: remove numbers and comparison operators
        clean_name = re.sub(
            r'[-+]?\d*\.?\d+|<=|>=|==|!=|<|>',
            '',
            feature_str
        ).strip()

        return clean_name

    @staticmethod
    def translate_feature_name(feature_str):
        """
        Convert raw feature/XAI rule into a readable title.
        """

        clean_name = InsightEDTranslator.extract_feature_name(feature_str)

        name_map = {
            'G1': 'First Period Grade (G1)',
            'G2': 'Second Period Grade (G2)',
            'Grade_Momentum': 'Academic Trend (G2 - G1)',
            'absences': 'Class Absences Count',
            'failures': 'Past Academic Failures',
            'studytime': 'Weekly Study Time',
            'freetime': 'Free Time After Campus',
            'goout': 'Social Activity Frequency',
            'Medu': "Mother's Education Level",
            'Fedu': "Father's Education Level",
            'health': 'Current Health Status',
            'traveltime': 'Campus Travel Duration',
            'age': 'Student Age'
        }

        return name_map.get(clean_name, clean_name)

    @staticmethod
    def get_actionable_recommendation(feature_str, rule_weight):
        """
        Convert an XAI feature into a human-readable reason
        and pedagogical action.
        """

        clean_key = InsightEDTranslator.extract_feature_name(feature_str)

        recommendation_matrix = {

            'G2': {
                'reason': (
                    "The student's second-period academic performance "
                    "is associated with the predicted risk."
                ),
                'action': (
                    "Provide targeted remedial tutorials or assign "
                    "a peer mentor before the final assessment."
                )
            },

            'G1': {
                'reason': (
                    "The student's first-period academic performance "
                    "indicates an early performance concern."
                ),
                'action': (
                    "Conduct a fundamental concept review and "
                    "identify learning gaps."
                )
            },

            'Grade_Momentum': {
                'reason': (
                    "The student's academic performance has changed "
                    "between the two assessment periods."
                ),
                'action': (
                    "Schedule an academic progress review to discuss "
                    "the performance trend."
                )
            },

            'absences': {
                'reason': (
                    "The student's recorded absences are contributing "
                    "to the predicted academic risk."
                ),
                'action': (
                    "Review attendance patterns and identify possible "
                    "barriers affecting class participation."
                )
            },

            'failures': {
                'reason': (
                    "The student has previous academic failures "
                    "associated with increased academic risk."
                ),
                'action': (
                    "Provide structured weekly check-ins, revision "
                    "support, and practice assessments."
                )
            },

            'studytime': {
                'reason': (
                    "The student's reported study-time level is "
                    "associated with the predicted risk."
                ),
                'action': (
                    "Recommend a structured study schedule and "
                    "guided academic study sessions."
                )
            },

            'freetime': {
                'reason': (
                    "The student's available free-time pattern "
                    "may be associated with the prediction."
                ),
                'action': (
                    "Discuss time management and establish a "
                    "balanced academic routine."
                )
            },

            'goout': {
                'reason': (
                    "The student's social-activity frequency is "
                    "associated with the prediction."
                ),
                'action': (
                    "Discuss time management and balancing social "
                    "activities with academic responsibilities."
                )
            },

            'age': {
                'reason': (
                    "Age is being used by the trained model as "
                    "one of the predictive variables."
                ),
                'action': (
                    "Consider the student's overall academic context "
                    "rather than using age alone to guide intervention."
                )
            }
        }

        fallback = {
            'reason': (
                f"The model identified {clean_key} as an influential "
                "predictive feature."
            ),
            'action': (
                "Monitor the student's academic engagement and "
                "review their progress during upcoming assessments."
            )
        }

        return recommendation_matrix.get(clean_key, fallback)