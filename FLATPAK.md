Flatpak build and Flathub submission

Quick local build (x86_64):

```bash
sudo apt install flatpak-builder   # distro package name may vary
flatpak-builder --force-clean build-dir flatpak/org.joanisc.LoyaltyCardsOpen.json
flatpak-builder --run build-dir org.joanisc.LoyaltyCardsOpen
```

Notes:
- To build for `aarch64` you generally need an aarch64 build host or CI; Flathub's build infrastructure will build both architectures for you when you submit the manifest.
- Create a GitHub repository containing this project (or a copy) with the `flatpak/` manifest and `data/` metainfo file, then open a pull request to https://github.com/flathub/flathub following Flathub's app submission instructions: include the manifest at the repo root and the AppStream/metainfo file.

If you want, I can:
- Prepare a GitHub-ready repo layout and a PR branch for Flathub submission.
- Adjust the runtime version in `flatpak/org.joanisc.LoyaltyCardsOpen.json` to a different GNOME Platform if you prefer.
