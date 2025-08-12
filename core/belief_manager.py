# core/belief_manager.py
import asyncio
import logging
import requests
from datetime import datetime

class BeliefManager:
    """Mengelola sistem kepercayaan BDI Agent (Enterprise Grade)."""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.beliefs = {}
        self.sources = {
            "system_health": "https://fmaa-dashboard1.vercel.app/api/health",
            "user_activity": "https://wirecutt-1.vercel.app/api/activity",
            "github_activity": "https://api.github.com/repos/facebook/react/commits?per_page=1"
        }

    async def update_beliefs(self) -> dict:
        self.logger.info("👁️  Departemen Intelijen memulai pengumpulan data...")
        tasks = [self._collect_single_belief(name, url) for name, url in self.sources.items()]
        await asyncio.gather(*tasks)
        self.beliefs['last_update'] = datetime.now().isoformat()
        return self.beliefs

    async def _collect_single_belief(self, name: str, url: str):
        try:
            response = await asyncio.to_thread(requests.get, url, timeout=10)
            if response.status_code == 200:
                self.beliefs[name] = response.json()
                self.logger.info(f"   -> ✅ Laporan dari '{name}' berhasil diterima.")
            else:
                self.beliefs[name] = {"status": "error", "code": response.status_code}
                self.logger.warning(f"   -> ⚠️  Laporan dari '{name}' gagal: Status {response.status_code}")
        except Exception as e:
            self.beliefs[name] = {"status": "unreachable", "error": str(e)}
            self.logger.error(f"   -> ❌ Mata-mata '{name}' gagal menghubungi target: {e}")
