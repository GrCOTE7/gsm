## [1.1.9](https://github.com/grcote7/gsm/compare/v1.1.8...v1.1.9) (2026-11-27)


### Bug Fixes

* declarative mode for main + ↑ ROADMAP ([f7273c4](https://github.com/grcote7/gsm/commit/f7273c4d6553d994cffcea72a44128aa5b8a2935))

## [1.1.8](https://github.com/grcote7/gsm/compare/v1.1.7...v1.1.8) (2026-11-25)


### Bug Fixes

* try 420 diag height ([a7d8a91](https://github.com/grcote7/gsm/commit/a7d8a91c2ce93a1807b6097ed65910667a240fe3))

## [1.1.7](https://github.com/grcote7/gsm/compare/v1.1.6...v1.1.7) (2026-11-25)


### Bug Fixes

* open links on Android (UrlLauncher) ([034abde](https://github.com/grcote7/gsm/commit/034abdedb3ce5ee70d74ff79b671d1ab9d8ad28f))

## [1.1.6](https://github.com/grcote7/gsm/compare/v1.1.5...v1.1.6) (2026-11-25)


### Bug Fixes

* set less height for diagnostic in test page ([09a4bdf](https://github.com/grcote7/gsm/commit/09a4bdf977443c602bfadc5e0ac8f847833f4e32))

## [1.1.5](https://github.com/grcote7/gsm/compare/v1.1.4...v1.1.5) (2026-11-25)


### Bug Fixes

* show the update card on the home page ([6154260](https://github.com/grcote7/gsm/commit/6154260f180c28d945bb1c76b1f35aab432369e4))

## [1.1.4](https://github.com/grcote7/gsm/compare/v1.1.3...v1.1.4) (2026-11-25)


### Bug Fixes

* add hand on menu burger icon ([92c5138](https://github.com/grcote7/gsm/commit/92c51382f72fd95c893249c75de13e7ffde875bb))

## [1.1.3](https://github.com/grcote7/gsm/compare/v1.1.2...v1.1.3) (2026-11-24)


### Bug Fixes

* start the Android app (explicit .env path) ([dac8060](https://github.com/grcote7/gsm/commit/dac806000965971d9c9e4e956d25c6203d9c43eb))

## [1.1.2](https://github.com/grcote7/gsm/compare/v1.1.1...v1.1.2) (2026-11-24)


### Bug Fixes

* **ci:** ship the release version inside the APK ([b6db232](https://github.com/grcote7/gsm/commit/b6db232d64ba1b8547cc2f54ed17df388f7a21ea))

## [1.1.1](https://github.com/grcote7/gsm/compare/v1.1.0...v1.1.1) (2026-11-24)


### Bug Fixes

* **ci:** unblock the release metadata sync rebase ([3e2237f](https://github.com/grcote7/gsm/commit/3e2237f0c1d7030e9581afb828939a6d33e47979))

# [1.1.0](https://github.com/grcote7/gsm/compare/v1.0.44...v1.1.0) (2026-11-24)


### Bug Fixes

* **ci:** clean the tree before the metadata rebase, sync 1.0.44 [skip ci] ([4d35b62](https://github.com/grcote7/gsm/commit/4d35b628d0870eccd2ed979dc85dfb85075570d6))
* **ui:** carry the hand cursor on a GestureDetector [skip ci] ([b73f6c5](https://github.com/grcote7/gsm/commit/b73f6c5f4f731f16d4131e2ed106f6b36383180b))
* **ui:** drop the invalid mouse_cursor kwarg that froze navigation [skip ci] ([89933b4](https://github.com/grcote7/gsm/commit/89933b44debb0f2073552b89ddbad51e83be0da2))
* **ui:** never read ft.context.page while rendering the brand [skip ci] ([109b42e](https://github.com/grcote7/gsm/commit/109b42ea23a42ba27d98f8f911d3a7c2ffd2dfab))


### Features

* **ui:** hand cursor on drawer entries that are not the current page [skip ci] ([36dc749](https://github.com/grcote7/gsm/commit/36dc749b1922c75efa8aad820b149ca3fdd0f118))
* **ui:** make the GSM brand clickable back to home [skip ci] ([2dda473](https://github.com/grcote7/gsm/commit/2dda4732eed19cb596e802f103f32d489c19d455))
* **ui:** show a hand cursor on the clickable GSM brand [skip ci] ([dd3d102](https://github.com/grcote7/gsm/commit/dd3d102f03a3d2068d1d3c868f1d25b3b72644a1))

## [1.0.44](https://github.com/grcote7/gsm/compare/v1.0.43...v1.0.44) (2026-11-24)


### Bug Fixes

* **ci:** autostash before the metadata rebase and sync 1.0.43 [skip ci] ([c5be7bf](https://github.com/grcote7/gsm/commit/c5be7bfb26383e0ce6aef3f7d17bf8b108a0f704))
* **diag:** read the app version from app_build.json ([88d088c](https://github.com/grcote7/gsm/commit/88d088c3995dd59c884f26c822c4ed721961b5b9))
* **go:** disable hot reload in web mode, it restart-looped the server [skip ci] ([ef718a3](https://github.com/grcote7/gsm/commit/ef718a34e82fb029afc3686448a9540577728eda))
* **go:** ignore pid files left by a closed CLI [skip ci] ([c2310b1](https://github.com/grcote7/gsm/commit/c2310b1f2b02ddd399ddbd0dd21c3ef69c6f871d))
* **go:** make the dedicated CLI visible, inheritable and diagnosable [skip ci] ([1c1cd94](https://github.com/grcote7/gsm/commit/1c1cd943acf3f3df72e5d4a446411d9efbbf12e8))
* **go:** repair the liveness query and launch the console directly [skip ci] ([d8961d3](https://github.com/grcote7/gsm/commit/d8961d367a6f3b69d9acd096446e8a39c8250ad5))
* **go:** target our own CLI window by title, ignore proxy processes [skip ci] ([4e73f01](https://github.com/grcote7/gsm/commit/4e73f01c1dc97220b448c7c328abb80a06dbd945))
* **go:** wait long enough for a cold Windows Terminal start [skip ci] ([350dfe8](https://github.com/grcote7/gsm/commit/350dfe8d1da5f567fc627fefb20ea86a9d14f072))
* **upu:** disable the startup update dialog too [skip ci] ([30852ce](https://github.com/grcote7/gsm/commit/30852cef591c380d1835defcc6ea78030c6b7bce))
* **upu:** hide the update card when UPU runs alone [skip ci] ([e48a4ae](https://github.com/grcote7/gsm/commit/e48a4aee37c806752b93f32987e7cecdb16ce9ef))
* **upu:** never show the release update card [skip ci] ([1ec93e0](https://github.com/grcote7/gsm/commit/1ec93e0aa85ea81704ab258ec134ccbd8ee23f1a))

## [1.0.43](https://github.com/grcote7/gsm/compare/v1.0.42...v1.0.43) (2026-11-24)


### Bug Fixes

* **ci:** let the release bot commit without husky hooks, sync 1.0.42 [skip ci] ([f421eb2](https://github.com/grcote7/gsm/commit/f421eb248aa25df305755cb493f49c3400cc7c11))
* **deploy:** rebuild the container and pin a flet-web compatible fastapi [skip ci] ([7e2af25](https://github.com/grcote7/gsm/commit/7e2af2591176d55bb7a43e97d52797e8b796d8df))
* **go:** never leave the user with nothing when the dedicated CLI fails ([f0df48f](https://github.com/grcote7/gsm/commit/f0df48fd5fbb1d426bc38158b5919c42ec799e5b))

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
