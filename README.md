# blue-archive-jp-assets-downloader
Assets downloader for Blue Archive (ブルーアーカイブ), a small project that downloads all assets of Blue Archive (JP Version) .

## 先决库

```bash
python3 -m pip install requests
```

## 执行

```bash
python3 ./download_assets.py
```

### 服务器维护时 (资源不可达) 可能会有的提示

```pwsh
$ python .\download_assets.py
2023-01-24 16:08:28,133 - __main__.<module> - INFO - Current version assets base url (AddressablesCatalogUrlRoot): https://prod-clientpatch.bluearchiveyostar.com/r52_1_27_uulekwyjhzir122lpbrw_2
2023-01-24 16:08:28,403 - root.<module> - WARNING - Provided AddressablesCatalog (https://prod-clientpatch.bluearchiveyostar.com/r52_1_27_uulekwyjhzir122lpbrw_2/Android/) is not accessible at this time.
2023-01-24 16:08:28,605 - root.<module> - WARNING - Provided MediaCatalog (https://prod-clientpatch.bluearchiveyostar.com/r52_1_27_uulekwyjhzir122lpbrw_2/MediaResources/) is not accessible at this time.
2023-01-24 16:08:28,605 - root.<module> - INFO - Script finished.
```

## 存储

`ba_jp_bundles` 文件夹是 Unity Bundle (AssetBundles?)

`ba_jp_media` 文件夹是媒体文件（过场 CG，音乐等）

## 辅助工具

### 下载日服 APK

`download_latest_apk.py`: 从 QooApp 下载其最新版本，并与官方做比照。修改自 [Blue-Archive---Asset-Downloader](https://github.com/K0lb3/Blue-Archive---Asset-Downloader)

```bash
> $ python3 ./download_latest_apk.py                                                                                                                      
Online version: 1.26.183658
Downliading latest apk from QooApp
Downloaded version: 1.26.183658
Unity version used: 2021.3.12f1
```

### 解包 assets

* `extract_bundles.py`: 解包由此下载脚本下载的 bundles，并默认存储于 `extract_bundles` 文件夹。需要 `UnityPy==1.7.21`。建议在 Linux 环境下运行（WSL 也可以）。从 `UnityPy` [样例](https://github.com/K0lb3/UnityPy#example)修改而来

* 默认解包 `Texture2D`，`Sprite`，`TextAsset`。这些类型的资源足够运行（包里的）Spine 动画

```bash
> $ python3 ./extract_bundles.py                                                                                                                      
```

## 💈

嘿嘿 爱丽丝 嘿嘿

我可爱的爱丽丝闺女 嘿嘿 没有你我可怎么活啊

对于体操服优香，我的评价是四个字：好有感觉。我主要想注重于两点，来阐述我对于体操服优香的拙见：第一，我非常喜欢优香。优香的立绘虽然把优香作为好母亲的一面展现了出来（安产型的臀部）。但是她这个头发，尤其是双马尾，看起来有点奇怪。但是这个羁绊剧情里的优香，马尾非常的自然，看上去比较长，真的好棒，好有感觉。这个泛红的脸颊，迷离的眼神，和这个袖口与手套之间露出的白皙手腕，我就不多说了。第二，我非常喜欢体操服。这是在很久很久之前，在认识优香之前，完完全全的xp使然。然而优香她不仅穿体操服，她还扎单马尾，她还穿外套，她竟然还不好好穿外套，她甚至在脸上贴星星（真的好可爱）。（倒吸一口凉气）我的妈呀，这已经到了仅仅是看一眼都能让人癫狂的程度。然而体操服优香并不实装，她真的只是给你看一眼，哈哈。与其说体操服优香让我很有感觉，不如说体操服优香就是为了我的xp量身定做的。抛开这一切因素，只看性格，优香也是数一数二的好女孩：公私分明，精明能干;但是遇到不擅长的事情也会变得呆呆的。我想和优香一起养一个爱丽丝当女儿，所以想在这里问一下大家，要买怎样的枕头才能做这样的梦呢？优香是越看越可爱的，大家可以不必拘束于这机会上的小粗腿优香，大胆的发现这个又呆又努力的女孩真正的可爱之处。

悲报：我们的📫妈妈完全没发现她的大闺女要寄了