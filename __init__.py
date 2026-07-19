import requests

class SafebooruSequentialTopTags:
    available_safebooru_post_tags_queue = []
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_prompt": ("STRING", {"multiline": True, "default": ""}),
                "safebooru_username": ("STRING", {"multiline": False, "default": ""}),
                "safebooru_api_key": ("STRING", {"multiline": False, "default": ""}),
                "categories": ("STRING", {"multiline": False, "default": "general, artist"}),
                "replace_underscores": ("BOOLEAN", {"default": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("combined_prompt", "current_post_tags")
    FUNCTION = "fetch_next_tags_and_prepend"
    CATEGORY = "utils"

    def fetch_next_tags_and_prepend(self, base_prompt, safebooru_username, safebooru_api_key, categories, replace_underscores, seed):
        if not self.__class__.available_safebooru_post_tags_queue:
            api_endpoint_url = f"https://safebooru.donmai.us/posts.json?limit=200&tags=order:rank"
            if safebooru_username and safebooru_api_key:
                api_endpoint_url += f"&login={safebooru_username}&api_key={safebooru_api_key}"
            
            http_request_headers = {
                "User-Agent": f"SafebooruTopTagsNode/1.0 ({safebooru_username or 'unknown'})",
                "Accept": "application/json"
            }
            
            try:
                api_response = requests.get(
                    api_endpoint_url, 
                    headers=http_request_headers, 
                    timeout=10
                )
                api_response.raise_for_status()
                post_data_list = api_response.json()
                
                for individual_post_data in post_data_list:
                    self.__class__.available_safebooru_post_tags_queue.append(individual_post_data)
                        
            except Exception as network_or_parsing_error:
                print(f"[Safebooru Node Error] {network_or_parsing_error}")

        if self.__class__.available_safebooru_post_tags_queue:
            safe_index = seed % len(self.__class__.available_safebooru_post_tags_queue)
            post_data = self.__class__.available_safebooru_post_tags_queue[safe_index]
            tags_to_include = []
            cats = [c.strip().lower() for c in categories.split(",") if c.strip()]
            include_series = "copyright" in cats or "series" in cats
            include_character = "character" in cats or "character_name" in cats
            include_artist = "artist" in cats
            include_general = "general" in cats
            include_meta = "meta" in cats

            if include_series:
                series_tags = post_data.get("tag_string_copyright", "")
                if series_tags: tags_to_include.append(series_tags)
                
            if include_character:
                char_tags = post_data.get("tag_string_character", "")
                if char_tags: tags_to_include.append(char_tags)
                
            if include_artist:
                artist_tags = post_data.get("tag_string_artist", "")
                if artist_tags: tags_to_include.append(artist_tags)
            
            if include_general:
                general_tags = post_data.get("tag_string_general", "")
                if general_tags: tags_to_include.append(general_tags)
            
            if include_meta:
                meta_tags = post_data.get("tag_string_meta", "")
                if meta_tags: tags_to_include.append(meta_tags)
            
            combined_raw = " ".join(tags_to_include)
            if combined_raw.strip():
                tags_list = combined_raw.split()
                if replace_underscores:
                    tags_list = [tag.replace("_", " ") for tag in tags_list]
                current_post_tags = ", ".join(tags_list) + ","
            else:
                current_post_tags = ""
        else:
            current_post_tags = ""

        if base_prompt.strip() and current_post_tags.strip():
            combined_prompt = f"{current_post_tags} {base_prompt}"
        elif current_post_tags.strip():
            combined_prompt = current_post_tags
        else:
            combined_prompt = base_prompt
            
        console_separator_line = "-" * 50
        print(f"\n{console_separator_line}")
        print(f"[Safebooru Node] Current Tag Index: {seed} (Mod: {seed % max(1, len(self.__class__.available_safebooru_post_tags_queue))}) / {max(0, len(self.__class__.available_safebooru_post_tags_queue) - 1)}")
        print(f"[Safebooru Node] Exact Fetched Tags:\n{current_post_tags[:100]}...") 
        print(f"{console_separator_line}")
            
        return (combined_prompt, current_post_tags)

class DanbooruSequentialTopTags:
    available_danbooru_post_tags_queue = []
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_prompt": ("STRING", {"multiline": True, "default": ""}),
                "danbooru_username": ("STRING", {"multiline": False, "default": ""}),
                "danbooru_api_key": ("STRING", {"multiline": False, "default": ""}),
                "categories": ("STRING", {"multiline": False, "default": "general, artist"}),
                "replace_underscores": ("BOOLEAN", {"default": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("combined_prompt", "current_post_tags")
    FUNCTION = "fetch_next_tags_and_prepend"
    CATEGORY = "utils"

    def fetch_next_tags_and_prepend(self, base_prompt, danbooru_username, danbooru_api_key, categories, replace_underscores, seed):
        if not self.__class__.available_danbooru_post_tags_queue:
            api_endpoint_url = f"https://danbooru.donmai.us/posts.json?limit=200&tags=order:rank"
            if danbooru_username and danbooru_api_key:
                api_endpoint_url += f"&login={danbooru_username}&api_key={danbooru_api_key}"
            
            http_request_headers = {
                "User-Agent": f"DanbooruTopTagsNode/1.0 ({danbooru_username or 'unknown'})",
                "Accept": "application/json"
            }
            
            try:
                # Danbooru allows standard requests with a proper User-Agent
                api_response = requests.get(
                    api_endpoint_url, 
                    headers=http_request_headers, 
                    timeout=10
                )
                api_response.raise_for_status()
                post_data_list = api_response.json()
                
                for individual_post_data in post_data_list:
                    self.__class__.available_danbooru_post_tags_queue.append(individual_post_data)
                        
            except Exception as network_or_parsing_error:
                print(f"[Danbooru Node Error] {network_or_parsing_error}")

        if self.__class__.available_danbooru_post_tags_queue:
            safe_index = seed % len(self.__class__.available_danbooru_post_tags_queue)
            post_data = self.__class__.available_danbooru_post_tags_queue[safe_index]
            tags_to_include = []
            
            cats = [c.strip().lower() for c in categories.split(",") if c.strip()]
            include_series = "copyright" in cats or "series" in cats
            include_character = "character" in cats or "character_name" in cats
            include_artist = "artist" in cats
            include_general = "general" in cats
            include_meta = "meta" in cats

            if include_series:
                series_tags = post_data.get("tag_string_copyright", "")
                if series_tags: tags_to_include.append(series_tags)
                
            if include_character:
                char_tags = post_data.get("tag_string_character", "")
                if char_tags: tags_to_include.append(char_tags)
                
            if include_artist:
                artist_tags = post_data.get("tag_string_artist", "")
                if artist_tags: tags_to_include.append(artist_tags)
            
            if include_general:
                general_tags = post_data.get("tag_string_general", "")
                if general_tags: tags_to_include.append(general_tags)
            
            if include_meta:
                meta_tags = post_data.get("tag_string_meta", "")
                if meta_tags: tags_to_include.append(meta_tags)
            
            combined_raw = " ".join(tags_to_include)
            if combined_raw.strip():
                tags_list = combined_raw.split()
                if replace_underscores:
                    tags_list = [tag.replace("_", " ") for tag in tags_list]
                current_post_tags = ", ".join(tags_list) + ","
            else:
                current_post_tags = ""
        else:
            current_post_tags = ""

        if base_prompt.strip() and current_post_tags.strip():
            combined_prompt = f"{current_post_tags} {base_prompt}"
        elif current_post_tags.strip():
            combined_prompt = current_post_tags
        else:
            combined_prompt = base_prompt
            
        console_separator_line = "-" * 50
        print(f"\n{console_separator_line}")
        print(f"[Danbooru Node] Current Tag Index: {seed} (Mod: {seed % max(1, len(self.__class__.available_danbooru_post_tags_queue))}) / {max(0, len(self.__class__.available_danbooru_post_tags_queue) - 1)}")
        print(f"[Danbooru Node] Exact Fetched Tags:\n{current_post_tags[:100]}...") 
        print(f"{console_separator_line}")
            
        return (combined_prompt, current_post_tags)

NODE_CLASS_MAPPINGS = {
    "SafebooruSequentialTopTags": SafebooruSequentialTopTags,
    "DanbooruSequentialTopTags": DanbooruSequentialTopTags
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SafebooruSequentialTopTags": "Fetch Safebooru Sequential Top Tags",
    "DanbooruSequentialTopTags": "Fetch Danbooru Sequential Top Tags"
}