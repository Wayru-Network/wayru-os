import os
import shutil
import json
import tarfile
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

BUILD_DIR = '../wayru-os' 
IMAGE_NAME_TEMPLATE = 'wayru-os-{}-{}.tar.gz'

# Azure configuration
AZURE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=firmwarebuilds;AccountKey=OFTa9OuDBRo1odhgVTPk1YXwPAfi8qNezM35XpyJH7lZFEmLbI7U2Etk+yDrAsXq/GO0I7mEUb6N+AStfMR64A==;EndpointSuffix=core.windows.net'
CONTAINER_NAME = 'wayru-os-builds'

def find_output_dir(base_dir):
    for root, dirs, files in os.walk(base_dir):
        if 'sha256sums' in files and any('sysupgrade' in file for file in files):
            return root
    return None

def get_sysupgrade_hash_and_file(output_dir):
    sha256sum_path = os.path.join(output_dir, 'sha256sums')
    sysupgrade_hash = None
    sysupgrade_file = None

    with open(sha256sum_path, 'r') as sha_file:
        lines = sha_file.readlines()

    for line in lines:
        if 'sysupgrade' in line:
            parts = line.split()
            sysupgrade_hash = parts[0]
            sysupgrade_file = parts[1].strip('*')
            break

    return sysupgrade_hash, sysupgrade_file

def get_codename_and_version():
    # Get codename from device.json
    device_json_path = os.path.join(BUILD_DIR, 'files', 'etc', 'wayru-os', 'device.json')
    with open(device_json_path) as json_file:
        device_info = json.load(json_file)
        codename = device_info['name']

    # Get version from VERSION
    version_file_path = os.path.join(BUILD_DIR, 'VERSION')
    with open(version_file_path) as version_file:
        version = version_file.read().strip()

    return codename, version

def package_files(output_dir, sysupgrade_hash, sysupgrade_file, codename, version):

    image_name = IMAGE_NAME_TEMPLATE.format(codename, version)
    image_path = os.path.join(output_dir, image_name)


    with tarfile.open(image_path, 'w:gz') as tar:
        #sysupgrade hash 
        temp_sha256sums_path = os.path.join(output_dir, 'temp_sha256sums')
        with open(temp_sha256sums_path, 'w') as sha_file:
            sha_file.write(f"{sysupgrade_hash}\n")

        tar.add(temp_sha256sums_path, arcname='sha256sums')

        # Add the sysupgrade file to the tar.gz
        sysupgrade_path = os.path.join(output_dir, sysupgrade_file)
        tar.add(sysupgrade_path, arcname=sysupgrade_file)

    os.remove(temp_sha256sums_path)

    return image_path

def upload_to_azure(file_path, connection_string, container_name, codename, version):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_folder_path = f'targets/{codename}/{version}/{os.path.basename(file_path)}'
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_folder_path)

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    print(f"Uploaded {file_path} to Azure Blob Storage at {blob_folder_path}")

def main():
    output_dir = find_output_dir(BUILD_DIR)
    if not output_dir:
        print("No se encontró el directorio de salida con los archivos requeridos.")
        return

    sysupgrade_hash, sysupgrade_file = get_sysupgrade_hash_and_file(output_dir)
    if not sysupgrade_hash or not sysupgrade_file:
        print("No se encontraron archivos sysupgrade en el directorio de salida.")
        return

    codename, version = get_codename_and_version()
    image_path = package_files(output_dir, sysupgrade_hash, sysupgrade_file, codename, version)
    print(f"Files packaged successfully: {image_path}")

    upload_to_azure(image_path, AZURE_CONNECTION_STRING, CONTAINER_NAME, codename, version)

if __name__ == '__main__':
    main()
