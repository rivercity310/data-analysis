from sel_options import get_chrome_driver
from selenium.webdriver.common.by import By


def crawling_youtube_main():
    driver = get_chrome_driver(headless=True)
    url = "https://youtube.com"
    driver.get(url)

    try:
        meta_elems = driver.find_elements(by=By.ID, value="meta")

        max_video_count = 0
        max_video_title = ""

        for meta_elem in meta_elems:
            try:
                video_title_elem = meta_elem.find_element(by=By.ID, value="video-title-link")
                meta_data_line_elem = meta_elem.find_element(by=By.ID, value="metadata-line")
                click_count = meta_data_line_elem.find_elements(by=By.TAG_NAME, value="span")[0].text[4:-1]

                if click_count == "" or not click_count.endswith("만"):
                    print(f"예외 발생!!!! click_count = {click_count}")
                    raise Exception

                video_title = video_title_elem.find_element(by=By.ID, value="title").text
                click_count = int(float(click_count[:-1]) * 10000)

                if click_count > max_video_count:
                    max_video_count = click_count
                    max_video_title = video_title

                print(max_video_title)
                print(max_video_count)

            except Exception as e:
                continue

        print(f"가장 많이 시청한 비디오: {max_video_title}")
        print(f"조회수: {max_video_count}")

    except Exception as e:
        import logging.config

        logging.config.fileConfig("../../logging.conf")
        logger = logging.getLogger(__name__)
        logger.critical(e)

    finally:
        driver.delete_network_conditions()
        driver.delete_all_cookies()
        driver.quit()


if __name__ == "__main__":
    crawling_youtube_main()
