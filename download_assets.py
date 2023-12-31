from typing import Tuple
import requests
import logging
import os

# set current version from environ
current_version = os.environ.get('BA_JP_CURRENT_VERSION', None)
if not current_version:
    current_version = 'r63_fs4ara67b1oynubut5uj'

# set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# set up requests session
session = requests.Session()

# set up constants
BA_JP_BUNDLES_DIR = os.path.join(os.path.dirname(__file__), 'ba_jp_bundles')
BA_JP_MEDIA_DIR = os.path.join(os.path.dirname(__file__), 'ba_jp_media')
BA_JP_TABLE_DIR = os.path.join(os.path.dirname(__file__), 'ba_jp_table')
dirs = [BA_JP_BUNDLES_DIR, BA_JP_MEDIA_DIR, BA_JP_TABLE_DIR]

BA_JP_VERSION_METADATA_TEMPLATE = "https://yostar-serverinfo.bluearchiveyostar.com/{}.json"

BA_JP_ANDROID_BUNDLE_DOWNLOAD_INFO_TEMPLATE = '{}/Android/bundleDownloadInfo.json'
BA_JP_ANDROID_BUNDLE_BASEURL_TEMPLATE = '{}/Android/'
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
