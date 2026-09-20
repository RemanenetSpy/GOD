import os
import io
import json
import threading
from typing import Dict, Any, Optional

def prune_hf_cache():
    """Prunes temporary huggingface cache locks and incomplete blobs to prevent disk bloat."""
    import shutil
    try:
        cache_hub = os.path.expanduser("~/.cache/huggingface/hub")
        if os.path.exists(cache_hub):
            for item in os.listdir(cache_hub):
                if item.startswith("tmp") or item.endswith(".incomplete") or item.endswith(".lock"):
                    p = os.path.join(cache_hub, item)
                    try:
                        if os.path.isdir(p):
                            shutil.rmtree(p, ignore_errors=True)
                        else:
                            os.remove(p)
                    except Exception:
                        pass
    except Exception:
        pass

try:
    from huggingface_hub import HfApi, hf_hub_download, create_repo
    _HF_AVAILABLE = True
except ImportError:
    _HF_AVAILABLE = False


class ARCSovereignVault:
    """
    Cloud state persistence for ARC Sovereign Arena using Hugging Face Dataset as immortal cloud storage.
    Synchronizes discoveries, pass counters, and mastered task states to/from Hugging Face Dataset repo.
    """

    def __init__(
        self,
        repo_id: Optional[str] = None,
        token: Optional[str] = None,
        local_cache_dir: str = "./data"
    ):
        self.token = token or os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
        env_repo = os.environ.get("HF_DATASET_REPO", "")
        if repo_id:
            self.repo_id = repo_id
        elif env_repo and "sovereign-civilization-memory" not in env_repo:
            self.repo_id = env_repo
        else:
            self.repo_id = "Explorerp/binorylogy-physics-memory"

        self.local_cache_dir = local_cache_dir
        os.makedirs(local_cache_dir, exist_ok=True)
        self.api = HfApi(token=self.token) if (_HF_AVAILABLE and self.token) else None
        self._ensure_repo()

    def _ensure_repo(self):
        if not self.token or not _HF_AVAILABLE:
            print("[ARC Vault] Operating in local-only fallback mode (no HF_TOKEN)")
            return
        try:
            create_repo(
                repo_id=self.repo_id,
                repo_type="dataset",
                private=True,
                token=self.token,
                exist_ok=True
            )
            print(f"[ARC Vault] Connected to Hugging Face Dataset: {self.repo_id}")
        except Exception as e:
            print(f"[ARC Vault] Dataset repo check: {e}")

    def save(
        self,
        state: Dict[str, Any],
        filename: str = "arc_sovereign_checkpoint.json",
        commit_msg: str = "ARC Sovereign checkpoint auto-save",
        async_upload: bool = True
    ):
        """Saves checkpoint compactly and pushes via in-memory stream to HF Dataset."""
        try:
            compact_json = json.dumps(state, separators=(',', ':'), default=str)
        except Exception as e:
            print(f"[ARC Vault] Serialization error: {e}")
            return

        local_path = os.path.join(self.local_cache_dir, filename)
        try:
            with open(local_path, "w", encoding="utf-8") as fe:
                fe.write(compact_json)
        except Exception as e:
            print(f"[ARC Vault] Local save error: {e}")
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
                    token=self.token
                )
                print(f"[ARC Vault Cloud Sync] Pushed {filename} to {self.repo_id}")
            except Exception as ex:
                print(f"[ARC Vault] Upload warning (will retry next interval): {ex}")

        if async_upload:
            threading.Thread(target=_upload, daemon=True).start()
        else:
            _upload()

    def load(self, filename: str = "arc_sovereign_checkpoint.json") -> Optional[Dict[str, Any]]:
        """Pulls latest state from HF Dataset; falls back to local cache."""
        local_path = os.path.join(self.local_cache_dir, filename)

        if self.token and _HF_AVAILABLE:
            try:
                dl_path = hf_hub_download(
                    repo_id=self.repo_id,
                    filename=filename,
                    repo_type="dataset",
                    token=self.token
                )
                with open(dl_path, "r", encoding="utf-8") as f:
                    state = json.load(f)
                print(f"[ARC Vault] Restored remote checkpoint from {self.repo_id}/{filename}")
                return state
            except Exception as e:
                print(f"[ARC Vault] No remote checkpoint yet (starting fresh or using local): {e}")

        if os.path.exists(local_path):
            try:
                with open(local_path, "r", encoding="utf-8") as f:
                    state = json.load(f)
                print(f"[ARC Vault] Restored from local cache: {local_path}")
                return state
            except Exception as e:
                print(f"[ARC Vault] Local cache read error: {e}")

        return None
