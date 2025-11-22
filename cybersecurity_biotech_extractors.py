# cybersecurity_biotech_extractors.py
"""
Cybersecurity & Biotechnology Knowledge Extractors
Advanced knowledge integration for security and health domains
"""
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

class EnhancedIntegratedKnowledgeExtractor:
    """Advanced knowledge extraction for cybersecurity and biotechnology domains"""
    
    def __init__(self):
        self.name = "Enhanced Integrated Knowledge Extractor"
        self.version = "1.0.0"
        self.domains = ["cybersecurity", "biotechnology", "health_sovereignty", "digital_biology"]
        
        # Initialize extraction patterns
        self.cybersecurity_patterns = {
            "threats": [
                r"\b(malware|virus|trojan|ransomware|phishing|ddos|breach|attack)\b",
                r"\b(vulnerability|exploit|backdoor|botnet|spyware|rootkit)\b",
                r"\b(firewall|encryption|authentication|authorization|ssl|tls)\b"
            ],
            "technologies": [
                r"\b(blockchain|cryptography|quantum|zero-trust|ai-security)\b",
                r"\b(penetration|testing|vulnerability|assessment|siem|soc)\b",
                r"\b(endpoint|detection|response|threat|intelligence)\b"
            ]
        }
        
        self.biotech_patterns = {
            "biological_systems": [
                r"\b(dna|rna|protein|enzyme|genetic|genome|chromosome)\b",
                r"\b(cell|tissue|organ|organism|metabolic|pathway)\b",
                r"\b(bioengineering|synthetic|biology|crispr|gene|therapy)\b"
            ],
            "health_metrics": [
                r"\b(biomarker|diagnostic|therapeutic|treatment|drug|medicine)\b",
                r"\b(immune|system|antibody|antigen|pathogen|bacteria|virus)\b",
                r"\b(health|wellness|longevity|prevention|nutrition|fitness)\b"
            ]
        }
        
        self.extraction_history = []
        
    def extract_cybersecurity_knowledge(self, data: str) -> Dict:
        """Extract cybersecurity knowledge from text data"""
        extraction = {
            "domain": "cybersecurity",
            "timestamp": datetime.now().isoformat(),
            "threats_identified": [],
            "technologies_found": [],
            "security_concepts": [],
            "risk_assessments": []
        }
        
        text_lower = data.lower()
        
        # Extract threats
        for pattern_group in self.cybersecurity_patterns["threats"]:
            matches = re.findall(pattern_group, text_lower)
            extraction["threats_identified"].extend(matches)
            
        # Extract technologies
        for pattern_group in self.cybersecurity_patterns["technologies"]:
            matches = re.findall(pattern_group, text_lower)
            extraction["technologies_found"].extend(matches)
            
        # Generate security concepts
        extraction["security_concepts"] = self._generate_security_concepts(
            extraction["threats_identified"], 
            extraction["technologies_found"]
        )
        
        # Assess risk levels
        extraction["risk_assessments"] = self._assess_security_risks(extraction)
        
        # Remove duplicates
        extraction["threats_identified"] = list(set(extraction["threats_identified"]))
        extraction["technologies_found"] = list(set(extraction["technologies_found"]))
        
        return extraction
        
    def extract_biotechnology_knowledge(self, data: str) -> Dict:
        """Extract biotechnology and health knowledge from text data"""
        extraction = {
            "domain": "biotechnology",
            "timestamp": datetime.now().isoformat(),
            "biological_systems": [],
            "health_metrics": [],
            "biotech_concepts": [],
            "health_insights": []
        }
        
        text_lower = data.lower()
        
        # Extract biological systems
        for pattern_group in self.biotech_patterns["biological_systems"]:
            matches = re.findall(pattern_group, text_lower)
            extraction["biological_systems"].extend(matches)
            
        # Extract health metrics
        for pattern_group in self.biotech_patterns["health_metrics"]:
            matches = re.findall(pattern_group, text_lower)
            extraction["health_metrics"].extend(matches)
            
        # Generate biotech concepts
        extraction["biotech_concepts"] = self._generate_biotech_concepts(
            extraction["biological_systems"],
            extraction["health_metrics"]
        )
        
        # Generate health insights
        extraction["health_insights"] = self._generate_health_insights(extraction)
        
        # Remove duplicates
        extraction["biological_systems"] = list(set(extraction["biological_systems"]))
        extraction["health_metrics"] = list(set(extraction["health_metrics"]))
        
        return extraction
        
    def integrated_analysis(self, data: str) -> Dict:
        """Perform integrated analysis across cybersecurity and biotechnology"""
        cyber_extraction = self.extract_cybersecurity_knowledge(data)
        bio_extraction = self.extract_biotechnology_knowledge(data)
        
        integrated = {
            "analysis_type": "integrated_cyber_bio",
            "timestamp": datetime.now().isoformat(),
            "cybersecurity": cyber_extraction,
            "biotechnology": bio_extraction,
            "integration_insights": [],
            "convergence_opportunities": [],
            "sovereignty_implications": []
        }
        
        # Generate integration insights
        integrated["integration_insights"] = self._generate_integration_insights(
            cyber_extraction, bio_extraction
        )
        
        # Identify convergence opportunities
        integrated["convergence_opportunities"] = [
            "Bio-inspired cybersecurity algorithms",
            "Digital health sovereignty systems", 
            "Quantum-bio-crypto integration",
            "Immune system network defense",
            "Biometric security enhancement"
        ]
        
        # Sovereignty implications
        integrated["sovereignty_implications"] = [
            "Enhanced digital health autonomy",
            "Secure biological data protection",
            "Sovereign biotechnology infrastructure",
            "Independent health intelligence systems"
        ]
        
        # Store analysis
        self.extraction_history.append(integrated)
        
        return integrated
        
    def _generate_security_concepts(self, threats: List[str], technologies: List[str]) -> List[str]:
        """Generate security concepts from identified threats and technologies"""
        concepts = []
        
        if threats:
            concepts.extend([
                "Threat landscape analysis required",
                "Multi-layered defense strategy needed",
                "Continuous monitoring implementation"
            ])
            
        if technologies:
            concepts.extend([
                "Advanced security technology integration",
                "Zero-trust architecture deployment",
                "AI-powered threat detection"
            ])
            
        return concepts
        
    def _assess_security_risks(self, extraction: Dict) -> List[Dict]:
        """Assess security risk levels based on extraction"""
        risks = []
        
        threat_count = len(extraction["threats_identified"])
        tech_count = len(extraction["technologies_found"])
        
        if threat_count > 5:
            risks.append({
                "level": "HIGH",
                "category": "Multiple Threats",
                "recommendation": "Immediate security assessment required"
            })
        elif threat_count > 2:
            risks.append({
                "level": "MEDIUM", 
                "category": "Moderate Threats",
                "recommendation": "Enhanced monitoring recommended"
            })
        else:
            risks.append({
                "level": "LOW",
                "category": "Minimal Threats",
                "recommendation": "Standard security posture maintained"
            })
            
        return risks
        
    def _generate_biotech_concepts(self, bio_systems: List[str], health_metrics: List[str]) -> List[str]:
        """Generate biotechnology concepts from identified systems and metrics"""
        concepts = []
        
        if bio_systems:
            concepts.extend([
                "Biological system integration analysis",
                "Synthetic biology applications",
                "Genetic engineering considerations"
            ])
            
        if health_metrics:
            concepts.extend([
                "Health optimization strategies",
                "Personalized medicine approaches",
                "Biomarker-driven diagnostics"
            ])
            
        return concepts
        
    def _generate_health_insights(self, extraction: Dict) -> List[str]:
        """Generate health insights from biotechnology extraction"""
        insights = []
        
        bio_count = len(extraction["biological_systems"])
        health_count = len(extraction["health_metrics"])
        
        if bio_count > 3 and health_count > 3:
            insights.extend([
                "Comprehensive health sovereignty approach available",
                "Integrated biological monitoring systems feasible",
                "Advanced personalized health protocols applicable"
            ])
        elif bio_count > 0 or health_count > 0:
            insights.extend([
                "Targeted health optimization opportunities",
                "Specific biological system enhancement possible",
                "Focused health metric improvement available"
            ])
        else:
            insights.append("General health sovereignty maintenance recommended")
            
        return insights
        
    def _generate_integration_insights(self, cyber: Dict, bio: Dict) -> List[str]:
        """Generate insights from integrated cybersecurity and biotechnology analysis"""
        insights = []
        
        # Check for convergence potential
        if cyber["threats_identified"] and bio["biological_systems"]:
            insights.append("Bio-inspired cybersecurity defense patterns identified")
            
        if cyber["technologies_found"] and bio["health_metrics"]:
            insights.append("Digital health security integration opportunities available")
            
        if len(cyber["security_concepts"]) > 2 and len(bio["biotech_concepts"]) > 2:
            insights.append("Comprehensive cyber-bio sovereignty system feasible")
            
        # Default insights
        if not insights:
            insights = [
                "Standard integrated analysis completed",
                "Cross-domain knowledge integration successful",
                "Foundational sovereignty concepts established"
            ]
            
        return insights
        
    def get_extraction_history(self, limit: int = 10) -> List[Dict]:
        """Get recent extraction history"""
        return self.extraction_history[-limit:] if self.extraction_history else []
        
    def get_knowledge_summary(self) -> Dict:
        """Get comprehensive knowledge extraction summary"""
        return {
            "extractor_name": self.name,
            "version": self.version,
            "domains": self.domains,
            "total_extractions": len(self.extraction_history),
            "last_extraction": self.extraction_history[-1]["timestamp"] if self.extraction_history else None,
            "capabilities": [
                "Cybersecurity threat analysis",
                "Biotechnology system extraction",
                "Integrated domain analysis",
                "Health sovereignty insights",
                "Cross-domain pattern recognition"
            ],
            "status": "FULLY_OPERATIONAL"
        }

def get_knowledge_extractor():
    """Get global knowledge extractor instance"""
    return EnhancedIntegratedKnowledgeExtractor()

def extract_integrated_knowledge(data: str):
    """Extract knowledge across cybersecurity and biotechnology domains"""
    extractor = get_knowledge_extractor()
    return extractor.integrated_analysis(data)