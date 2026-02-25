#!/usr/bin/env python3
"""
Music Profile Data Ingestion Script
Aggregates listening history, concert attendance, and music preferences
from Last.fm and Setlist.fm APIs into a unified profile.
"""

import requests
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class MusicProfileIngest:
    def __init__(self, lastfm_api_key: str, setlistfm_api_key: str):
        """Initialize with API keys."""
        self.lastfm_api_key = lastfm_api_key
        self.setlistfm_api_key = setlistfm_api_key
        self.lastfm_user = "fastlane2"
        self.setlistfm_user = "fastlane2"
        
        self.lastfm_base = "https://ws.audioscrobbler.com/2.0/"
        self.setlistfm_base = "https://api.setlist.fm/rest/1.0/"
        
        self.data = {
            "last_fm": {},
            "setlist_fm": {},
            "aggregated": {},
            "ingested_at": datetime.now().isoformat()
        }

    def fetch_lastfm_top_artists(self, limit: int = 100, period: str = "overall") -> List[Dict]:
        """Fetch top artists from Last.fm."""
        print(f"Fetching Last.fm top artists ({period})...")
        params = {
            "method": "user.getTopArtists",
            "user": self.lastfm_user,
            "api_key": self.lastfm_api_key,
            "format": "json",
            "limit": limit,
            "period": period
        }
        
        try:
            response = requests.get(self.lastfm_base, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "topartists" in data:
                artists = data["topartists"]["artist"]
                print(f"  ✓ Retrieved {len(artists)} top artists")
                return artists
            else:
                print(f"  ✗ No artist data found")
                return []
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return []

    def fetch_lastfm_top_tracks(self, limit: int = 100, period: str = "overall") -> List[Dict]:
        """Fetch top tracks from Last.fm."""
        print(f"Fetching Last.fm top tracks ({period})...")
        params = {
            "method": "user.getTopTracks",
            "user": self.lastfm_user,
            "api_key": self.lastfm_api_key,
            "format": "json",
            "limit": limit,
            "period": period
        }
        
        try:
            response = requests.get(self.lastfm_base, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "toptracks" in data:
                tracks = data["toptracks"]["track"]
                print(f"  ✓ Retrieved {len(tracks)} top tracks")
                return tracks
            else:
                print(f"  ✗ No track data found")
                return []
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return []

    def fetch_lastfm_recent_tracks_with_stats(self, pages: int = 5) -> List[Dict]:
        """Fetch recent tracks from Last.fm across multiple pages for comprehensive stats."""
        print(f"Fetching Last.fm recent tracks (comprehensive stats)...")
        all_tracks = []
        
        try:
            for page in range(1, pages + 1):
                params = {
                    "method": "user.getRecentTracks",
                    "user": self.lastfm_user,
                    "api_key": self.lastfm_api_key,
                    "format": "json",
                    "limit": 50,
                    "page": page,
                    "extended": "1"  # Get extended info with play counts
                }
                
                response = requests.get(self.lastfm_base, params=params)
                response.raise_for_status()
                data = response.json()
                
                if "recenttracks" in data:
                    tracks = data["recenttracks"].get("track", [])
                    if not isinstance(tracks, list):
                        tracks = [tracks] if tracks else []
                    all_tracks.extend(tracks)
                    
                    # Check pagination info
                    attr = data["recenttracks"].get("@attr", {})
                    current_page = int(attr.get("page", 1))
                    total_pages = int(attr.get("totalPages", 1))
                    
                    if current_page >= total_pages:
                        break
                else:
                    break
            
            print(f"  ✓ Retrieved {len(all_tracks)} recent tracks with stats")
            return all_tracks
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return []

    def fetch_setlistfm_user_profile(self) -> Dict:
        """Fetch user profile from Setlist.fm."""
        print(f"Fetching Setlist.fm user profile...")
        headers = {"x-api-key": self.setlistfm_api_key}
        url = f"{self.setlistfm_base}user/{self.setlistfm_user}"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            print(f"  ✓ Retrieved user profile")
            return data
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return {}

    def fetch_setlistfm_attended_concerts(self, limit: int = 100) -> List[Dict]:
        """Fetch attended concerts from Setlist.fm."""
        print(f"Fetching Setlist.fm attended concerts...")
        headers = {"x-api-key": self.setlistfm_api_key}
        url = f"{self.setlistfm_base}user/{self.setlistfm_user}/attended"
        
        concerts = []
        page = 1
        
        try:
            while page <= (limit // 20 + 1):  # API returns 20 per page
                params = {"p": page}
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                if "setlist" in data:
                    concerts.extend(data["setlist"])
                    
                    # Check if there are more pages
                    if len(data.get("setlist", [])) < 20:
                        break
                    page += 1
                else:
                    break
            
            print(f"  ✓ Retrieved {len(concerts)} attended concerts")
            return concerts
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return []

    def aggregate_data(self):
        """Aggregate all fetched data into unified profile."""
        print("\nAggregating data...")
        
        # Extract unique artists from Last.fm
        lastfm_artists = {}
        for artist in self.data["last_fm"].get("top_artists", []):
            name = artist.get("name")
            if name:
                lastfm_artists[name] = {
                    "playcount": int(artist.get("playcount", 0)),
                    "rank": artist.get("@attr", {}).get("rank", "N/A")
                }
        
        # Extract song stats from recent tracks
        song_stats = []
        seen_tracks = set()
        for track in self.data["last_fm"].get("recent_tracks_stats", []):
            artist = track.get("artist", {})
            if isinstance(artist, dict):
                artist_name = artist.get("name", "Unknown")
            else:
                artist_name = str(artist)
            
            track_name = track.get("name", "Unknown")
            track_key = f"{artist_name}|{track_name}"
            
            # Avoid duplicates
            if track_key not in seen_tracks:
                seen_tracks.add(track_key)
                song_stats.append({
                    "name": track_name,
                    "artist": artist_name,
                    "playcount": int(track.get("playcount", 0)),
                    "loved": track.get("loved", "0")
                })
        
        # Extract unique artists from Setlist.fm
        setlistfm_artists = {}
        for concert in self.data["setlist_fm"].get("attended_concerts", []):
            artist_name = concert.get("artist", {}).get("name")
            if artist_name:
                if artist_name not in setlistfm_artists:
                    setlistfm_artists[artist_name] = {"concert_count": 0}
                setlistfm_artists[artist_name]["concert_count"] += 1
        
        # Merge artist data
        all_artists = {}
        for name, data in lastfm_artists.items():
            all_artists[name] = {
                "playcount": data["playcount"],
                "last_fm_rank": data["rank"],
                "concerts_attended": setlistfm_artists.get(name, {}).get("concert_count", 0)
            }
        
        for name, data in setlistfm_artists.items():
            if name not in all_artists:
                all_artists[name] = {
                    "playcount": 0,
                    "concerts_attended": data["concert_count"]
                }
        
        self.data["aggregated"] = {
            "artists": all_artists,
            "total_artists": len(all_artists),
            "total_concerts_attended": len(self.data["setlist_fm"].get("attended_concerts", [])),
            "unique_artists_with_concerts": len(setlistfm_artists),
            "top_artists_by_playcount": sorted(
                lastfm_artists.items(),
                key=lambda x: x[1]["playcount"],
                reverse=True
            )[:20],
            "song_stats": sorted(
                song_stats,
                key=lambda x: x["playcount"],
                reverse=True
            )[:50]
        }
        
        print(f"  ✓ Aggregated {len(all_artists)} unique artists")
        print(f"  ✓ Aggregated {len(song_stats)} unique tracks with play counts")

    def ingest(self) -> Dict[str, Any]:
        """Run full ingestion pipeline."""
        print("Starting Music Profile Ingestion...\n")
        
        # Last.fm data
        self.data["last_fm"]["top_artists"] = self.fetch_lastfm_top_artists()
        self.data["last_fm"]["top_tracks"] = self.fetch_lastfm_top_tracks()
        self.data["last_fm"]["recent_tracks_stats"] = self.fetch_lastfm_recent_tracks_with_stats(pages=5)
        
        # Setlist.fm data
        self.data["setlist_fm"]["user_profile"] = self.fetch_setlistfm_user_profile()
        self.data["setlist_fm"]["attended_concerts"] = self.fetch_setlistfm_attended_concerts()
        
        # Aggregate
        self.aggregate_data()
        
        print("\n✓ Ingestion complete!")
        return self.data

    def save_json(self, output_path: str = None):
        """Save ingested data to JSON file."""
        if output_path is None:
            output_path = "/var/home/mal/.zeroclaw/workspace/shared/music_data_raw.json"
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.data, f, indent=2)
        
        print(f"✓ Data saved to {output_path}")

    def generate_profile_markdown(self, output_path: str = None):
        """Generate markdown profile from aggregated data."""
        if output_path is None:
            output_path = "/var/home/mal/.zeroclaw/workspace/shared/music_profile_generated.md"
        
        md = "# Music Profile\n\n"
        md += f"*Generated {self.data['ingested_at']}*\n\n"
        
        # Summary
        agg = self.data.get("aggregated", {})
        md += "## Summary\n\n"
        md += f"- **Total Unique Artists:** {agg.get('total_artists', 0)}\n"
        md += f"- **Concerts Attended:** {agg.get('total_concerts_attended', 0)}\n"
        md += f"- **Artists with Concert Attendance:** {agg.get('unique_artists_with_concerts', 0)}\n\n"
        
        # Top artists by playcount
        md += "## Top Artists (by Last.fm playcount)\n\n"
        for artist, data in agg.get("top_artists_by_playcount", [])[:15]:
            concerts = data.get("concerts_attended", 0)
            concert_str = f" | {concerts} concert{'s' if concerts != 1 else ''}" if concerts > 0 else ""
            md += f"- **{artist}** — {data['playcount']} plays{concert_str}\n"
        
        md += "\n## Top Tracks (by playcount)\n\n"
        for i, track in enumerate(agg.get("song_stats", [])[:15], 1):
            name = track.get("name", "Unknown")
            artist = track.get("artist", "Unknown")
            playcount = track.get("playcount", 0)
            md += f"{i}. *{name}* — {artist} ({playcount} plays)\n"
        
        md += "\n## Concert Venues & Artists\n\n"
        concert_artists = {}
        for concert in self.data["setlist_fm"].get("attended_concerts", []):
            artist = concert.get("artist", {}).get("name", "Unknown")
            venue = concert.get("venue", {}).get("name", "Unknown")
            city = concert.get("venue", {}).get("city", {}).get("name", "")
            
            if artist not in concert_artists:
                concert_artists[artist] = []
            concert_artists[artist].append(f"{venue}, {city}")
        
        for artist in sorted(concert_artists.keys())[:15]:
            venues = concert_artists[artist]
            md += f"- **{artist}** ({len(venues)} concert{'s' if len(venues) != 1 else ''})\n"
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(md)
        
        print(f"✓ Profile markdown saved to {output_path}")


def main():
    """Main entry point."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python3 music_profile_ingest.py <lastfm_api_key> <setlistfm_api_key>")
        sys.exit(1)
    
    lastfm_key = sys.argv[1]
    setlistfm_key = sys.argv[2]
    
    ingest = MusicProfileIngest(lastfm_key, setlistfm_key)
    ingest.ingest()
    ingest.save_json()
    ingest.generate_profile_markdown()
    
    print("\n✓ All done! Check the generated files in /var/home/mal/.zeroclaw/workspace/shared/")


if __name__ == "__main__":
    main()
