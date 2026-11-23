## [1.0.42](https://github.com/grcote7/gsm/compare/v1.0.41...v1.0.42) (2026-11-23)


### Bug Fixes

* **build:** drop flet-web from runtime deps, install it via the web extra [skip ci] ([5a786fc](https://github.com/grcote7/gsm/commit/5a786fc26d8a058a0a6604adb5e31e8089d71216))
* **build:** drop the temporary APK debug workflow and publish the flet 1.0 build ([0dc5dc4](https://github.com/grcote7/gsm/commit/0dc5dc4907ff14745b39079862020c1fa3241f60))
* **build:** keep CLI/desktop tooling out of the mobile bundle [skip ci] ([f005e86](https://github.com/grcote7/gsm/commit/f005e861cad899ab79e61b999fd38bcb5ac775de))
* **build:** pin jni 1.2 via tool.flet.flutter.pubspec [skip ci] ([1ad58a2](https://github.com/grcote7/gsm/commit/1ad58a26f694195fd25ceb78a8a2f1cbe462fe80))
* **build:** ship the flet 1.0 Android build fixes in a release ([8d596dd](https://github.com/grcote7/gsm/commit/8d596dd52032b10a304aa94ea30b2fb72cf0e300))

## [1.0.41](https://github.com/grcote7/gsm/compare/v1.0.40...v1.0.41) (2026-11-23)


### Bug Fixes

* remove committed merge conflicts and Python 2 syntax blocking the APK build ([e117d8f](https://github.com/grcote7/gsm/commit/e117d8f3ac18f203f3de4c48369eb85691eece81))

## [1.0.40](https://github.com/grcote7/gsm/compare/v1.0.39...v1.0.40) (2026-11-23)


### Bug Fixes

* **ci:** pin Flutter 3.44.8 required by flet 1.0.0 for the APK build ([10b1aac](https://github.com/grcote7/gsm/commit/10b1aace5cc73e311808be2baf49ea8621d13542))

## [1.0.39](https://github.com/grcote7/gsm/compare/v1.0.38...v1.0.39) (2026-11-23)


### Bug Fixes

* **ci:** fall back to an existing VPS SSH key secret for deploy ([9944469](https://github.com/grcote7/gsm/commit/994446954589166ffc26aef7c4346f92a62b9182))

## [1.0.38](https://github.com/grcote7/gsm/compare/v1.0.37...v1.0.38) (2026-11-23)


### Bug Fixes

* **release:** add missing src/gsm/app_data/app_build.json ([4f7a063](https://github.com/grcote7/gsm/commit/4f7a0636c90e930a492b87ae10f9bd30fee11808))

## [1.0.37](https://github.com/grcote7/gsm/compare/v1.0.36...v1.0.37) (2026-11-23)


### Bug Fixes

* **deps:** move pytest to dev extra (remove duplicate) ([d41b255](https://github.com/grcote7/gsm/commit/d41b2559031368df5d7021a52fea13b0bd992cea))
* **prod:** drop bind mounts, optimize Dockerfile layer caching ([8508010](https://github.com/grcote7/gsm/commit/85080109320f18a6237d8ec444cce4006bc97a87))
