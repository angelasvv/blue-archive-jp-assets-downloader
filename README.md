# blue-archive-jp-assets-downloader
Assets downloader for Blue Archive (ブルーアーカイブ), a small project that downloads all assets of Blue Archive (JP Version) .

## **免责声明/Disclaimer**

<details><summary>官方说明</summary>
<p>

根据[日服官方推特](https://twitter.com/Blue_ArchiveJP/status/1633361958916456448)于今日下午（2023-03-08T15:00+0800）的声明：

> 【重要なお知らせ】
>「ブルーアーカイブ」の非公開情報を不正に取得し、SNSなどで情報を広める(リーク)行為に関するお知らせを掲載いたします。
>
>リークは禁止行為ですので、今後発見した場合、法的措置を含めた厳しい対応を検討いたします。

[详细说明](https://bluearchive.jp/news/newsJump/295)：

> 現在、通常のご利用では取得できない非公開情報を不正に抜き取り、該当情報をリーク(※注1)する行為が確認されています。
>
> リーク行為は、運営スケジュールの進行に支障をきたすだけではなく、何よりゲーム内の演出や展開を期待していただいている皆様の体験を損なうことに繋がります。
>
> 今後、リーク行為を発見した場合、法的措置を含めた厳しい対応を検討いたします。
>
>
>
> 「ブルーアーカイブ」運営チームといたしましては、先生の皆様の期待、喜び、そして感動といった体験を大切にしたいと考えております。
>
> これからも先生の皆様に、感動できる様々な体験をご提供することを目指しながら、日々不正行為を監視し、その貴重な体験が損なわれないよう努めてまいります。
>
> ※注1
>
> リーク行為とは、正式公開前にデータの解析など、利用規約に違反する手段で、ゲーム内データ、およびコンテンツを不正に取得し、SNS等で拡散する不正行為を指します。
>
> また、非公開情報にはゲーム内の生徒画像、パラメーター、3Dモデル、あらゆる画像、音楽、映像およびテクスチャ、データテーブルなど通常のご利用では取得できないものが含まれております。

</p>
</details>


**The relevant content of this repo involves the actual interests of Nexon/Yostar. This repo and code are meant for learning and research purposes on mobile platforms only. Do not use this tool for commercial or illegal purposes, or publish anything related to 非公開情報 in public places (SNS, etc.).  Do as you please with it, but accept any and all responsibility for your actions.**

**本仓库相关内容已涉及 Nexon/Yostar 的实际利益。本仓库仅用于移动应用安全研究与学习。请勿将此工具用于商业或者非法用途，或在公开场合（SNS 等）发布任何和非公開情報有关系的事物。如果阁下愿意继续阅读，请您承诺将为自己的全部行为负责。**

~~把寿司人打鸡斯拉的感动还给我~~

## 对版本哈希 (version hash) 的说明

碧蓝档案日服下载资源的方式与国际服不一样，可以参照 [这里](https://github.com/xiongnemo/blue-archive-jp-assets-downloader/issues/1)。

TL;DR: 每个大版本都有一个对应的 hash, 不更新 hash 就无法拉取别的版本的资源，从而无法 (自动) 拉取最新版本的资源。

主脚本中使用到的 hash （如 `r52_uulekwyjhzir122lpbrw`）是通过抓包得出的。(首次更新, log 泄露等)

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
2023-02-17 09:42:18,684 - __main__.<module> - INFO - Script finished.
2023-02-17 09:42:18,684 - __main__.<module> - INFO - Bundle: 3057 total, 0 downloaded, 3057 skipped.
2023-02-17 09:42:18,685 - __main__.<module> - INFO - Media: 11325 total, 0 downloaded, 11325 skipped.
2023-02-17 09:42:18,685 - __main__.<module> - INFO - table: 240 total, 0 downloaded, 240 skipped.
```

### 服务器维护时 (资源不可达) 可能会有的提示

```pwsh
$ py .\download_assets.py
2023-03-08 15:37:27,052 - __main__.<module> - INFO - Current version assets base url (AddressablesCatalogUrlRoot): https://prod-clientpatch.bluearchiveyostar.com/r53_1_29_k9al0rwmplkqmj9cn3ap
2023-03-08 15:37:27,322 - __main__.<module> - WARNING - Provided AddressablesCatalog (https://prod-clientpatch.bluearchiveyostar.com/r53_1_29_k9al0rwmplkqmj9cn3ap/Android/) is not accessible at this time.
2023-03-08 15:37:27,578 - __main__.<module> - WARNING - Provided MediaCatalog (https://prod-clientpatch.bluearchiveyostar.com/r53_1_29_k9al0rwmplkqmj9cn3ap/MediaResources/) is not accessible at this time.
2023-03-08 15:37:27,783 - __main__.<module> - WARNING - TableCatalog (https://prod-clientpatch.bluearchiveyostar.com/r53_1_29_k9al0rwmplkqmj9cn3ap/TableBundles/TableCatalog.json) is not accessible at this time.
2023-03-08 15:37:27,783 - __main__.<module> - INFO - Script finished.
```

## 存储

`ba_jp_bundles` 文件夹是 Unity Bundle (AssetBundles)

`ba_jp_media` 文件夹是媒体文件（预渲染的过场 CG，音乐等）

`ba_jp_table` 文件夹是加密的几乎所有游戏文本资源（剧情文本，数值，技能等）（TableBundle）

## 辅助工具

<details><summary>展开</summary>
<p>

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

* `extract_bundles.py`: 解包由此下载脚本下载的 bundles，并默认存储于 `ba_jp_bundles_extracted` 文件夹。需要 `UnityPy==1.9.26`。从 `UnityPy` [样例](https://github.com/K0lb3/UnityPy#example)修改而来

* 默认解包 `Texture2D`，`Sprite`，`TextAsset`，`MonoBehaviour`。前三者足够运行（包里的）Spine 动画。

```bash
> $ python3 ./extract_bundles.py
```

### 解包 TableBundles

* `extract_table_bundles`: 解包由此下载脚本下载的 TableBundles，并默认存储于 `ba_jp_table_extracted` 文件夹。需要 `xxhash`。`MersenneTwister` 的实现从 [Blue-Archive---Asset-Downloader](https://github.com/K0lb3/Blue-Archive---Asset-Downloader/blob/main/lib/MersenneTwister.py) 借用。


```pwsh
python .\extract_table_bundles.py
2023-03-01 08:43:50,811 - root.unzip_all_table_bundles - INFO - Loading from D:\UserData\Documents\GitHub\blue-archive-jp-assets-downloader\ba_jp_table\Battle.zip
2023-03-01 08:43:50,813 - root.unzip_all_table_bundles - INFO - Reading animationmappingdata.json from D:\UserData\Documents\GitHub\blue-archive-jp-assets-downloader\ba_jp_table\Battle.zip
2023-03-01 08:43:50,815 - root.unzip_all_table_bundles - INFO - Extracting animationmappingdata.json to D:\UserData\Documents\GitHub\blue-archive-jp-assets-downloader\ba_jp_table_extracted\Battle
2023-03-01 08:43:50,815 - root.unzip_all_table_bundles - INFO - Extracted animationmappingdata.json to D:\UserData\Documents\GitHub\blue-archive-jp-assets-downloader\ba_jp_table_extracted\Battle\animationmappingdata.json
2023-03-01 08:43:50,815 - root.unzip_all_table_bundles - INFO - Reading logiceffectdata.json from D:\UserData\Documents\GitHub\blue-archive-jp-assets-downloader\ba_jp_table\Battle.zip
...
```
### 合并视频与音轨

* 由 [lwd-temp](https://github.com/lwd-temp) 在 [pr/6](https://github.com/xiongnemo/blue-archive-jp-assets-downloader/pull/6) 中提供。
* `combine_videos.py`: 合并由此下载脚本下载的视频文件（因为视频和音轨是分开存放的），并默认存储于 `ba_jp_media_combined` 文件夹。需要 `ffmpeg-python`。

```pwsh
py .\combine_videos.py        
2023-03-16 21:40:13,083 - root.match_files - INFO - Found ba_jp_media\Cafe\PV\PV_1_Sound.ogg for ba_jp_media\Cafe\PV\PV_1_Video.mp4, score 5
2023-03-16 21:40:13,126 - root.match_files - INFO - Found ba_jp_media\Cafe\PV\PV_2_Sound.ogg for ba_jp_media\Cafe\PV\PV_2_Video.mp4, score 5
2023-03-16 21:40:13,169 - root.match_files - INFO - Found ba_jp_media\Cafe\PV\PV_3_Sound.ogg for ba_jp_media\Cafe\PV\PV_3_Video.mp4, score 5
2023-03-16 21:40:13,212 - root.match_files - INFO - Found ba_jp_media\Cafe\PV\PV_4_Sound.ogg for ba_jp_media\Cafe\PV\PV_4_Video.mp4, score 5
2023-03-16 21:40:13,258 - root.match_files - INFO - Found ba_jp_media\Scenario\Event\10000_Title_Sound.ogg for ba_jp_media\Scenario\Event\10000_Title_Video.mp4, score 12
2023-03-16 21:40:13,304 - root.match_files - INFO - Found ba_jp_media\Scenario\Event\10001_Title_Sound.ogg for ba_jp_media\Scenario\Event\10001_Title_Video.mp4, score 12
2023-03-16 21:40:13,350 - root.match_files - INFO - Found ba_jp_media\Scenario\Event\10002_Title_Sound.ogg for ba_jp_media\Scenario\Event\10002_Title_Video.mp4, score 12
2023-03-16 21:40:13,396 - root.match_files - INFO - Found ba_jp_media\Scenario\Event\10003_Title_Sound.ogg for ba_jp_media\Scenario\Event\10003_Title_Video.mp4, score 12
2023-03-16 21:40:13,441 - root.match_files - INFO - Found ba_jp_media\Scenario\Event\10004_Title_Sound.ogg for ba_jp_media\Scenario\Event\10004_Title_Video.mp4, score 12
2023-03-16 21:40:13,487 - root.match_files - INFO - Found ba_jp_media\Scenario\Event\10005_Title_Sound.ogg for ba_jp_media\Scenario\Event\10005_Title_Video.mp4, score 12
2023-03-16 21:40:13,535 - root.match_files - INFO - Found ba_jp_media\Scenario\Event\10006_Title_Sound.ogg for ba_jp_media\Scenario\Event\10006_Title_Video.mp4, score 12
2023-03-16 21:40:13,581 - root.match_files - INFO - Found ba_jp_media\Scenario\Event\10007_Title_Sound.ogg for ba_jp_media\Scenario\Event\10007_Title_Video.mp4, score 12
2023-03-16 21:40:13,627 - root.match_files - INFO - Found ba_jp_media\Scenario\Event\10008_Title_Sound.ogg for ba_jp_media\Scenario\Event\10008_Title_Video.mp4, score 12
2023-03-16 21:40:13,673 - root.match_files - INFO - Found ba_jp_media\Scenario\Event\10009_Title_Sound.ogg for ba_jp_media\Scenario\Event\10009_Title_Video.mp4, score 12
2023-03-16 21:40:13,719 - root.match_files - INFO - Found ba_jp_media\Scenario\Event\10010_Title_Sound.ogg for ba_jp_media\Scenario\Event\10010_Title_Video.mp4, score 12
2023-03-16 21:40:13,765 - root.match_files - INFO - Found ba_jp_media\Scenario\Event\10011_Title_Sound.ogg for ba_jp_media\Scenario\Event\10011_Title_Video.mp4, score 12
2023-03-16 21:40:13,811 - root.match_files - INFO - Found ba_jp_media\Scenario\Event\10012_Title_Sound.ogg for ba_jp_media\Scenario\Event\10012_Title_Video.mp4, score 12
2023-03-16 21:40:13,857 - root.match_files - INFO - Found ba_jp_media\Scenario\Event\10013_Title_Sound.ogg for ba_jp_media\Scenario\Event\10013_Title_Video.mp4, score 12
2023-03-16 21:40:13,903 - root.match_files - INFO - Found ba_jp_media\Scenario\Event\10014_Title_Sound.ogg for ba_jp_media\Scenario\Event\10014_Title_Video.mp4, score 12
2023-03-16 21:40:13,948 - root.match_files - INFO - Found ba_jp_media\Scenario\Event\10015_Title_Sound.ogg for ba_jp_media\Scenario\Event\10015_Title_Video.mp4, score 12
2023-03-16 21:40:13,999 - root.match_files - INFO - Found ba_jp_media\Scenario\Event\10016_Title_Sound.ogg for ba_jp_media\Scenario\Event\10016_Title_Video.mp4, score 12
2023-03-16 21:40:14,045 - root.match_files - INFO - Found ba_jp_media\Scenario\Event\10017_Title_Sound.ogg for ba_jp_media\Scenario\Event\10017_Title_Video.mp4, score 12
2023-03-16 21:40:14,092 - root.match_files - INFO - Found ba_jp_media\Scenario\Event\10018_Title_Sound.ogg for ba_jp_media\Scenario\Event\10018_Title_Video.mp4, score 12
2023-03-16 21:40:14,137 - root.match_files - INFO - Found ba_jp_media\Scenario\Main\104000_ED_Sound.ogg for ba_jp_media\Scenario\Main\104000_ED_Video.mp4, score 10
2023-03-16 21:40:14,181 - root.match_files - INFO - Found ba_jp_media\Scenario\Main\22000_MV_Sound.ogg for ba_jp_media\Scenario\Main\22000_MV_Video.mp4, score 9
2023-03-16 21:40:14,227 - root.match_files - INFO - Found ba_jp_media\Scenario\Main\Test_01_Sound.ogg for ba_jp_media\Scenario\Main\Test_01_Video.mp4, score 8
2023-03-16 21:40:18,925 - root.match_files - INFO - Found ba_jp_media\Audio\Videos\pv-a.ogg for ba_jp_media\Video\pv-v.mp4, score 3
2023-03-16 21:40:18,925 - root.combine_and_output - INFO - Combining ba_jp_media\Cafe\PV\PV_1_Video.mp4 and ba_jp_media\Cafe\PV\PV_1_Sound.ogg to ba_jp_media_combined\PV_1_Video.mp4
ffmpeg version 6.0-full_build-www.gyan.dev Copyright (c) 2000-2023 the FFmpeg developers
...
```

</p>
</details>

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

最害怕的一集

![image](https://user-images.githubusercontent.com/38759782/221453505-a0da27ad-6d89-40fa-afcb-ee7cf72abb14.png)

  
</p>
</details>
