# Usage Guide

## Installation

1. **Clone Repository:**
    ```bash
    git clone https://github.com/TRAN-DANG-KHOA-IT/ Download_Video_Audio_Youtube.git
    ```

2. **Install Required Libraries:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Source Code:**
    ```bash
    python download.py
    ```

## How to Use

1. **Enter Storage Path:**
    - When prompted, enter the path where you want to save the videos or audios from YouTube.

2. **Select Download Type:**
    - Enter 'audio' if you want to download audio.
    - Enter 'video' if you want to download video.

3. **Enter YouTube Authentication Information:**
    - Provide the required cookie and authorization code requested from YouTube.

4. **Wait for the source to be downloaded from YouTube and download at the designated path.**

## Advanced Usage

- You can modify the `download_choice` variable in the main block of the script to set the default download option (audio or video) without prompting the user each time.
- Customize the output file naming and location by modifying the `outtmpl` parameter in the `download_youtube_audio` function for audio downloads and the `stream.download` function for video downloads.
- Feel free to explore and customize the script according to your needs. You can add error handling, logging, or additional functionality as required.

## Contributing
Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request on GitHub.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments
- This script was inspired by various YouTube downloader projects and libraries available on GitHub.
- Special thanks to the developers of PyTube, mutagen, and yt-dlp for providing excellent libraries to interact with YouTube and manipulate audio metadata.
