"""
========================================================================================
HUGGING FACE DATASET MEMORY VAULT: 24/7 FREE TIER CLOUD PERSISTENCE
========================================================================================
Uses a Private Hugging Face Dataset repository as an immortal cloud checkpoint vault.
Whenever the Sovereign Civilization levels up, discovers subroutines, or completes epochs:
1. Pushes JSON checkpoints & subroutine weights to the private Dataset repository.
2. When the Space / container reboots, pulls the latest state from the Dataset repo.
========================================================================================
"""

import os
import json
import threading
from typing import Dict, Any, Optional
from huggingface_hub import HfApi, hf_hub_download, create_repo


class HFDatasetMemoryVault:
    """
    Cloud state persistence engine using a Private Hugging Face Dataset repository.
    Enables true 24/7 immortal training on free ephemeral cloud containers.
    """
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
        """Ensures the private dataset repository exists on Hugging Face Hub."""
        if not self.token:
            print("[HF Memory] No HF_TOKEN provided; operating in local-only fallback mode.")
            return
            
        try:
            create_repo(
                repo_id=self.repo_id,
                repo_type="dataset",
                private=True,
                token=self.token,
                exist_ok=True
            )
            print(f"[HF Memory] Connected to Private Dataset Vault: {self.repo_id}")
        except Exception as e:
            print(f"[HF Memory Warning] Failed to verify/create Dataset repo: {e}")

    def save_checkpoint(
        self,
        state_dict: Dict[str, Any],
        filename: str = "civilization_champion.json",
        commit_msg: str = "Auto-save civilization checkpoint",
        async_upload: bool = True
    ):
        """
        Saves checkpoint locally and uploads directly to the private Hugging Face Dataset.
        """
        local_path = os.path.join(self.local_cache_dir, filename)
        try:
            with open(local_path, 'w') as f:
                json.dump(state_dict, f, indent=2)
        except Exception as e:
            print(f"[HF Memory Error] Failed to write local cache file: {e}")
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
                print(f"[HF Memory Cloud Sync] Pushed {filename} to {self.repo_id}")
            except Exception as ex:
                print(f"[HF Memory Warning] Hub upload failed (will retry next epoch): {ex}")

        if async_upload:
            t = threading.Thread(target=_do_upload, daemon=True)
            t.start()
        else:
            _do_upload()

    def load_checkpoint(self, filename: str = "civilization_champion.json") -> Optional[Dict[str, Any]]:
        """
        Pulls and deserializes the latest state from the private Hugging Face Dataset repo.
        Falls back to local cache if offline or on fresh start.
        """
        local_path = os.path.join(self.local_cache_dir, filename)
        
        # 1. Try pulling fresh cloud state from Private Dataset
        if self.token:
            try:
                downloaded_path = hf_hub_download(
                    repo_id=self.repo_id,
                    filename=filename,
                    repo_type="dataset",
                    token=self.token
                )
                with open(downloaded_path, 'r') as f:
                    cloud_state = json.load(f)
                print(f"[HF Memory Recovery] Restored state from Cloud Dataset Vault ({self.repo_id}/{filename})!")
                return cloud_state
            except Exception as e:
                print(f"[HF Memory Info] No cloud checkpoint found on Hub (or initial start): {e}")

        # 2. Fallback to local cache if cloud pull failed
        if os.path.exists(local_path):
            try:
                with open(local_path, 'r') as f:
                    local_state = json.load(f)
                print(f"[HF Memory Recovery] Loaded state from local cache ({local_path})")
                return local_state
            except Exception as e:
                print(f"[HF Memory Warning] Failed to read local cache: {e}")

        return None
