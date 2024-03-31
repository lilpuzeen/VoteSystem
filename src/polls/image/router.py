from uuid import uuid4

from fastapi import APIRouter, Depends, UploadFile, HTTPException, Response, status
from loguru import logger

import boto3
from botocore.exceptions import ClientError

import pylibmagic
import magic

from src.polls.utils import get_current_active_user


router_images = APIRouter(
	prefix="/images",
	tags=["Images"]
)


KB = 1024
MB = 1024 * KB


SUPPORTED_FILE_TYPES = {
    'image/png': 'png',
    'image/jpeg': 'jpg',
    'application/pdf': 'pdf'
}

AWS_BUCKET = 'votesystem'

s3 = boto3.resource('s3')
bucket = s3.Bucket(AWS_BUCKET)


async def s3_upload(contents: bytes, key: str):
    logger.info(f'Uploading {key} to s3')
    bucket.put_object(Key=key, Body=contents)


async def s3_download(key: str):
    try:
        return s3.Object(bucket_name=AWS_BUCKET, key=key).get()['Body'].read()
    except ClientError as err:
        logger.error(str(err))


@router_images.post('', dependencies=[Depends(get_current_active_user)])
async def upload(file: UploadFile):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No file found!!'
        )

    contents = await file.read()
    size = len(contents)

    if not 0 < size <= 1 * MB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Supported file size is 0 - 1 MB'
        )

    file_type = magic.from_buffer(buffer=contents, mime=True)
    if file_type not in SUPPORTED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Unsupported file type: {file_type}. Supported types are {SUPPORTED_FILE_TYPES}'
        )
    file_name = f'{uuid4()}.{SUPPORTED_FILE_TYPES[file_type]}'
    await s3_upload(contents=contents, key=file_name)
    return {'file_name': file_name}


@router_images.get('', dependencies=[Depends(get_current_active_user)])
async def download(file_name: str | None = None):
    if not file_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No file name provided'
        )

    contents = await s3_download(key=file_name)
    return Response(
        content=contents,
        headers={
            'Content-Disposition': f'attachment;filename={file_name}',
            'Content-Type': 'application/octet-stream',
        }
    )