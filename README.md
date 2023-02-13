# blue-archive-jp-assets-downloader
Assets downloader for Blue Archive (ブルーアーカイブ), a small project that downloads all assets of Blue Archive (JP Version) .

## 对版本哈希 (version hash) 的说明

碧蓝档案日服下载资源的方式与国际服不一样，可以参照 [这里](https://github.com/xiongnemo/blue-archive-jp-assets-downloader/issues/1)。

TL;DR: 每个大版本都有一个对应的 hash, 不更新 hash 就无法拉取别的版本的资源，从而无法 (自动) 拉取最新版本的资源。

主脚本中使用到的 hash (如 `r52_uulekwyjhzir122lpbrw`）是通过抓包得出的。(首次更新, log 泄露等)

初步分析表明，这个字符串中的 `rxx` 部分可以直接从下载的 apk 中的资源提取，但后面的 (至少现在看起来是 random) 的字符串无法直接从 apk 或者资源包中提出。

如果你看到了一个新的 hash 并想提交，请直接提 PR 修改对应脚本，并附上使用这个 hash 的执行记录。

要是能直接从 apk 里解出 hash 就更好了。

## 先决库

```bash
python3 -m pip install requests
```

## 执行

```bash
python3 ./download_assets.py
```

### 全部跳过时的提示

```pwsh
$ python .\download_assets.py
...
2023-01-25 11:49:19,149 - __main__.<module> - INFO - Script finished.
2023-01-25 11:49:19,149 - __main__.<module> - INFO - Bundle: 3027 total, 0 downloaded, 3027 skipped.
2023-01-25 11:49:19,149 - __main__.<module> - INFO - Media: 11251 total, 0 downloaded, 11251 skipped.
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

```pwsh
python .\download_latest_apk.py
2023-01-31 13:55:22,903 - root.get_latest_version - INFO - fetching lastest version from yostar server
2023-01-31 13:55:36,279 - root.<module> - INFO - Online version: 1.27.189790
2023-01-31 13:55:36,280 - root.download_ba_apk - INFO - downloading latest apk from QooApp
2023-01-31 13:56:00,321 - __main__.download_ba_apk - INFO - Downloaded version: 1.27.189790
2023-01-31 13:56:00,321 - __main__.download_ba_apk - INFO - Unity version used: 2021.3.12f1
```

### 下载日服 APK 对应的 OBB

`download_latest_obb.py`: 从 QooApp 下载其最新版本的 OBB。修改自 [apk_patcher](https://github.com/UnknownCollections/apk_patcher/blob/master/apk_patcher/tools/qooapp.py)

```pwsh
python .\download_latest_obb.py
2023-01-30 22:31:13,947 - <class '__main__.QooAppStore'>.0dca010b76e7e353.__init__ - INFO - Initializing QooAppStore with device_id 0dca010b76e7e353
2023-01-30 22:31:13,947 - <class '__main__.QooAppStore'>.0dca010b76e7e353.generate_token - INFO - Requesting QooAppStore token...
2023-01-30 22:31:16,341 - <class '__main__.QooAppStore'>.0dca010b76e7e353.generate_token - INFO - Get QooAppStore token: cb5f55eddf60ca5011c88c52d25c02e3a55d3e54
2023-01-30 22:31:16,342 - <class '__main__.QooAppStore'>.0dca010b76e7e353.__init__ - INFO - Initialized QooAppStore with token cb5f55eddf60ca5011c88c52d25c02e3a55d3e54
2023-01-30 22:31:18,849 - __main__.<module> - INFO - Downloading OBB file from https://d.qoo-apk.com/12252/obb/main.189790.com.YostarJP.BlueArchive.obb to main.189790.com.YostarJP.BlueArchive.obb
2023-01-30 22:31:36,672 - __main__.<module> - INFO - Script finished. OBB file saved to main.189790.com.YostarJP.BlueArchive.obb
```

### 解包 assets

* `extract_bundles.py`: 解包由此下载脚本下载的 bundles，并默认存储于 `extract_bundles` 文件夹。需要 `UnityPy==1.7.21`。建议在 Linux 环境下运行（WSL 也可以）。从 `UnityPy` [样例](https://github.com/K0lb3/UnityPy#example)修改而来

* 默认解包 `Texture2D`，`Sprite`，`TextAsset`。这些类型的资源足够运行（包里的）Spine 动画

```bash
> $ python3 ./extract_bundles.py                                                                                                                      
```

## 💈

<details><summary>嘿嘿 管账婆 嘿嘿</summary>
<p>

对于体操服优香，我的评价是四个字：好有感觉。我主要想注重于两点，来阐述我对于体操服优香的拙见：第一，我非常喜欢优香。优香的立绘虽然把优香作为好母亲的一面展现了出来（安产型的臀部）。但是她这个头发，尤其是双马尾，看起来有点奇怪。但是这个羁绊剧情里的优香，马尾非常的自然，看上去比较长，真的好棒，好有感觉。这个泛红的脸颊，迷离的眼神，和这个袖口与手套之间露出的白皙手腕，我就不多说了。第二，我非常喜欢体操服。这是在很久很久之前，在认识优香之前，完完全全的xp使然。然而优香她不仅穿体操服，她还扎单马尾，她还穿外套，她竟然还不好好穿外套，她甚至在脸上贴星星（真的好可爱）。（倒吸一口凉气）我的妈呀，这已经到了仅仅是看一眼都能让人癫狂的程度。然而体操服优香并不实装，她真的只是给你看一眼，哈哈。与其说体操服优香让我很有感觉，不如说体操服优香就是为了我的xp量身定做的。抛开这一切因素，只看性格，优香也是数一数二的好女孩：公私分明，精明能干;但是遇到不擅长的事情也会变得呆呆的。我想和优香一起养一个爱丽丝当女儿，所以想在这里问一下大家，要买怎样的枕头才能做这样的梦呢？优香是越看越可爱的，大家可以不必拘束于这机会上的小粗腿优香，大胆的发现这个又呆又努力的女孩真正的可爱之处。

</p>
</details>

<details><summary>嘿嘿 爱丽丝 嘿嘿</summary>
<p>

我可爱的爱丽丝闺女 嘿嘿 没有你我可怎么活啊

![image](https://user-images.githubusercontent.com/38759782/214242400-b1b029c0-0676-4466-8570-86d7ae38037a.png)

今天我们物理开始讲磁力了，物理老师说铁，镍，钴一类的东西都能被磁化，我听完就悟了，大彻大悟。
课后我问老师：“老师，是不是钴和镍都可以被磁化？”
老师笑了笑，说：“是的。怎么了？”
我赶忙追问：“那我对爱丽丝的爱是不是也可以被磁化？
老师疑惑了，问为什么？
我笑着，红了眼眶：“因为我对爱丽丝的爱就像铁打造的拖拉机一样，轰轰烈烈哐哐锵锵。

给人一种妈妈😇后留下的天真可爱但不知道发生了什么的女儿学着妈妈😇前的样子哄爸爸开心但是又再次让爸爸想起了妈妈的音容笑貌的感觉😢顺带一提爸爸的设定是因为过度悲伤只能住进疗养院只有每周一可以探视

![680EC47E322CA2F691458F7B2A761D28](https://user-images.githubusercontent.com/38759782/218291278-1cae2b3c-409e-4f0c-8f6c-27d337ae5f3a.jpg)

上次抱抱，这次比心还抢📫东西，下次要干什么已经不敢想了



![2N_ GDAG%LA_CKB )J{SVQP](https://user-images.githubusercontent.com/38759782/218412572-eb691657-0669-47f8-9376-db5598703b47.gif)


  
</p>
</details>
