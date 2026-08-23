"""
========================================================================================
HUGGING FACE DATASET MEMORY VAULT: 24/7 FREE TIER CLOUD PERSISTENCE
========================================================================================
"""

import os
import json
import threading
from typing import Dict, Any, Optional
from huggingface_hub import HfApi, hf_hub_download, create_repo


class HFDatasetMemoryVault:
    def __init__(
        self,
        repo_id: str = "Explorerp/sovereign-civilization-memory",
        token: Optional[str] = None,
        local_cache_dir: str = "./data"
    ):
        self.repo_id = repo_id
        self.token = token or os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
        self.local_cache_dir = local_cache_dir
        os.makedirs(local_cache_dir, exist_ok=True)
        
        self.api = HfApi(token=self.token) if self.token else None
        self._ensure_repo_exists()

    def _ensure_repo_exists(self):
        if not self.token:
            return
        try:
            create_repo(
                repo_id=self.repo_id,
                repo_type="dataset",
                private=True,
                token=self.token,
                exist_ok=True
            )
        except Exception:
            pass

    def save_checkpoint(
        self,
        state_dict: Dict[str, Any],
        filename: str = "civilization_champion.json",
        commit_msg: str = "Auto-save civilization checkpoint",
        async_upload: bool = True
    ):
        local_path = os.path.join(self.local_cache_dir, filename)
        try:
            with open(local_path, 'w') as f:
                json.dump(state_dict, f, indent=2)
        except Exception as e:
            print(f"[HF Memory Error]: {e}")
            return

        if not self.api or not self.token:
            return

        def _do_upload():
            try:
                self.api.upload_file(
                    path_or_fileobj=local_path,
                    path_in_repo=filename,
                    repo_id=self.repo_id,
                    repo_type="dataset",
                    commit_message=commit_msg,
                    token=self.token
                )
            except Exception as ex:
                print(f"[HF Memory Upload Warning]: {ex}")

        if async_upload:
            threading.Thread(target=_do_upload, daemon=True).start()
        else:
            _do_upload()

    def load_checkpoint(self, filename: str = "civilization_champion.json") -> Optional[Dict[str, Any]]:
        local_path = os.path.join(self.local_cache_dir, filename)
        if self.token:
            try:
                downloaded_path = hf_hub_download(
                    repo_id=self.repo_id,
                    filename=filename,
                    repo_type="dataset",
                    token=self.token
                )
                with open(downloaded_path, 'r') as f:
                    return json.load(f)
            except Exception:
                pass

        if os.path.exists(local_path):
            try:
                with open(local_path, 'r') as f:
                    return json.load(f)
            except Exception:
                pass

        return None
