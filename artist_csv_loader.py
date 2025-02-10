import os
import re
import folder_paths
import pandas as pd
from random import choice
import random

class ArtistLoader:
    @staticmethod
    def load_artists_csv(single_artist_path: str, mixed_artists_path: str):
        single_artist = []
        mixed_artists = []
        if not os.path.exists(single_artist_path) or not os.path.exists(mixed_artists_path):
            print(f"""Error. No artists.csv found. Put your artists.csv in the custom_nodes-ComfyUI_Loader-CSV directory of ComfyUI. Then press "Refresh".
                  Your current root directory is: {folder_paths.base_path}
            """)
            return single_artist, mixed_artists
        try:
            artists_df = pd.read_csv(single_artist_path)
            single_artist = list(artists_df['画师'])
            artists_df = pd.read_csv(mixed_artists_path)
            mixed_artists = list(artists_df['画师串'])
        except Exception as e:
            print(f"""Error loading artists.csv. Make sure it is in the custom_nodes-ComfyUI_Loader-CSV directory of ComfyUI. Then press "Refresh".
                    Your current root directory is: {folder_paths.base_path}
                    Error: {e}
            """)
        return single_artist, mixed_artists
        
    @classmethod
    def INPUT_TYPES(cls):
        single_artists_path = os.path.join(folder_paths.base_path, "custom_nodes/ComfyUI-Artist-Selector/CSV/1000SingleArtist.csv")
        mixed_artists_path = os.path.join(folder_paths.base_path, "custom_nodes/ComfyUI-Artist-Selector/CSV/300MixedArtists.csv")
        cls.single_artist_list, cls.mixed_artists_list = cls.load_artists_csv(single_artists_path, mixed_artists_path)
        return {
            "required": {
                "mode": (['random', 'random_single', 'random_mixed', 'none', 'single', 'mixed'], {"default": 'none'}),
                "seed": ("INT", {"default": 0}),
            },
            "optional": {
                "single_artist": (cls.single_artist_list, {"default": ""}),
                "mixed_artists": (cls.mixed_artists_list, {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("artist_tags",)
    FUNCTION = "execute"
    CATEGORY = "ArtistSelector"   

    def execute(self, mode, single_artist, mixed_artists, seed):
        tags = ''
        if mode == 'random':
            random.seed(seed)
            tags = choice(self.single_artist_list + self.mixed_artists_list)
        elif mode == 'random_single':
            random.seed(seed)
            tags = choice(self.single_artist_list)
        elif mode == 'random_mixed':
            random.seed(seed)
            tags = choice(self.mixed_artists_list)
        elif mode == 'single':
            tags = single_artist
        elif mode == 'mixed':
            tags = mixed_artists
        
        return (tags,)

#NODE NAMING

NODE_CLASS_MAPPINGS = {
    "LoadArtistTag": ArtistLoader,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ArtistLoader": "SelectArtist",
}
