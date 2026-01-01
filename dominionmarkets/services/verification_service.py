"""
News Verification Service
==========================
Multi-source verification engine with conflict detection.

Core Functions:
- calculate_verification_score(): Score articles 0-100
- detect_conflicts(): Find factual discrepancies
- extract_key_facts(): NLP-based fact extraction
- calculate_agreement(): Measure source consensus

Last Updated: December 24, 2025
"""

from typing import List, Dict, Tuple, Optional
from datetime import datetime
import re
import json
from collections import defaultdict

from dominionmarkets.models.news import (
    NewsArticle, NewsSource, VerificationCheck, VerificationStatus, NewsTier
)


class VerificationService:
    """
    Core verification engine for news articles.
    """
    
    # Source trust scoring by tier
    TIER_WEIGHTS = {
        'aaa': 1.0,   # 100% weight
        'aa': 0.9,    # 90% weight
        'a': 0.75,    # 75% weight
        'b': 0.6,     # 60% weight
        'c': 0.4      # 40% weight
    }
    
    def __init__(self):
        self.conflict_threshold = 0.15  # 15% disagreement triggers conflict warning
    
    def calculate_verification_score(
        self, 
        article: NewsArticle, 
        sources: List[NewsSource]
    ) -> Tuple[int, Dict]:
        """
        Calculate overall verification score (0-100) based on three components.
        
        Args:
            article: NewsArticle instance
            sources: List of NewsSource instances reporting this story
        
        Returns:
            Tuple of (score: int, breakdown: dict)
        """
        if not sources:
            return 0, {'error': 'No sources provided'}
        
        # Component 1: Source Count Score (0-30 points)
        source_count_score = self._score_source_count(len(sources))
        
        # Component 2: Agreement Score (0-40 points)
        # This requires content analysis - simplified version checks source consistency
        agreement_score, agreement_rate = self._score_agreement(article, sources)
        
        # Component 3: Source Quality Score (0-30 points)
        quality_score = self._score_source_quality(sources)
        
        # Calculate total
        total_score = source_count_score + agreement_score + quality_score
        total_score = min(int(total_score), 100)
        
        # Build breakdown
        breakdown = {
            'source_count_score': source_count_score,
            'source_count_max': 30,
            'agreement_score': agreement_score,
            'agreement_rate': agreement_rate,
            'agreement_max': 40,
            'quality_score': quality_score,
            'quality_max': 30,
            'total_score': total_score,
            'total_max': 100
        }
        
        return total_score, breakdown
    
    def _score_source_count(self, count: int) -> int:
        """
        Score based on number of sources.
        More sources = higher confidence.
        
        Returns: 0-30 points
        """
        if count >= 8:
            return 30
        elif count >= 5:
            return 25
        elif count >= 3:
            return 20
        elif count == 2:
            return 15
        else:
            return 10
    
    def _score_agreement(self, article: NewsArticle, sources: List[NewsSource]) -> Tuple[int, float]:
        """
        Score based on source agreement.
        Uses simple heuristics: title similarity, category matching, etc.
        
        In production, this would use NLP to extract and compare key facts.
        
        Returns: (score: 0-40 points, agreement_rate: 0-100%)
        """
        # Simplified agreement calculation
        # In production: extract key facts (numbers, dates, quotes) and compare
        
        # For now, assume high agreement if multiple sources report similar content
        # This is a placeholder - replace with actual NLP fact extraction
        
        if len(sources) == 1:
            # Can't measure agreement with single source
            return 30, 100.0
        
        # Simulate agreement rate based on source quality
        # Higher-tier sources tend to agree more
        avg_tier_weight = sum(self.TIER_WEIGHTS.get(s.tier.value, 0.5) for s in sources) / len(sources)
        
        # Mock agreement rate (in production: compare extracted facts)
        agreement_rate = 85 + (avg_tier_weight * 10)  # 85-95% range
        
        # Convert agreement rate to score
        if agreement_rate >= 95:
            score = 40
        elif agreement_rate >= 90:
            score = 35
        elif agreement_rate >= 80:
            score = 30
        elif agreement_rate >= 70:
            score = 25
        elif agreement_rate >= 60:
            score = 20
        else:
            score = 15
        
        return score, agreement_rate
    
    def _score_source_quality(self, sources: List[NewsSource]) -> int:
        """
        Score based on source trust ratings.
        Weighted average of source trust scores.
        
        Returns: 0-30 points
        """
        if not sources:
            return 0
        
        # Calculate weighted average trust score
        total_weighted_score = 0
        total_weight = 0
        
        for source in sources:
            tier_weight = self.TIER_WEIGHTS.get(source.tier.value, 0.5)
            weighted_score = (source.trust_score / 100) * tier_weight
            total_weighted_score += weighted_score
            total_weight += tier_weight
        
        avg_quality = (total_weighted_score / total_weight) if total_weight > 0 else 0.5
        
        # Convert to 0-30 scale
        quality_score = int(avg_quality * 30)
        
        return quality_score
    
    def detect_conflicts(
        self, 
        article: NewsArticle, 
        sources: List[NewsSource],
        source_contents: Dict[str, str]
    ) -> List[Dict]:
        """
        Detect factual conflicts between sources.
        
        Args:
            article: NewsArticle instance
            sources: List of NewsSource instances
            source_contents: Dict mapping source_id -> article text
        
        Returns:
            List of conflict dicts with details
        """
        if len(sources) < 2:
            return []  # Need at least 2 sources to detect conflicts
        
        conflicts = []
        
        # Extract numerical claims from each source
        numerical_claims = self._extract_numerical_claims(source_contents)
        
        # Compare claims across sources
        for claim_type, claims_by_source in numerical_claims.items():
            conflict = self._check_claim_consistency(claim_type, claims_by_source, sources)
            if conflict:
                conflicts.append(conflict)
        
        return conflicts
    
    def _extract_numerical_claims(self, source_contents: Dict[str, str]) -> Dict[str, Dict]:
        """
        Extract numerical claims from article text.
        
        Returns:
            Dict mapping claim_type -> {source_id: value}
        """
        claims = defaultdict(dict)
        
        # Patterns for common financial claims
        patterns = {
            'percentage': r'([\d.]+)%',
            'dollar_amount': r'\$([0-9,]+(?:\.[0-9]{2})?)\s*(?:million|billion|trillion)?',
            'shares': r'([0-9,]+)\s*shares?',
            'price_target': r'price target of \$([0-9.]+)',
            'earnings': r'earnings of \$([0-9.]+)',
        }
        
        for source_id, content in source_contents.items():
            for claim_type, pattern in patterns.items():
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    # Store first significant match
                    claims[claim_type][source_id] = matches[0]
        
        return dict(claims)
    
    def _check_claim_consistency(
        self, 
        claim_type: str, 
        claims_by_source: Dict[str, str],
        sources: List[NewsSource]
    ) -> Optional[Dict]:
        """
        Check if claims are consistent across sources.
        
        Returns:
            Conflict dict if inconsistency found, None otherwise
        """
        if len(claims_by_source) < 2:
            return None
        
        # Convert claims to comparable format
        values = []
        source_ids = []
        for source_id, claim_value in claims_by_source.items():
            try:
                # Remove commas and convert to float
                clean_value = float(claim_value.replace(',', ''))
                values.append(clean_value)
                source_ids.append(source_id)
            except (ValueError, AttributeError):
                continue
        
        if len(values) < 2:
            return None
        
        # Calculate variance
        avg_value = sum(values) / len(values)
        max_deviation = max(abs(v - avg_value) / avg_value for v in values) if avg_value > 0 else 0
        
        # Flag as conflict if deviation exceeds threshold
        if max_deviation > self.conflict_threshold:
            # Find which sources disagree most
            disagreeing_sources = []
            for i, value in enumerate(values):
                deviation = abs(value - avg_value) / avg_value if avg_value > 0 else 0
                if deviation > self.conflict_threshold:
                    source = next((s for s in sources if s.id == source_ids[i]), None)
                    if source:
                        disagreeing_sources.append({
                            'source_name': source.name,
                            'source_id': source.id,
                            'value': value,
                            'deviation': round(deviation * 100, 1)
                        })
            
            # Determine severity
            if max_deviation > 0.3:
                severity = 'high'
            elif max_deviation > 0.2:
                severity = 'medium'
            else:
                severity = 'low'
            
            return {
                'type': claim_type,
                'severity': severity,
                'max_deviation': round(max_deviation * 100, 1),
                'average_value': avg_value,
                'disagreeing_sources': disagreeing_sources,
                'description': f"Sources report {claim_type} with {round(max_deviation * 100, 1)}% variance"
            }
        
        return None
    
    def extract_key_facts(self, article_text: str) -> List[Dict]:
        """
        Extract key facts from article text using NLP.
        
        This is a simplified version. In production, use:
        - spaCy for named entity recognition
        - Custom fact extraction models
        - Financial-domain-specific parsers
        
        Returns:
            List of fact dicts: [{'type': 'number', 'value': '5.5%', 'context': '...'}, ...]
        """
        facts = []
        
        # Extract percentages
        for match in re.finditer(r'([\d.]+)%', article_text):
            facts.append({
                'type': 'percentage',
                'value': match.group(1),
                'context': article_text[max(0, match.start()-50):match.end()+50]
            })
        
        # Extract dollar amounts
        for match in re.finditer(r'\$([0-9,]+(?:\.[0-9]{2})?)', article_text):
            facts.append({
                'type': 'dollar_amount',
                'value': match.group(1),
                'context': article_text[max(0, match.start()-50):match.end()+50]
            })
        
        # Extract dates
        for match in re.finditer(r'(\d{1,2}/\d{1,2}/\d{4})', article_text):
            facts.append({
                'type': 'date',
                'value': match.group(1),
                'context': article_text[max(0, match.start()-50):match.end()+50]
            })
        
        return facts
    
    def calculate_source_agreement(
        self, 
        facts_by_source: Dict[str, List[Dict]]
    ) -> float:
        """
        Calculate percentage agreement across sources.
        
        Args:
            facts_by_source: Dict mapping source_id -> list of extracted facts
        
        Returns:
            Agreement rate (0-100%)
        """
        if len(facts_by_source) < 2:
            return 100.0
        
        # Group facts by type
        facts_by_type = defaultdict(list)
        for source_id, facts in facts_by_source.items():
            for fact in facts:
                facts_by_type[fact['type']].append({
                    'source_id': source_id,
                    'value': fact['value']
                })
        
        # Calculate agreement for each fact type
        agreements = []
        for fact_type, fact_list in facts_by_type.items():
            # Simple agreement: if all sources report similar values
            values = [f['value'] for f in fact_list]
            unique_values = set(values)
            agreement_rate = (len(values) - len(unique_values) + 1) / len(values) * 100
            agreements.append(agreement_rate)
        
        # Overall agreement is average across all fact types
        overall_agreement = sum(agreements) / len(agreements) if agreements else 100.0
        
        return round(overall_agreement, 2)
    
    def create_verification_record(
        self,
        session,
        article: NewsArticle,
        check_type: str,
        passed: bool,
        score: Optional[int] = None,
        details: Optional[Dict] = None,
        conflict_data: Optional[Dict] = None
    ) -> VerificationCheck:
        """
        Create a verification check record in the database.
        
        Args:
            session: SQLAlchemy session
            article: NewsArticle instance
            check_type: Type of check ('source_count', 'agreement', 'quality', 'conflict')
            passed: Whether the check passed
            score: Sub-score for this check
            details: Additional details (JSON)
            conflict_data: Conflict information if applicable
        
        Returns:
            VerificationCheck instance
        """
        check = VerificationCheck(
            article_id=article.id,
            check_type=check_type,
            performed_at=datetime.utcnow(),
            passed=passed,
            score=score,
            details=details
        )
        
        if conflict_data:
            check.conflict_severity = conflict_data.get('severity')
            check.conflicting_sources = conflict_data.get('disagreeing_sources', [])
            check.conflict_description = conflict_data.get('description')
        
        session.add(check)
        return check


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_source_tier_label(tier_enum) -> str:
    """Convert tier enum to display label"""
    labels = {
        'aaa': 'AAA (Highest Trust)',
        'aa': 'AA (High Trust)',
        'a': 'A (Good Trust)',
        'b': 'B (Moderate Trust)',
        'c': 'C (Lower Trust)'
    }
    return labels.get(tier_enum.value if hasattr(tier_enum, 'value') else tier_enum, 'Unknown')


def format_verification_badge(score: int) -> Dict[str, str]:
    """
    Get badge display info for verification score.
    
    Returns:
        Dict with 'emoji', 'label', 'color'
    """
    if score >= 90:
        return {'emoji': '✅', 'label': 'Highly Verified', 'color': 'emerald'}
    elif score >= 75:
        return {'emoji': '✅', 'label': 'Verified', 'color': 'green'}
    elif score >= 60:
        return {'emoji': '⚠️', 'label': 'Partially Verified', 'color': 'yellow'}
    else:
        return {'emoji': '❌', 'label': 'Low Verification', 'color': 'red'}
