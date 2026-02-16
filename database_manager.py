# FAQ DATABASE MANAGER - Handles all FAQ-related operations
import json
import os
from typing import Dict, List, Tuple

class FAQDatabase:
    """Manages FAQ data with custom university-specific questions"""
    
    def __init__(self):
        self.faqs = self._initialize_faqs()
    
    @staticmethod
    def _initialize_faqs() -> Dict[str, str]:
        """Create custom university FAQ database"""
        return {
            # ENROLLMENT & ADMISSION
            "How can I enroll in courses?": "You can enroll through the student portal during registration week each semester.",
            "What documents are needed for admission?": "Marks cards, ID proof, photographs, and application form are required for admission.",
            "What is the minimum attendance required?": "Minimum 75 percent attendance is mandatory for all students.",
            "When are exams conducted?": "Exams are conducted at the end of each semester, typically after 24 weeks of classes.",
            
            # ACADEMIC RESOURCES
            "What facilities are available on campus?": "Library, computing labs, hostel, sports ground, medical center, and recreation facilities.",
            "What are library timings?": "Library is open from 9 AM to 8 PM on weekdays and 10 AM to 6 PM on weekends.",
            "Is WiFi available on campus?": "Yes, free high-speed WiFi is available throughout the campus.",
            "How to access student portal?": "Login using your student ID and password on the main website portal.",
            
            # HOSTEL SERVICES
            "Is hostel available?": "Yes, hostel is available for both boys and girls with comfortable accommodation.",
            "How to apply for hostel?": "Apply through the hostel application form available on the student portal.",
            "Is hostel food provided?": "Yes, mess facility provides breakfast, lunch, dinner and snacks daily.",
            "What are hostel room types?": "Single, Double, and Triple occupancy rooms are available with modern amenities.",
            
            # FINANCIAL & FEES
            "How to pay college fees?": "Fees can be paid online through the portal, bank transfer, or at the fee collection desk.",
            "Are scholarships available?": "Yes, merit-based and need-based scholarships are provided to eligible students.",
            "How to apply for financial aid?": "Submit financial aid form on the university website during application period.",
            
            # PLACEMENT & CAREER
            "Is placement support available?": "Yes, placement and training cell assists students with internships and job placements.",
            "Are internships available?": "Yes, students get internship opportunities during summer and final year.",
            "What is average placement percentage?": "Our university has 98% placement rate with average CTC of 8-12 LPA.",
            
            # CAMPUS LIFE
            "Is sports facility available?": "Yes, various indoor and outdoor sports facilities with professional coaching available.",
            "Is medical facility available?": "Yes, campus has medical center with doctors and emergency services.",
            "What courses are offered?": "Engineering, Data Science, Business Administration, and various postgraduate programs.",
            
            # STUDENT SERVICES
            "How to get ID card?": "ID card is automatically issued to all students during the orientation week.",
            "Is counseling support available?": "Yes, counseling services are provided for academic and personal guidance.",
            "How to contact administration?": "Email admin@gmucollege.edu or visit the main office during office hours.",
            "What are college working hours?": "College operates from 9 AM to 4 PM on weekdays.",
            
            # ACADEMIC SUPPORT
            "Is there research facility?": "Yes, well-equipped laboratories support student and faculty research work.",
            "How to submit assignments?": "Assignments can be submitted online through portal or in-class as specified by professors.",
            "Are workshops conducted?": "Yes, regular technical and soft skills workshops are conducted throughout the year.",
            "What is exam passing criteria?": "Minimum 40 percent marks is required to pass each semester examination."
        }
    
    def get_all_faqs(self) -> Dict[str, str]:
        """Get all FAQ pairs"""
        return self.faqs.copy()
    
    def get_questions_list(self) -> List[str]:
        """Get list of all questions"""
        return list(self.faqs.keys())
    
    def get_answers_list(self) -> List[str]:
        """Get list of all answers"""
        return list(self.faqs.values())
    
    def add_faq(self, question: str, answer: str) -> bool:
        """Add new FAQ pair"""
        if question and answer:
            self.faqs[question] = answer
            return True
        return False
    
    def get_faq_count(self) -> int:
        """Get total number of FAQs"""
        return len(self.faqs)


class AnalyticsManager:
    """Manages user interaction analytics"""
    
    ANALYTICS_FILE = "analytics_data.json"
    
    @staticmethod
    def initialize_analytics() -> Dict:
        """Initialize analytics data structure"""
        return {
            "total_queries": 0,
            "high_confidence": 0,
            "low_confidence": 0,
            "learned_answers": 0,
            "top_questions": {},
            "user_feedback": []
        }
    
    @staticmethod
    def load_analytics() -> Dict:
        """Load analytics from file"""
        if os.path.exists(AnalyticsManager.ANALYTICS_FILE):
            with open(AnalyticsManager.ANALYTICS_FILE, 'r') as f:
                return json.load(f)
        return AnalyticsManager.initialize_analytics()
    
    @staticmethod
    def save_analytics(data: Dict) -> None:
        """Save analytics to file"""
        with open(AnalyticsManager.ANALYTICS_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    
    @staticmethod
    def record_query(analytics: Dict, query: str) -> None:
        """Record a user query"""
        analytics["total_queries"] += 1
        if query not in analytics["top_questions"]:
            analytics["top_questions"][query] = 0
        analytics["top_questions"][query] += 1
    
    @staticmethod
    def record_confidence(analytics: Dict, confidence: float) -> None:
        """Record answer confidence"""
        if confidence >= 0.5:
            analytics["high_confidence"] += 1
        else:
            analytics["low_confidence"] += 1
    
    @staticmethod
    def record_feedback(analytics: Dict, query: str, rating: str) -> None:
        """Record user feedback"""
        analytics["user_feedback"].append({"query": query, "rating": rating})
    
    @staticmethod
    def add_learned_answer(analytics: Dict) -> None:
        """Increment learned answers count"""
        analytics["learned_answers"] += 1
    
    @staticmethod
    def get_top_questions(analytics: Dict, limit: int = 10) -> List[Tuple[str, int]]:
        """Get top asked questions"""
        sorted_q = sorted(analytics["top_questions"].items(), key=lambda x: x[1], reverse=True)
        return sorted_q[:limit]
    
    @staticmethod
    def get_feedback_summary(analytics: Dict) -> Dict:
        """Get feedback summary"""
        feedback = analytics["user_feedback"]
        return {
            "helpful": sum(1 for f in feedback if f["rating"] == "helpful"),
            "somewhat": sum(1 for f in feedback if f["rating"] == "somewhat"),
            "not_helpful": sum(1 for f in feedback if f["rating"] == "not_helpful")
        }
