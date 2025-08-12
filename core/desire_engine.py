# core/desire_engine.py
import requests
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import logging

load_dotenv()

class DesireEngine:
    """Menetapkan tujuan strategis dan berkomunikasi dengan Otak Kuantum."""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.github_user = os.getenv("PROJECT_GITHUB_USER")
        self.github_repo = os.getenv("PROJECT_GITHUB_REPO")
        self.github_token = os.getenv("PROJECT_GITHUB_TOKEN")
        
        if not all([self.supabase_url, self.supabase_key, self.github_user, self.github_repo, self.github_token]):
            raise ValueError("Konfigurasi Supabase/GitHub tidak ditemukan di file .env!")
        
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)

    async def generate_desires(self, beliefs: dict) -> int | None:
        try:
            self.logger.info("📝 Mengirim laporan intelijen ke Otak Kuantum...")
            response = self.supabase.table("quantum_tasks").insert({
                "task_type": "optimize_desires", "payload": beliefs, "status": "pending"
            }).execute()
            task_id = response.data[0]["id"]
            self.logger.info(f"   -> ✅ Laporan berhasil dikirim dengan ID: {task_id}")
            await self._trigger_github_action()
            return task_id
        except Exception as e:
            self.logger.error(f"❌ Gagal mengirim tugas ke Supabase: {e}")
            return None

    async def _trigger_github_action(self):
        self.logger.info("📞 Menelepon Otak Kuantum di GitHub untuk bangun...")
        headers = {"Authorization": f"token {self.github_token}", "Accept": "application/vnd.github.v3+json"}
        url = f"https://api.github.com/repos/{self.github_user}/{self.github_repo}/actions/workflows/quantum_worker.yml/dispatches"
        data = {"ref": "main"}
        try:
            await asyncio.to_thread(requests.post, url, headers=headers, json=data, timeout=10)
            self.logger.info("   -> ✅ Panggilan berhasil. Otak Kuantum sedang dalam perjalanan!")
        except Exception as e:
            self.logger.error(f"❌ Gagal menelepon Otak Kuantum: {e}")
