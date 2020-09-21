import os

from django.core.exceptions import ValidationError
import magic


def validate_file_type(file, valid_mime_types, valid_file_extensions):
    file_mime_type = magic.from_buffer(file.read(1024), mime=True)

    if file_mime_type not in valid_mime_types:
        raise ValidationError('Unsupported file type.')

    valid_file_extensions = ['.pdf']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension.')


def validate_is_pdf(file):
    return validate_file_type(
        file,
        valid_mime_types=['application/pdf'],
        valid_file_extensions=['.pdf'],
    )
