# Nunnix Manga
> Manga reader written in Python.
 
![CI](https://github.com/nunnito/nunnix-manga/actions/workflows/python-lint-pytest.yml/badge.svg)
![Linux build](https://github.com/nunnito/nunnix-manga/actions/workflows/linux-build.yml/badge.svg)
![Windows build](https://github.com/nunnito/nunnix-manga/actions/workflows/windows-build.yml/badge.svg)
[![stable release](https://img.shields.io/github/v/release/nunnito/nunnix-manga?include_prereleases&label=download)](https://github.com/nunnito/nunnix-manga/releases)
![total downloads](https://img.shields.io/github/downloads/nunnito/nunnix-manga/total?label=total%20downloads)

Nunnix Manga is a free and open-source manga reader written in Python.

This is an early alpha release. Bugs are expected. Currently only the browser and manga viewer (not the reader) are working.

For futures features, see the [TODO list](#todo-list)


![](https://i.imgur.com/LaUypU3.jpg)
![](https://i.imgur.com/hkubjYp.png)


## Installation
### Using Windows binaries
- Download the latest release from [here](https://github.com/nunnito/nunnix-manga/releases/latest/download/Nunnix_Manga_v0.2.0_win64.zip)
- Unzip the file
- Run `Nunnix-Manga.exe` file

### Using Linux binaries
```bash
# Download the latest release
curl -OL https://github.com/nunnito/nunnix-manga/releases/latest/download/Nunnix-Manga_v0.2.0_linux64.AppImage

# Give executable permissions
chmod +x Nunnix-Manga_v0.2.0_linux64.AppImage

# Run the application
./Nunnix-Manga_v0.2.0_linux64.AppImage
```

### Using Python (3.10+)
If you are using MacOS, you can install the application using the following command:
```bash
# Clone the repository
git clone https://github.com/nunnito/nunnix-manga.git

# Change directory to the cloned repository
cd nunnix-manga

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 app/main.py
```

## TODO list
- [x] Explorer, this contains the search engine
- [x] Data viewer, this contains the manga information
- [ ] Reader, this contains the manga reader
- [ ] Library, where you can store your manga
- [ ] Downloader, where it will download the manga
- [ ] History, where you can see your history
- [ ] Settings, where you can change the application settings
- [ ] Import from local storage
- [ ] Export to PDF, EPUB and CBZ
- [ ] Light theme
