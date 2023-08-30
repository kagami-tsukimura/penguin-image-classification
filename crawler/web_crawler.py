import argparse
import base64
import logging
import os
from enum import Enum

import yaml
from icrawler import ImageDownloader
from icrawler.builtin import BingImageCrawler, GoogleImageCrawler
from six.moves.urllib.parse import urlparse  # noqa
from tqdm import tqdm


class SearchEngine(Enum):
    BING = "bing"
    GOOGLE = "google"


class Base64NameDownloader(ImageDownloader):
    def get_filename(self, task, default_ext):
        """Base64 encodes the URL path and generates a file name.

        Args:
            task (dict): A dictionary with a "file_url" key.
            default_ext (str): A default extension to use.

        Returns:
            str: The generated filename.
        """
        url_path = urlparse(task["file_url"])[2]
        # If the image contains an extension, get it.
        if "." in url_path:
            extension = url_path.split(".")[-1]
            if extension.lower() not in [
                "jpg",
                "jpeg",
                "png",
            ]:
                extension = default_ext
        else:
            extension = default_ext
        # Encoding the URL to the file name.
        filename = base64.b64encode(url_path.encode()).decode()
        return f"{filename}.{extension}"


def setting_args():
    """Parse command line arguments for the image crawler.

    Returns:
        Namespace: Containing parsed arguments.
    """
    parser = argparse.ArgumentParser(description="crawling images")
    parser.add_argument("-o", "--output", default="./images", type=str)
    parser.add_argument("-n", "--N", default=1000, type=int)
    parser.add_argument("-e", "--engine", default="google", type=str)
    return parser.parse_args()


def setup_logger():
    """Set up logger."""

    LOG_DIR = "./logs"
    FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    os.makedirs(LOG_DIR, exist_ok=True)

    log_file = os.path.join(LOG_DIR, "web_crawler.log")
    logging.basicConfig(level=logging.CRITICAL)
    formatter = logging.Formatter(FORMAT)
    handler = logging.FileHandler(log_file, mode="w")
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger = logging.getLogger("icrawler")
    logger.addHandler(handler)


def get_crawler(args, dir_name):
    """Returns a crawler object based on the search engine in the arguments.

    Args:
        args (argparse.Namespace): Containing parsed arguments.
        dir_name (str): The output directory for downloaded images.

    Returns:
        A crawler object for the selected search engine.
    """

    ROOT = "root_dir"
    if args.engine == SearchEngine.BING.value:
        crawler = BingImageCrawler(
            downloader_cls=Base64NameDownloader, storage={ROOT: dir_name}
        )
    elif args.engine == SearchEngine.GOOGLE.value:
        crawler = GoogleImageCrawler(storage={ROOT: dir_name})
    return crawler


def main(args):
    """Main processing.

    Args:
        args (argparse.Namespace): Containing parsed arguments.
    """

    setup_logger()
    print("Start crawling images...")

    SEARCH_FILE = "configs/search.yaml"
    SEARCH_WORD = "search_word"
    with open(SEARCH_FILE) as f:
        yml = yaml.safe_load(f)

    search_words = yml[SEARCH_WORD]

    for search_word in tqdm(search_words):
        output_dir = os.path.join(args.output, search_word)
        # If there is no output directory, create it.
        os.makedirs(output_dir, exist_ok=True)
        # Start crawling images.
        crawler = get_crawler(args, output_dir)
        crawler.crawl(keyword=search_word, max_num=args.N)
    print("Finish crawling images!")


if __name__ == "__main__":
    args = setting_args()
    main(args)
