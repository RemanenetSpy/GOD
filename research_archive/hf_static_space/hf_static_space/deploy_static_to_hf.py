"""
========================================================================================
DEPLOYMENT SCRIPT FOR HUGGING FACE STATIC SPACES (100% FREE)
========================================================================================
Usage:
    python deploy_static_to_hf.py --repo_id <username>/<space_name> --token <hf_token>
Or with environment variable:
    set HF_TOKEN=your_huggingface_token
    python deploy_static_to_hf.py --repo_id <username>/<space_name>
========================================================================================
"""

import os
import sys
import argparse
from huggingface_hub import HfApi, create_repo


def deploy(repo_id: str, token: str = None):
    hf_token = token or os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    if not hf_token:
        print("[ERROR] Hugging Face Token not found.")
        print("Please provide --token <your_hf_token> or set the HF_TOKEN environment variable.")
        sys.exit(1)
        
    api = HfApi(token=hf_token)
    
    print(f"Creating / connecting to Hugging Face Static Space: {repo_id}...")
    create_repo(
        repo_id=repo_id,
        repo_type="space",
        space_sdk="static",
        token=hf_token,
        exist_ok=True
    )
    
    space_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Uploading static files from {space_dir} to Space {repo_id}...")
    
    api.upload_folder(
        folder_path=space_dir,
        repo_id=repo_id,
        repo_type="space",
        ignore_patterns=["deploy_static_to_hf.py"]
    )
    
    space_url = f"https://huggingface.co/spaces/{repo_id}"
    print("\n" + "=" * 80)
    print(f"[SUCCESS] STATIC SPACE DEPLOYMENT SUCCESSFUL!")
    print(f"Live Space URL: {space_url}")
    print("=" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy Static Sovereign Civilization to Hugging Face")
    parser.add_argument("--repo_id", type=str, required=True, help="Hugging Face Space repo ID (e.g., username/sovereign-civilization)")
    parser.add_argument("--token", type=str, default=None, help="Hugging Face API Token")
    args = parser.parse_args()
    
    deploy(repo_id=args.repo_id, token=args.token)
