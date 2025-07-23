from typing import Tuple
import requests
import logging
import os
import json

# set current version from environ
current_version = os.environ.get('BA_JP_CURRENT_VERSION', None)
if not current_version:
    current_version = 'r82_59_hhfkpxf94r4f9sgct1y9'

# set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# set up requests session
session = requests.Session()

# set up constants
BA_JP_BUNDLES_DIR = os.path.join(os.path.dirname(__file__), 'ba_jp_bundles')
BA_JP_PATCHPACK_DIR = os.path.join(os.path.dirname(__file__), current_version + '_ba_jp_patchpack')
BA_JP_MEDIA_DIR = os.path.join(os.path.dirname(__file__), 'ba_jp_media')
BA_JP_TABLE_DIR = os.path.join(os.path.dirname(__file__), 'ba_jp_table')
dirs = [BA_JP_BUNDLES_DIR, BA_JP_MEDIA_DIR, BA_JP_TABLE_DIR, BA_JP_PATCHPACK_DIR]

BA_JP_VERSION_METADATA_TEMPLATE = "https://yostar-serverinfo.bluearchiveyostar.com/{}.json"

BA_JP_ANDROID_BUNDLE_DOWNLOAD_INFO_TEMPLATE = '{}/Android/bundleDownloadInfo.json'
BA_JP_ANDROID_BUNDLE_BASEURL_TEMPLATE = '{}/Android/'
#PATCH PACK#
BA_JP_ANDROID_PATCH_PACK_BASEURL_TEMPLATE = '{}/Android_PatchPack/'
BA_JP_ANDROID_PATCH_PACK_TEMPLATE = '{}/Android_PatchPack/BundlePackingInfo.json'

BA_JP_IOS_BUNDLE_DOWNLOAD_INFO_TEMPLATE = '{}/iOS/bundleDownloadInfo.json'
BA_JP_IOS_BUNDLE_BASEURL_TEMPLATE = '{}/iOS/'
BA_JP_MEDIA_CATALOG_TEMPLATE = '{}/MediaResources/MediaCatalog.json'
BA_JP_MEDIA_BASEURL_TEMPLATE = '{}/MediaResources/'
BA_JP_TABLE_BUNDLES_CATALOG_TEMPLATE = '{}/TableBundles/TableCatalog.json'
BA_JP_TABLE_BUNDLES_BASEURL_TEMPLATE = '{}/TableBundles/'

# create download directories
for d in dirs:
    os.makedirs(d, exist_ok=True)


def download_ba_jp_bundle(bundle_base_url: str, bundles: list, output_dir: str) -> Tuple[int, int, int]:
    '''
    returns:
        bundle count given, 
        downloaded,
        skipped
    '''
    downloaded_count = 0
    skipped_count = 0
    for bundle in bundles:
        bundle_name = bundle['Name']
        url = f'{bundle_base_url}{bundle_name}'
        bundle_local_path = os.path.join(output_dir, bundle_name)
        if not (os.path.exists(bundle_local_path) and os.path.getsize(bundle_local_path) == bundle["Size"]):
            logger.info(f'Downloading {bundle_name} from {url}')
            data = session.get(url).content
            with open(bundle_local_path, "wb") as f:
                f.write(data)
            if len(data) != bundle["Size"]:
                logger.warn(
                    f'Size mismatch for {bundle_name}: {len(data)}, should be {bundle["Size"]}')
            logger.info(f'{bundle_name} written to {bundle_local_path}')
            downloaded_count += 1
        else:
            logger.info(f'Skipping {bundle_name} as it already exists')
            skipped_count += 1
    return len(bundles), downloaded_count, skipped_count
    
def download_ba_jp_patchpack(patchpack_base_url: str, patchpack_data: dict, output_dir: str) -> Tuple[int, int, int]:
    '''
    returns:
        bundle count given, 
        downloaded,
        skipped
    '''
    downloaded_count = 0
    skipped_count = 0
    total_count = 0

    for pack in patchpack_data.get("FullPatchPacks", []):
        pack_name = pack.get("PackName")
        pack_size = pack.get("PackSize")

        if not pack_name.lower().endswith('.zip'):
            continue  # skipped

        total_count += 1
        zip_url = f"{patchpack_base_url}{pack_name}"
        zip_local_path = os.path.join(output_dir, pack_name)

        if not (os.path.exists(zip_local_path) and os.path.getsize(zip_local_path) == pack_size):
            logger.info(f'Downloading FullPatch zip: {pack_name} from {zip_url}')
            data = session.get(zip_url).content
            with open(zip_local_path, "wb") as f:
                f.write(data)
            if len(data) != pack_size:
                logger.warning(f'Size mismatch for {pack_name}: got {len(data)} bytes, expected {pack_size}')
            downloaded_count += 1
        else:
            logger.info(f'Skipping FullPatch zip {pack_name} (already exists)')
            skipped_count += 1

    return total_count, downloaded_count, skipped_count

def download_ba_jp_media(media_base_url: str, media_list: dict, output_dir: str) -> Tuple[int, int, int]:
    '''
    returns:
        media count given, 
        downloaded,
        skipped
    '''
    downloaded_count = 0
    skipped_count = 0
    for media_key in media_list:
        media = media_list[media_key]
        media_name = media['FileName']
        media_path = media['path']
        media_local_path = os.path.join(output_dir, media_path)
        url = f'{media_base_url}{media_path}'
        if not (os.path.exists(media_local_path) and os.path.getsize(media_local_path) == media["bytes"]):
            logger.info(f'Downloading {media_name} from {url}')
            try:
                os.remove(media_local_path)
            except:
                pass
            os.makedirs(media_local_path, exist_ok=True)
            os.rmdir(media_local_path)
            data = session.get(url).content
            with open(media_local_path, "wb") as f:
                f.write(data)
            logger.info(f'{media_name} written to {media_local_path}')
            downloaded_count += 1
        else:
            logger.info(f'Skipping {media_name} as it already exists')
            skipped_count += 1
    return len(media_list), downloaded_count, skipped_count


def download_ba_jp_table(table_base_url: str, table_list: dict, output_dir: str) -> Tuple[int, int, int]:
    '''
    returns:
        table count given, 
        downloaded,
        skipped
    '''
    downloaded_count = 0
    skipped_count = 0
    for table_key in table_list:
        # here, table_key is the table name
        table = table_list[table_key]
        table_name = table['Name']
        table_local_path = os.path.join(output_dir, table_name)
        url = f'{table_base_url}{table_name}'
        if not (os.path.exists(table_local_path) and os.path.getsize(table_local_path) == table["Size"]):
            logger.info(f'Downloading {table_name} from {url}')
            data = session.get(url).content
            with open(table_local_path, "wb") as f:
                f.write(data)
            logger.info(f'{table_name} written to {table_local_path}')
            downloaded_count += 1
        else:
            logger.info(f'Skipping {table_name} as it already exists')
            skipped_count += 1
    return len(table_list), downloaded_count, skipped_count


current_version_assets_base_url = requests.get(BA_JP_VERSION_METADATA_TEMPLATE.format(current_version)).json()[
    "ConnectionGroups"][0]['OverrideConnectionGroups'][-1]['AddressablesCatalogUrlRoot']
logger.info('Current version assets base url (AddressablesCatalogUrlRoot): %s',
            current_version_assets_base_url)

# Default to Android
# {
#     "BundleFiles": [
#         {
#             "Name": "academy-_mxload-2022-05-12_assets_all_27d6f05dabf78e6cee7239a72935fc72.bundle",
#             "Size": 1182569,
#             "IsInbuild": false,
#             "Crc": 789432595
#         },
#         ...
#     ]
# }
#BUNDLE#
def process_android_bundles():
    try:
        bundles_request = requests.get(BA_JP_ANDROID_BUNDLE_DOWNLOAD_INFO_TEMPLATE.format(
            current_version_assets_base_url))
        bundles_to_download = bundles_request.json()['BundleFiles']
        total_bundle_count, downloaded_bundle_count, skipped_bundle_count = download_ba_jp_bundle(BA_JP_ANDROID_BUNDLE_BASEURL_TEMPLATE.format(
            current_version_assets_base_url), bundles_to_download, BA_JP_BUNDLES_DIR)
    except:
        # should check if the status code is 403
        if bundles_request.status_code == 403:
            logger.warning(
                f'Provided AddressablesCatalog ({BA_JP_ANDROID_BUNDLE_BASEURL_TEMPLATE.format(current_version_assets_base_url)}) is not accessible at this time.')
        else:
            logger.warning(
                f'Unexpected exception raised while handling provided AddressablesCatalog ({BA_JP_ANDROID_BUNDLE_BASEURL_TEMPLATE.format(current_version_assets_base_url)}).')
            import traceback
            logger.error(traceback.format_exc())
#BUNDLE#

# {
    # "Milestone": "r82",
    # "PatchVersion": 0,
    # "FullPatchPacks": [{
            # "PackName": "FullPatch_000.zip",
            # "PackSize": 52801904,
            # "Crc": 2081377421,
            # "IsPrologue": false,
            # "IsSplitDownload": false,
            # "BundleFiles": [{
                    # "Name": "academy-_mxload-prefabs-2025-07-02_assets_all_1923138029.bundle",
                    # "Size": 1926340,
                    # "IsPrologue": false,
                    # "Crc": 1923138029,
                    # "IsSplitDownload": false
                # }
            # ]
        # }
    # ],
    # "UpdatePacks": []
# }

#PATCH PACK#
def process_patchpack():
    try:
        patch_pack_url = BA_JP_ANDROID_PATCH_PACK_TEMPLATE.format(current_version_assets_base_url)
        patch_pack_request = requests.get(patch_pack_url)
        patch_pack_request.raise_for_status()  # HTTPError
        patch_pack_json = patch_pack_request.json()

        # Download BundlePackingInfo.json
        patchpack_info_path = os.path.join(BA_JP_PATCHPACK_DIR, 'BundlePackingInfo.json')
        with open(patchpack_info_path, 'w', encoding='utf-8') as f:
            json.dump(patch_pack_json, f, indent=4, ensure_ascii=False)

        logger.info(f'BundlePackingInfo.json saved to: {patchpack_info_path}')

        # Download zip
        total_patch_bundle, downloaded_patch_bundle, skipped_patch_bundle = download_ba_jp_patchpack(
            BA_JP_ANDROID_PATCH_PACK_BASEURL_TEMPLATE.format(current_version_assets_base_url),
            patch_pack_json,
            BA_JP_PATCHPACK_DIR
        )

    except:
        # should check if the status code is 403
        if bundles_request.status_code == 403:
            logger.warning(
                f'Provided AddressablesCatalog ({BA_JP_ANDROID_PATCH_PACK_BASEURL_TEMPLATE.format(current_version_assets_base_url)}) is not accessible at this time.')
        else:
            logger.warning(
                f'Unexpected exception raised while handling provided AddressablesCatalog ({BA_JP_ANDROID_PATCH_PACK_BASEURL_TEMPLATE.format(current_version_assets_base_url)}).')
            import traceback
            logger.error(traceback.format_exc())
#PATCH PACK#

# {
#     "Table": {
#         "audio/bgm/bgm_mikumikuni": {
#             "isChanged": false,
#             "mediaType": 1,
#             "path": "Audio/BGM/BGM_Mikumikuni.ogg",
#             "fileName": "BGM_Mikumikuni.ogg",
#             "bytes": 891648,
#             "Crc": 27073415,
#             "isInbuild": false
#         },
#         ...
#     }
# }

#MEDIA#
def process_media():
    try:
        media_request = requests.get(BA_JP_MEDIA_CATALOG_TEMPLATE.format(
            current_version_assets_base_url))
        media_to_download = media_request.json()['Table']
        total_media_count, downloaded_media_count, skipped_media_count = download_ba_jp_media(BA_JP_MEDIA_BASEURL_TEMPLATE.format(
            current_version_assets_base_url), media_to_download, BA_JP_MEDIA_DIR)
    except:
        # should check if the status code is 403
        if media_request.status_code == 403:
            logger.warning(
                f'Provided MediaCatalog ({BA_JP_ANDROID_BUNDLE_BASEURL_TEMPLATE.format(current_version_assets_base_url)}) is not accessible at this time.')
        else:
            logger.warning(
                f'Unexpected exception raised while handling provided MediaCatalog ({BA_JP_ANDROID_BUNDLE_BASEURL_TEMPLATE.format(current_version_assets_base_url)}).')
            import traceback
            logger.error(traceback.format_exc())
#MEDIA#

# {
#     "Table": {
#         "Excel.zip": {
#             "Name": "Excel.zip",
#             "Size": 72025333,
#             "Crc": 875393033,
#             "isInbuild": false,
#             "isChanged": false,
#             "Includes": [
#                 "rawdata/table/excel/academyfavorscheduleexceltable.bytes",
#                 "rawdata/table/excel/academylocationexceltable.bytes",
#                 "rawdata/table/excel/academylocationrankexceltable.bytes",
#                 "rawdata/table/excel/academymessanger1exceltable.bytes",
#                 "rawdata/table/excel/academymessanger2exceltable.bytes",
#                 ...
#            ]
#         },
#         ...
#     },
#    "BundleMap": null
# }

#TABLE#
def process_table():
    try:
        table_request = requests.get(BA_JP_TABLE_BUNDLES_CATALOG_TEMPLATE.format(
            current_version_assets_base_url))
        table_to_download = table_request.json()['Table']
        total_table_count, downloaded_table_count, skipped_table_count = download_ba_jp_table(BA_JP_TABLE_BUNDLES_BASEURL_TEMPLATE.format(
            current_version_assets_base_url), table_to_download, BA_JP_TABLE_DIR)
    except:
        # should check if the status code is 403
        if table_request.status_code == 403:
            logger.warning(
                f'Provided TableCatalog ({BA_JP_ANDROID_BUNDLE_BASEURL_TEMPLATE.format(current_version_assets_base_url)}) is not accessible at this time.')
        else:
            logger.warning(
                f'Unexpected exception raised while handling provided TableCatalog ({BA_JP_ANDROID_BUNDLE_BASEURL_TEMPLATE.format(current_version_assets_base_url)}).')
            import traceback
            logger.error(traceback.format_exc())
#TABLE#

logger.info('Script finished.')
if globals().get('total_bundle_count'):
    logger.info(
        f'Bundle: {total_bundle_count} total, {downloaded_bundle_count} downloaded, {skipped_bundle_count} skipped.')
if globals().get('total_media_count'):
    logger.info(
        f'Media: {total_media_count} total, {downloaded_media_count} downloaded, {skipped_media_count} skipped.')
if globals().get('total_table_count'):
    logger.info(
        f'table: {total_table_count} total, {downloaded_table_count} downloaded, {skipped_table_count} skipped.')
if globals().get('total_patch_bundle'):
    logger.info(
        f'PatchPack: {total_patch_bundle} total, {downloaded_patch_bundle} downloaded, {skipped_patch_bundle} skipped.')   
    
def main_menu():
    while True:
        print("\n=== Blue Archive JP Downloader Menu ===")
        print("1. Download Android Bundles")
        print("2. Download PatchPack (zip + bundles)")        
        print("3. Download Media Files")
        print("4. Download TABLE Files")
        print("5. Download All")
        print("6. Exit")

        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            result = process_android_bundles()
            if result:
                total, downloaded, skipped = result
                logger.info(f'Bundle: {total} total, {downloaded} downloaded, {skipped} skipped.')
        elif choice == "2":
            result = process_patchpack()
            if result:
                total, downloaded, skipped = result
                logger.info(f'PatchPack: {total} total, {downloaded} downloaded, {skipped} skipped.')
        elif choice == "3":
            result = process_media()
            if result:
                total, downloaded, skipped = result
                logger.info(f'Media: {total} total, {downloaded} downloaded, {skipped} skipped.')
        elif choice == "4":
            result = process_table()
            if result:
                total, downloaded, skipped = result
                logger.info(f'TABLE: {total} total, {downloaded} downloaded, {skipped} skipped.')
        elif choice == "5":
            b = process_android_bundles() or (0,0,0)
            p = process_patchpack() or (0,0,0)
            m = process_media() or (0,0,0)
            t = process_table() or (0,0,0)
            logger.info(f'[ALL] Bundles: {b[0]}, PatchPack: {p[0]}, Media: {m[0]}, TABLE: {m[0]}')
        elif choice == "6":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
