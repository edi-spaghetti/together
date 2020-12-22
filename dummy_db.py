import hashlib

db = {
    'user': {
        'admin@admin.com': {
            'hashed_password': hashlib.md5(b'admin').hexdigest(),
        },
        'user@user.com': {
            'hashed_password': hashlib.md5(b'password123').hexdigest(),
        }
    }
}