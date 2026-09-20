"""BinoryLogy HF Vault - Immortal cloud checkpoint storage via Hugging Face Dataset.
Mirrors the pattern used by the Automata Multiverse deployment.
Saves the full physics discovery state as JSON to HF Dataset repo on every checkpoint.
On Render reboot, restores from HF (true immortal 24/7 training).
"""
import os, io, json, threading
from typing import Dict, Any, Optional
try:
    from huggingface_hub import HfApi, hf_hub_download, create_repo
    _HF_AVAILABLE = True
except ImportError:
    _HF_AVAILABLE = False

class BinoryHFVault:
    """Cloud state persistence for BinoryLogy using HuggingFace Dataset as immortal storage."""

    def __init__(self, repo_id: str = "Explorerp/binorylogy-physics-memory",
                 token: Optional[str] = None, local_cache_dir: str = "./data"):
        self.repo_id = repo_id
        self.token = token or os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
        self.local_cache_dir = local_cache_dir
        os.makedirs(local_cache_dir, exist_ok=True)
        self.api = HfApi(token=self.token) if (_HF_AVAILABLE and self.token) else None
        self._ensure_repo()

    def _ensure_repo(self):
        if not self.token or not _HF_AVAILABLE:
            print("[BinoryVault] No HF_TOKEN - local-only fallback mode")
            return
        try:
            create_repo(repo_id=self.repo_id, repo_type="dataset",
                        private=True, token=self.token, exist_ok=True)
            print(f"[BinoryVault] Connected to HF Dataset: {self.repo_id}")
        except Exception as e:
            print(f"[BinoryVault] Repo setup warning: {e}")

    def save(self, state: Dict[str, Any], filename: str = "binory_checkpoint.json",
             commit_msg: str = "BinoryLogy auto-checkpoint", async_upload: bool = True):
        """Save checkpoint compactly and push to HF Dataset via in-memory stream."""
        try:
            compact_json = json.dumps(state, separators=(',', ':'), default=str)
        except Exception as e:
            print(f"[BinoryVault] Serialization error: {e}")
            return

        local_path = os.path.join(self.local_cache_dir, filename)
        try:
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(compact_json)
        except Exception as e:
            print(f"[BinoryVault] Local save error: {e}")
            return

        if not self.api:
            return

        # Bandwidth Guard: Hash deduplication to eliminate redundant network uploads
        import hashlib
        content_hash = hashlib.sha256(compact_json.encode("utf-8")).hexdigest()
        if not hasattr(self, "_last_hashes"):
            self._last_hashes = {}
        if self._last_hashes.get(filename) == content_hash:
            return
        self._last_hashes[filename] = content_hash

        def _upload():
            try:
                stream_buf = io.BytesIO(compact_json.encode("utf-8"))
                self.api.upload_file(
                    path_or_fileobj=stream_buf,
                    path_in_repo=filename,
                    repo_id=self.repo_id,
                    repo_type="dataset",
                    commit_message=commit_msg,
                    token=self.token,
                )
                print(f"[BinoryVault] Cloud sync: {filename} -> {self.repo_id}")
            except Exception as ex:
                print(f"[BinoryVault] Upload warning (will retry next tick): {ex}")

        if async_upload:
            threading.Thread(target=_upload, daemon=True).start()
        else:
            _upload()

    def load(self, filename: str = "binory_checkpoint.json") -> Optional[Dict[str, Any]]:
        """Pull latest state from HF Dataset, fallback to local cache."""
        local_path = os.path.join(self.local_cache_dir, filename)

        if self.token and _HF_AVAILABLE:
            try:
                dl_path = hf_hub_download(
                    repo_id=self.repo_id, filename=filename,
                    repo_type="dataset", token=self.token
                )
                with open(dl_path, "r", encoding="utf-8") as f:
                    state = json.load(f)
                print(f"[BinoryVault] Restored from cloud: {self.repo_id}/{filename}")
                return state
            except Exception as e:
                print(f"[BinoryVault] No cloud checkpoint found (fresh start): {e}")

        if os.path.exists(local_path):
            try:
                with open(local_path, "r", encoding="utf-8") as f:
                    state = json.load(f)
                print(f"[BinoryVault] Restored from local cache: {local_path}")
                return state
            except Exception as e:
                print(f"[BinoryVault] Local cache read error: {e}")

        return None
