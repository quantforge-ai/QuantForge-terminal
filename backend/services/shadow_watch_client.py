# backend/services/shadow_watch_client.py
"""
Shadow Watch Package Integration Wrapper
Maintains API compatibility with existing QuantForge code
while using the PyPI shadowwatch package

This wrapper allows gradual migration:
- Old code continues to work
- New code uses package directly
- Easy to update incrementally
"""

from typing import Dict, Optional
from backend.core.logger import log

# Global Shadow Watch instance (initialized in main.py)
_shadow_watch_instance = None


def set_shadow_watch_instance(instance):
    """
    Set the global Shadow Watch instance
    Called from main.py during startup
    """
    global _shadow_watch_instance
    _shadow_watch_instance = instance
    log.info("✅ Shadow Watch client wrapper configured")


def get_shadow_watch():
    """Get the global Shadow Watch instance"""
    if _shadow_watch_instance is None:
        log.warning("⚠️ Shadow Watch not initialized! Call set_shadow_watch_instance first")
    return _shadow_watch_instance


# ============================================================================
# COMPATIBILITY FUNCTIONS - Match old API exactly
# ============================================================================

async def track_activity(
    user_id: int,
    symbol: str,
   action: str,
    event_metadata: Optional[Dict] = None
):
    """
    Track user activity (compatibility wrapper)
    
    Maps old API:
        track_activity(user_id, symbol, action, event_metadata)
    
    To new package API:
        sw.track(user_id, entity_id, action, metadata)
    """
    sw = get_shadow_watch()
    if sw:
        try:
            await sw.track(
                user_id=user_id,
                entity_id=symbol,  # symbol → entity_id
                action=action,
                metadata=event_metadata  # event_metadata → metadata
            )
        except Exception as e:
            log.error(f"❌ Shadow Watch tracking error: {e}")


async def generate_library_snapshot(user_id: int) -> Dict:
    """
    Generate library snapshot (compatibility wrapper)
    
    Maps old API:
        generate_library_snapshot(user_id) → {...}
    
    To new package API:
        sw.get_profile(user_id) → {...}
    """
    sw = get_shadow_watch()
    if sw:
        try:
            return await sw.get_profile(user_id)
        except Exception as e:
            log.error(f"❌ Shadow Watch profile error: {e}")
            return _empty_profile()
    return _empty_profile()


async def calculate_trust_score(user_id: int, request_context: Dict) -> Dict:
    """
    Calculate trust score (compatibility wrapper)
    
    Maps old API:
        calculate_trust_score(user_id, request_context) → {...}
    
    To new package API:
        sw.verify_login(user_id, request_context) → {...}
    """
    sw = get_shadow_watch()
    if sw:
        try:
            return await sw.verify_login(user_id, request_context)
        except Exception as e:
            log.error(f"❌ Shadow Watch trust score error: {e}")
            return _default_trust_score()
    return _default_trust_score()


async def generate_recovery_file(user_id: int) -> Dict:
    """
    Generate recovery file (compatibility wrapper)
    
    Note: Package may have different recovery API
    Check shadowwatch documentation
    """
    sw = get_shadow_watch()
    if sw:
        try:
            # TODO: Check if package has recovery file generation
            # May need to call sw.get_profile() and format manually
            profile = await sw.get_profile(user_id)
            return {
                "filename": f"shadow_watch_recovery_{user_id}.json",
                "content": profile,
                "recovery_code": "NOT_IMPLEMENTED"
            }
        except Exception as e:
            log.error(f"❌ Shadow Watch recovery error: {e}")
    return {}


async def export_user_data(user_id: int) -> Dict:
    """
    Export user data for GDPR (compatibility wrapper)
    """
    sw = get_shadow_watch()
    if sw:
        try:
            # Package likely has export functionality
            # For now, return profile
            profile = await sw.get_profile(user_id)
            return {
                "exported_at": "2026-01-11",  # TODO: Use datetime
                "user_id": user_id,
                "shadow_watch_data": profile
            }
        except Exception as e:
            log.error(f"❌ Shadow Watch export error: {e}")
    return {}


async def delete_user_data(user_id: int) -> Dict:
    """
    Delete user data for GDPR (compatibility wrapper)
    """
    sw = get_shadow_watch()
    if sw:
        try:
            # Package should have delete functionality
            # Check documentation for exact method
            log.warning(f"⚠️ Delete user data not yet implemented in wrapper")
            return {
                "success": False,
                "message": "Delete functionality needs package API mapping"
            }
        except Exception as e:
            log.error(f"❌ Shadow Watch delete error: {e}")
    return {"success": False, "message": str(e)}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _empty_profile() -> Dict:
    """Return empty profile structure"""
    return {
        "version": 0,
        "total_items": 0,
        "pinned_count": 0,
        "fingerprint": "",
        "library": []
    }


def _default_trust_score() -> Dict:
    """Return default trust score (neutral)"""
    return {
        "trust_score": 0.7,
        "risk_level": "medium",
        "action": "monitor",
        "factors": {}
    }
