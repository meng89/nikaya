import selenium.webdriver
#from selenium import webdriver
import time

# 启动 Firefox WebDriver


options = selenium.webdriver.FirefoxOptions()
options.add_argument("--headless")
#options.add_argument("--window-size=1600,2560")

driver = selenium.webdriver.Firefox(options=options) # 确保你已安装 geckodriver
#driver.set_window_position(0,0)
driver.
driver.set_window_size(1600,2560, windowHandle='current')
driver.get("file:///mnt/data/projects/nikaya/resource/hyndzj/cover/經分別_简_2025年12月09日.xhtml")
#time.sleep(2) # 等待页面加载

# 截屏并保存文件
driver.save_screenshot("google_screenshot.png")
# 或者使用 get_screenshot_as_file(filename)
# driver.get_screenshot_as_file("google_screenshot_file.png")

print("截图已保存为 google_screenshot.png")
#driver.quit()