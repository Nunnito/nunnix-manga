# Nunnix Manga
> Manga reader written in Python.
 
![CI](https://github.com/nunnito/nunnix-manga/actions/workflows/python-lint-pytest.yml/badge.svg)
![Linux build](https://github.com/nunnito/nunnix-manga/actions/workflows/linux-build.yml/badge.svg)
![Windows build](https://github.com/nunnito/nunnix-manga/actions/workflows/windows-build.yml/badge.svg)
[![stable release](https://img.shields.io/github/v/release/nunnito/nunnix-manga?include_prereleases&label=download)](https://github.com/nunnito/nunnix-manga/releases)

Nunnix Manga is a free and open-source manga reader written in Python.

This is a early alpha release. Bugs are expected. Currently only works the explorer with MangaDex and ManagaKatana.

For futures features, see the [TODO list](#todo-list)


![](https://i.imgur.com/LaUypU3.jpg)


## Installation
### Using Windows binaries
- Download the latest release from [here](https://github.com/nunnito/nunnix-manga/releases/download/v0.1.0/Nunnix-Manga-Windows-x86_64.zip)
- Unzip the file
- Run `nunnix-manga.bat` file

### Using Linux binaries
```bash
# Download the latest release
curl -OL https://github.com/nunnito/nunnix-manga/releases/download/v0.1.0/Nunnix-Manga-Linux-x86_64.AppImage

# Give executable permissions
chmod +x Nunnix-Manga-Linux-x86_64.AppImage

# Run the application
./Nunnix-Manga-Linux-x86_64.AppImage
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
- [ ] Data viewer, this contains the manga information
- [ ] Reader, this contains the manga viewer
- [ ] Library, where you can store your manga
- [ ] Downloader, where it will download the manga
- [ ] History, where you can see your history
- [ ] Settings, where you can change the application settings
- [ ] Import from local storage
- [ ] Export to PDF, EPUB and CBZ
- [ ] Better light theme
