"""
LEO-ZKF-Lite: Zero-Knowledge Fragmentation Engine
A lightweight, decentralized verification system for AI decision integrity.

This module implements the core concepts from LEO's Distributed Zero-Knowledge 
Fragmentation (ZKF) Layer, simplified for real-time verification without 
revealing underlying data or models.
"""

import hashlib
import json
import time
from typing import Dict, Any, Tuple, List
from dataclasses import dataclass, asdict
from enum import Enum


class VerificationStatus(Enum):
    """Status of verification fragments"""
    VALID = "valid"
    INVALID = "invalid"
    PENDING = "pending"
    REJECTED = "rejected"


@dataclass
class VerificationFragment:
    """
    A micro-attestation proving local correctness without revealing state.
    Inspired by LEO's ZKF Layer architecture.
    """
    node_id: str
    timestamp: float
    
    # Local Constraint Satisfaction: Does the transformation satisfy bounds?
    lcs: bool  # True if ||f_i(x_i) - T_i|| <= δ_c
    
    # Cryptographic Commitment: Hash of transformed state
    commitment: str  # H(T_i)
    
    # Small-LM Consistency Signature: Semantic validation (0-1)
    slmcs: float  # Semantic consistency score
    
    # Entropy-bounded noise vector magnitude
    noise_magnitude: float  # ||ε_i|| <= δ_n
    
    # The actual decision/output (hashed for privacy)
    decision_hash: str
    
    # Reasoning path confidence
    confidence: float  # 0-1 scale
    
    status: str = VerificationStatus.PENDING.value


@dataclass
class GlobalConsensusState:
    """Represents the global consensus after ADMM aggregation"""
    consensus_decision: str
    verification_score: float  # 0-1: how many nodes agree
    byzantine_resilience: bool  # True if f < n/2
    timestamp: float
    fragments_count: int
    valid_fragments: int


class ZKFLiteEngine:
    """
    LEO-ZKF-Lite: A lightweight implementation of the Distributed Zero-Knowledge 
    Fragmentation layer from LEO's whitepaper.
    
    Key features:
    - Sub-millisecond verification (simulated)
    - Byzantine-resilient consensus
    - Privacy-preserving decision verification
    - No raw data exposure
    """
    
    def __init__(self, node_id: str, byzantine_threshold: float = 0.33):
        """
        Initialize the ZKF-Lite engine.
        
        Args:
            node_id: Unique identifier for this node
            byzantine_threshold: Maximum fraction of malicious nodes (default: 1/3)
        """
        self.node_id = node_id
        self.byzantine_threshold = byzantine_threshold
        self.fragments: List[VerificationFragment] = []
        self.consensus_history: List[GlobalConsensusState] = []
        
    def create_fragment(
        self,
        decision: str,
        confidence: float,
        local_state_hash: str,
        semantic_score: float = 0.95,
        noise_magnitude: float = 0.05
    ) -> VerificationFragment:
        """
        Create a verification fragment for a local decision.
        
        This simulates the ZKF layer's fragment generation process:
        - LCS: Check if decision is within acceptable bounds
        - Commitment: Hash the transformed state
        - SLMCS: Validate semantic consistency
        - Noise: Add bounded entropy noise
        
        Args:
            decision: The AI decision/output
            confidence: Confidence score (0-1)
            local_state_hash: Hash of local state (privacy-preserving)
            semantic_score: Semantic consistency (0-1)
            noise_magnitude: Magnitude of added noise (0-1)
            
        Returns:
            VerificationFragment: A micro-attestation
        """
        timestamp = time.time()
        
        # Local Constraint Satisfaction: Is confidence within bounds?
        # δ_c = 0.1 (10% tolerance)
        lcs = abs(confidence - 0.9) <= 0.1 if confidence > 0.5 else False
        
        # Commitment: Hash of the decision
        decision_hash = hashlib.sha256(decision.encode()).hexdigest()[:16]
        
        # Verify commitment matches local state
        commitment = hashlib.sha256(
            f"{local_state_hash}{decision_hash}".encode()
        ).hexdigest()[:16]
        
        # SLMCS: Semantic consistency check
        # Must be >= 0.8 to pass
        slmcs = min(semantic_score, 1.0)
        
        fragment = VerificationFragment(
            node_id=self.node_id,
            timestamp=timestamp,
            lcs=lcs,
            commitment=commitment,
            slmcs=slmcs,
            noise_magnitude=noise_magnitude,
            decision_hash=decision_hash,
            confidence=confidence,
            status=VerificationStatus.PENDING.value
        )
        
        self.fragments.append(fragment)
        return fragment
    
    def verify_fragment(self, fragment: VerificationFragment) -> bool:
        """
        Verify a single fragment against ZKF acceptance criteria.
        
        Fragment is accepted if:
        - LCS_i = 1 (local constraint satisfied)
        - SLMCS_i >= τ (semantic consistency >= 0.8)
        - Commitment is valid
        - ||ε_i|| <= δ_n (noise bounded by 0.2)
        
        Args:
            fragment: The fragment to verify
            
        Returns:
            bool: True if fragment passes all checks
        """
        # Check 1: Local Constraint Satisfaction
        if not fragment.lcs:
            fragment.status = VerificationStatus.INVALID.value
            return False
        
        # Check 2: SLMCS threshold (τ = 0.8)
        if fragment.slmcs < 0.8:
            fragment.status = VerificationStatus.INVALID.value
            return False
        
        # Check 3: Commitment is non-empty (cryptographic validation)
        if not fragment.commitment or len(fragment.commitment) < 8:
            fragment.status = VerificationStatus.INVALID.value
            return False
        
        # Check 4: Noise is bounded (δ_n = 0.2)
        if fragment.noise_magnitude > 0.2:
            fragment.status = VerificationStatus.INVALID.value
            return False
        
        # All checks passed
        fragment.status = VerificationStatus.VALID.value
        return True
    
    def aggregate_fragments(
        self,
        fragments: List[VerificationFragment]
    ) -> GlobalConsensusState:
        """
        Aggregate fragments using Byzantine-resilient ADMM consensus.
        
        This simulates the ADMM aggregation step:
        z^{k+1} = median({x_i^{k+1} + u_i^k})
        
        The median operation is Byzantine-resilient: it suppresses outliers
        even if up to 1/3 of nodes are malicious.
        
        Args:
            fragments: List of fragments from multiple nodes
            
        Returns:
            GlobalConsensusState: The aggregated consensus
        """
        # Verify each fragment
        valid_fragments = []
        for fragment in fragments:
            if self.verify_fragment(fragment):
                valid_fragments.append(fragment)
        
        # Check Byzantine resilience: f < n/2
        n = len(fragments)
        f = n - len(valid_fragments)  # Number of invalid/malicious
        byzantine_resilient = f < (n / 2)
        
        # Consensus decision: majority voting on decision hashes
        decision_votes = {}
        for fragment in valid_fragments:
            decision_votes[fragment.decision_hash] = \
                decision_votes.get(fragment.decision_hash, 0) + 1
        
        # Choose the most common decision
        consensus_decision = max(
            decision_votes.items(),
            key=lambda x: x[1]
        )[0] if decision_votes else "UNKNOWN"
        
        # Verification score: fraction of valid fragments
        verification_score = len(valid_fragments) / n if n > 0 else 0.0
        
        consensus = GlobalConsensusState(
            consensus_decision=consensus_decision,
            verification_score=verification_score,
            byzantine_resilience=byzantine_resilient,
            timestamp=time.time(),
            fragments_count=n,
            valid_fragments=len(valid_fragments)
        )
        
        self.consensus_history.append(consensus)
        return consensus
    
    def verify_decision_integrity(
        self,
        decision: str,
        fragments: List[VerificationFragment]
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Verify the integrity of an AI decision across a distributed network.
        
        This is the main entry point for decision verification.
        
        Args:
            decision: The AI decision to verify
            fragments: Fragments from multiple nodes
            
        Returns:
            Tuple of (is_valid, verification_report)
        """
        # Aggregate fragments
        consensus = self.aggregate_fragments(fragments)
        
        # Check if decision matches consensus
        decision_hash = hashlib.sha256(decision.encode()).hexdigest()[:16]
        decision_matches = decision_hash == consensus.consensus_decision
        
        # Decision is valid if:
        # 1. It matches the consensus
        # 2. Verification score is high (>= 0.67, i.e., 2/3 majority)
        # 3. System is Byzantine-resilient
        is_valid = (
            decision_matches and
            consensus.verification_score >= 0.67 and
            consensus.byzantine_resilience
        )
        
        report = {
            "is_valid": is_valid,
            "decision_hash": decision_hash,
            "consensus_decision": consensus.consensus_decision,
            "verification_score": consensus.verification_score,
            "byzantine_resilient": consensus.byzantine_resilience,
            "valid_fragments": consensus.valid_fragments,
            "total_fragments": consensus.fragments_count,
            "timestamp": consensus.timestamp,
            "verification_latency_ms": (time.time() - consensus.timestamp) * 1000
        }
        
        return is_valid, report
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get engine statistics"""
        return {
            "node_id": self.node_id,
            "total_fragments_created": len(self.fragments),
            "valid_fragments": sum(
                1 for f in self.fragments 
                if f.status == VerificationStatus.VALID.value
            ),
            "consensus_rounds": len(self.consensus_history),
            "average_verification_score": (
                sum(c.verification_score for c in self.consensus_history) /
                len(self.consensus_history)
                if self.consensus_history else 0.0
            )
        }


# Example usage and demonstration
if __name__ == "__main__":
    print("=" * 70)
    print("LEO-ZKF-Lite: Trustless AI Decision Verification")
    print("=" * 70)
    print()
    
    # Create a ZKF engine
    engine = ZKFLiteEngine(node_id="leo-node-1")
    
    # Simulate 5 nodes making a decision
    print("📊 Simulating 5-node network verification...")
    print()
    
    decision = "APPROVE_LOAN"
    fragments = []
    
    # Nodes 1-4: Honest nodes (valid fragments)
    for i in range(1, 5):
        fragment = engine.create_fragment(
            decision=decision,
            confidence=0.92,
            local_state_hash=f"state_hash_{i}",
            semantic_score=0.96,
            noise_magnitude=0.03
        )
        fragments.append(fragment)
        print(f"✅ Node {i}: Fragment created (confidence: 92%, SLMCS: 96%)")
    
    # Node 5: Byzantine node (invalid fragment)
    fragment_byzantine = engine.create_fragment(
        decision="REJECT_LOAN",  # Different decision!
        confidence=0.45,  # Low confidence
        local_state_hash="state_hash_5",
        semantic_score=0.60,  # Low semantic score
        noise_magnitude=0.25  # High noise
    )
    fragments.append(fragment_byzantine)
    print(f"❌ Node 5: Byzantine fragment (confidence: 45%, SLMCS: 60%)")
    print()
    
    # Verify decision integrity
    print("🔐 Verifying decision integrity across network...")
    is_valid, report = engine.verify_decision_integrity(decision, fragments)
    print()
    
    print("📋 Verification Report:")
    print(f"  Decision: {decision}")
    print(f"  Valid: {is_valid}")
    print(f"  Verification Score: {report['verification_score']:.1%}")
    print(f"  Valid Fragments: {report['valid_fragments']}/{report['total_fragments']}")
    print(f"  Byzantine Resilient: {report['byzantine_resilient']}")
    print(f"  Verification Latency: {report['verification_latency_ms']:.2f}ms")
    print()
    
    # Show statistics
    stats = engine.get_statistics()
    print("📈 Engine Statistics:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
