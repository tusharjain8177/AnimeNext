import streamlit as st
import requests
import pandas as pd

def fetch_anime_recommendations():
    url = "https://api.jikan.moe/v4/recommendations/anime"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Check if we hit the rate limit
        if response.status_code == 429:
            st.error("Rate limit reached. Please wait a few seconds and try again.")
            return None
            
        data = response.json().get('data', [])
        if not data:
            st.warning("No recommendations found.")
            return None
            
        return data
    except requests.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None
    except ValueError as e:
        st.error("Error parsing response data")
        return None

def main():
    # Set page config and custom CSS
    st.set_page_config(
        page_title="AnimeNext",
        page_icon="🎬",
        layout="wide",
        menu_items={} # This removes menu items
    )

    # Custom CSS for better styling
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        :root {
            color-scheme: light dark;
        }
        /* Light mode colors */
        :root {
            --text-color: #1E1E1E;
            --bg-color: white;
            --box-shadow: rgba(0,0,0,0.1);
        }
        /* Dark mode colors */
        @media (prefers-color-scheme: dark) {
            :root {
                --text-color: #E1E1E1;
                --bg-color: #2E2E2E;
                --box-shadow: rgba(0,0,0,0.3);
            }
        }
        .stTitle {
            color: #FF4B4B;
            font-size: 3rem !important;
            text-align: center;
            margin-bottom: 2rem;
        }
        .anime-title {
            color: var(--text-color);
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 10px;
            text-align: center;
            background-color: var(--bg-color);
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 4px var(--box-shadow);
        }
        .truncate-title {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 200px;
            display: inline-block;
        }

        /* Loading Animation */
        .loading-spinner {
            width: 50px;
            height: 50px;
            border: 5px solid var(--bg-color);
            border-top: 5px solid #FF4B4B;
            border-radius: 50%;
            animation: spinner 1s linear infinite;
            margin: 20px auto;
        }
        
        .loading-text {
            text-align: center;
            color: #FF4B4B;
            font-size: 1.5rem;
            font-weight: bold;
            margin: 20px 0;
            animation: pulse 1.5s ease-in-out infinite;
        }
        
        @keyframes spinner {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @keyframes pulse {
            0% { opacity: 0.6; }
            50% { opacity: 1; }
            100% { opacity: 0.6; }
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Anime Recommendations")
    
    # Custom loading screen
    with st.spinner(""):  # Empty spinner to override default
        st.markdown("""
            <div class="loading-text">Loading Anime Recommendations</div>
            <div class="loading-spinner"></div>
        """, unsafe_allow_html=True)
        recommendations = fetch_anime_recommendations()
        # Hide the loading elements after data is fetched
        st.markdown("""
            <style>
                .loading-spinner, .loading-text { display: none; }
            </style>
        """, unsafe_allow_html=True)
    
    if recommendations:
        # Create rows of 3 columns
        for i in range(0, len(recommendations), 3):
            cols = st.columns(3)
            # Process up to 3 recommendations per row
            for j in range(3):
                if i + j < len(recommendations):
                    rec = recommendations[i + j]
                    with cols[j]:
                        st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
                        
                        # Image with border, shadow, and number overlay
                        st.markdown(f"""
                            <div style="position: relative; border: 2px solid #FF4B4B; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px var(--box-shadow); margin-bottom: 15px;">
                                <div style="position: absolute; top: 10px; left: 10px; background-color: var(--bg-color); padding: 5px 10px; border-radius: 5px; z-index: 1; box-shadow: 0 2px 4px var(--box-shadow);">
                                    <span style="color: #FF4B4B; font-weight: bold;">#{i + j + 1}</span>
                                </div>
                                <img src="{rec['entry'][0]['images']['jpg']['image_url']}" style="width: 100%; display: block;">
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Display anime titles with clickable links
                        st.markdown(f"""
                            <div class="anime-title">
                                <a href="https://myanimelist.net/anime/{rec['entry'][0]['mal_id']}" target="_blank" style="text-decoration: none; color: var(--text-color);">
                                    <span class="truncate-title">{rec['entry'][0]['title']}</span>
                                </a>
                                ➜
                                <a href="https://myanimelist.net/anime/{rec['entry'][1]['mal_id']}" target="_blank" style="text-decoration: none; color: var(--text-color);">
                                    <span class="truncate-title">{rec['entry'][1]['title']}</span>
                                </a>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 
