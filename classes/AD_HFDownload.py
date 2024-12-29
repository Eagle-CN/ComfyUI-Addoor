import os
import re
from urllib.parse import urlparse, unquote
from huggingface_hub import hf_hub_download, snapshot_download, HfApi
from huggingface_hub.utils import HfHubHTTPError
# import gradio as gr

class AD_HFDownload:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "download_url": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "placeholder": "https://huggingface.co/owner/repo/tree/main or https://hf-mirror.com/owner/repo/..."
                }),
                "repo_id": ("STRING", {"default": ""}),
                "save_path": ("STRING", {"default": ""}),
                "resource_type": (["model", "dataset"],),
                "use_mirror": ("BOOLEAN", {"default": False}),
                "create_folder": ("BOOLEAN", {"default": True}),
                "filename": ("STRING", {"default": "", "optional": True}),
                "hf_token": ("STRING", {
                    "default": "",
                    "placeholder": "Enter your Hugging Face token here"
                }),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("Download_Path", "Status")
    FUNCTION = "download_from_hf"
    OUTPUT_NODE = True
    CATEGORY = "🌻 Addoor/Utilities"

    def parse_hf_url(self, url):
        """Parse Hugging Face URL to extract repository info."""
        try:
            # Remove trailing slashes and parse URL
            url = url.rstrip('/')
            parsed = urlparse(url)
            
            # Check if it's a valid HF domain and determine if it's a mirror
            is_mirror = parsed.netloc == 'hf-mirror.com'
            if not (parsed.netloc in ['huggingface.co', 'hf-mirror.com']):
                return None
            
            # Split path parts
            parts = [p for p in parsed.path.split('/') if p]
            
            if len(parts) < 2:
                return None
                
            owner, repo = parts[0], parts[1]
            
            # Handle different URL patterns
            result = {
                'owner': owner,
                'repo': repo,
                'repo_id': f"{owner}/{repo}",
                'is_file': False,
                'filename': None,
                'subfolder': None,
                'is_mirror': is_mirror
            }
            
            if len(parts) > 2:
                if 'resolve' in parts:
                    # File download URL
                    result['is_file'] = True
                    file_path = '/'.join(parts[parts.index('resolve')+2:])
                    result['filename'] = file_path
                elif 'tree' in parts:
                    # Directory URL
                    if len(parts) > 4:
                        subfolder = '/'.join(parts[parts.index('tree')+2:])
                        result['subfolder'] = subfolder
                
            return result
        except Exception as e:
            print(f"Error parsing URL: {str(e)}")
            return None

    def download_from_hf(self, download_url, repo_id, save_path, resource_type, use_mirror, create_folder, filename="", hf_token=""):
        try:
            # Process the download URL if provided
            url_info = self.parse_hf_url(download_url) if download_url else None
            
            # Set up base parameters
            if not save_path:
                save_path = os.path.join(os.getcwd(), "downloads")
            
            # Use URL info if available, otherwise fall back to repo_id
            active_repo_id = url_info['repo_id'] if url_info else repo_id
            if not active_repo_id:
                return "", "Error: Either URL or Repository ID is required."
            
            # Create the final save path
            if create_folder:
                save_path = os.path.join(save_path, active_repo_id.split('/')[-1])
            
            os.makedirs(save_path, exist_ok=True)
            
            # Set up mirror endpoint based on URL or checkbox
            use_mirror_endpoint = use_mirror or (url_info and url_info['is_mirror'])
            mirror_url = "https://hf-mirror.com" if use_mirror_endpoint else None
            
            # Validate token if provided
            if hf_token:
                try:
                    api = HfApi(token=hf_token)
                    api.whoami()
                except Exception as e:
                    return "", f"Error: Invalid Hugging Face token. Details: {str(e)}"
            
            # Common download parameters
            download_kwargs = {
                "repo_id": active_repo_id,
                "repo_type": resource_type,
                "local_dir": save_path,
                "local_dir_use_symlinks": False,
                "resume_download": True,
                "endpoint": mirror_url,
                "token": hf_token if hf_token else None
            }
            
            # Handle different download scenarios
            if url_info and url_info['is_file']:
                # Download specific file from URL
                file_path = hf_hub_download(
                    filename=url_info['filename'],
                    **download_kwargs
                )
                status = f"File '{url_info['filename']}' downloaded successfully using {'mirror' if use_mirror_endpoint else 'default'} endpoint."
                return file_path, status
                
            elif url_info and url_info['subfolder']:
                # Download specific subfolder using allow_patterns
                subfolder_pattern = f"{url_info['subfolder']}/**"
                downloaded_path = snapshot_download(
                    allow_patterns=subfolder_pattern,
                    **download_kwargs
                )
                status = f"Subfolder '{url_info['subfolder']}' downloaded successfully using {'mirror' if use_mirror_endpoint else 'default'} endpoint."
                return downloaded_path, status
                
            elif filename:
                # Download specific file using filename parameter
                file_path = hf_hub_download(
                    filename=filename,
                    **download_kwargs
                )
                status = f"File '{filename}' downloaded successfully using {'mirror' if use_mirror_endpoint else 'default'} endpoint."
                return file_path, status
                
            else:
                # Download entire repository
                downloaded_path = snapshot_download(**download_kwargs)
                status = f"Repository '{active_repo_id}' downloaded successfully using {'mirror' if use_mirror_endpoint else 'default'} endpoint."
                return downloaded_path, status

        except HfHubHTTPError as e:
            if hasattr(e, 'response') and e.response is not None:
                if e.response.status_code == 401:
                    return "", "Error: Authentication failed. Please check your Hugging Face token or ensure you have access to this repository."
                elif e.response.status_code == 404:
                    return "", f"Error: Repository or file not found: {active_repo_id}"
                else:
                    return "", f"Error downloading: {e.response.text}"
            else:
                return "", f"Error: An HTTP error occurred without a response. Details: {str(e)}"
        except Exception as e:
            return "", f"Error: {str(e)}"

