# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.2.0] - 2023-04-17
### Added
- PointingHandCursor to control components
- A viewer to view manga data
    - Title
    - Author
    - Description
    - Cover
    - Chapters
    - Genres
    - Status
- Initial MacOS "support" (uses GNU/Linux paths)

### Changed
- Update cx_Freeze version to 6.14.2
- Update all GitHub Actions workflows

### Removed
- Light theme

## [0.1.1] - 2022-05-12
### Added
- Windows executable icon
- [cx_Freeze](https://github.com/marcelotduarte/cx_Freeze) Python build script

### Removed
- Remove PyInstaller build script (When running on Windows, it's detected as a virus). See [this](https://github.com/pyinstaller/pyinstaller/issues/5932) issue for more information.
