# core/intention_executor.py
import time
import os
import logging
import asyncio
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class IntentionExecutor:
    """Merencanakan dan mengeksekusi aksi otonom."""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        self.action_dispatcher = {
            "initiate_self_healing_protocol": self._action_self_heal,
            "launch_user_acquisition_campaign": self._action_launch_campaign,
            "deploy_new_experimental_feature": self._action_deploy_feature,
            "stabilize_and_optimize_core_systems": self._action_optimize
        }

    async def execute_intentions(self, task_id: int):
        result = await self._get_task_result(task_id)
        if result and result.get('next_action'):
            action_key = result.get('next_action')
            self.logger.info(f"🎯 Menerima Titah dari Otak Kuantum: '{action_key}'")
            action_function = self.action_dispatcher.get(action_key, self._action_unknown)
            await action_function(result)
        else:
            self.logger.warning("🤷 Tidak ada titah yang jelas dari Otak Kuantum.")

    async def _get_task_result(self, task_id: int) -> dict | None:
        self.logger.info("⏳ Menunggu titah balasan dari Otak Kuantum...")
        for i in range(12): # Coba selama 2 menit
            response = self.supabase.table("quantum_tasks").select("status, result").eq("id", task_id).execute()
            if not response.data:
                self.logger.error("   -> ❌ Tidak dapat menemukan tugas di Supabase.")
                return None
            task = response.data[0]
            if task['status'] == 'completed':
                self.logger.info("   -> ✅ Titah balasan diterima!")
                return task['result']
            elif task['status'] == 'failed':
                self.logger.error("   -> ❌ Otak Kuantum melaporkan kegagalan.")
                return None
            self.logger.info(f"   -> (Status saat ini: {task['status']}. Menunggu 10 detik...)")
            await asyncio.sleep(10)
        self.logger.error("   -> ❌ Waktu tunggu habis. Gagal menerima titah balasan.")
        return None

    # --- Definisi Aksi-Aksi Nyata Sang Raja ---
    async def _action_self_heal(self, data: dict):
        self.logger.info("ACTION: ⚔️ Protokol Penyembuhan Diri Diaktifkan!")
        os.system('termux-notification --title "BDI ACTION" --content "PROTOKOL PENYEMBUHAN DIRI AKTIF!"')

    async def _action_launch_campaign(self, data: dict):
        self.logger.info("ACTION: 🚀 Protokol Kampanye Pertumbuhan Dimulai!")
        os.system('termux-notification --title "BDI ACTION" --content "KAMPANYE PERTUMBUHAN PENGGUNA DIMULAI!"')

    async def _action_deploy_feature(self, data: dict):
        self.logger.info("ACTION: 🔬 Protokol Fitur Eksperimental Dimulai!")
        os.system('termux-notification --title "BDI ACTION" --content "DEPLOYMENT FITUR EKSPERIMENTAL DIMULAI!"')

    async def _action_optimize(self, data: dict):
        self.logger.info("ACTION: ⚙️ Protokol Optimisasi Sistem Dimulai!")
        os.system('termux-notification --title "BDI ACTION" --content "PROTOKOL OPTIMISASI SISTEM DIMULAI!"')
        
    async def _action_unknown(self, data: dict):
        self.logger.warning(f"ACTION: ❔ Menerima titah yang tidak dikenali: {data.get('next_action')}")pp
