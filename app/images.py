import os
from pathlib import Path
from dotenv import load_dotenv
from imagekitio import ImageKit

env_path = Path(__file__).resolve().parent.parent / '.env'

load_dotenv(dotenv_path=env_path)


public_key = os.getenv("IMAGEKIT_PUBLIC_KEY")
private_key = os.getenv("IMAGEKIT_PRIVATE_KEY")
url_endpoint = os.getenv("IMAGEKIT_URL")

if not all([public_key, private_key, url_endpoint]):
    raise ValueError("Missing ImageKit credentials. Check your .env file location!")

imagekit = ImageKit(
    private_key=private_key,
)