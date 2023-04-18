#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkswr.v2.region.swr_region import SwrRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkswr.v2 import *
import sys
import yaml
import os

swr_dict = {

}

def args_handle(args):
    swr_dict["ak"] = args[1]
    swr_dict["sk"] = args[2]
    swr_dict["namespace"] = args[3]
    swr_dict["repository"] = args[4].replace("/", "$") + "-test"
    swr_dict["repository-src"] = args[4].replace("/", "$")

def latest_image_tag_get():

    credentials = BasicCredentials(swr_dict["ak"], swr_dict["sk"]) \

    client = SwrClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(SwrRegion.value_of("cn-north-4")) \
        .build()

    try:
        request = ListRepositoryTagsRequest()
        request.namespace = swr_dict["namespace"]
        request.repository = swr_dict["repository"]
        request.limit = "1"
        request.offset = "0"
        request.order_column = "updated_at"
        request.order_type = "desc"
        response = client.list_repository_tags(request)
        read_info = yaml.safe_load(str(response))
        return read_info["body"][0]["path"]
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)

def check_tag_exist(image_tag):
    print(f"check image tag: {image_tag}")

    credentials = BasicCredentials(swr_dict["ak"], swr_dict["sk"]) \

    client = SwrClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(SwrRegion.value_of("cn-north-4")) \
        .build()

    try:
        request = ListRepositoryTagsRequest()
        request.namespace = swr_dict["namespace"]
        request.repository = swr_dict["repository-src"]
        response = client.list_repository_tags(request)
        read_info = yaml.safe_load(str(response))
        for item in read_info["body"]:
            if image_tag in item["Tag"]:
                return True
        return False
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)

def update_tag_to_kustomization(tag):
    dst_image = "swr.cn-north-4.myhuaweicloud.com/" + swr_dict["namespace"] + "/" + swr_dict["repository-src"].replace("$", "/")
    update_check = False
    with open("kustomization.yaml", "r") as sf:
        Kustomization = list(yaml.load_all(sf, Loader=yaml.SafeLoader))
        for item in Kustomization:
            if item["kind"] == "Kustomization":
                for img in item["images"]:
                    if img["name"] == dst_image:
                        img["newTag"] = tag
                        update_check = True
                        print("updating tag!!!")
        with open("kustomization.yaml", "w") as df:
            yaml.dump_all(Kustomization, df, default_flow_style=False)
        if update_check == True:
            print("success update image")
        else:
            print("update image failed")

if __name__ == "__main__":
    args_handle(sys.argv)
    image = latest_image_tag_get()
    image_tag = image.split(":")[1]
    if check_tag_exist(image_tag):
        print("image tag exist")
        update_tag_to_kustomization(image_tag)
    else:
        print("image tag not exist in prod")