import requests
from bs4 import BeautifulSoup
from random import randint, choice

class Sargarmi:
	def __init__(self):
		pass

	def jok(self):
		page = randint(1, 1145)
		url = f"https://4jok.com/jok/59/{page}"
		headers = {'User-Agent': 'Mozilla/5.0'}

		try:
			response = requests.get(url, headers=headers, timeout=5)
			response.raise_for_status()
		except requests.RequestException as e:
			return f"❌ خطا در ارتباط با سرور: {e}"

		soup = BeautifulSoup(response.text, 'html.parser')
		posts = soup.find_all("div", class_="post")

		if posts:
			random_post = choice(posts)
			p = random_post.find("p")
			return p.get_text(strip=True).replace('\n', '‌') if p else "متنی پیدا نشد"
		else:
			return "هیچ جوکی پیدا نشد."

	def bio(self):
		url = 'https://taw-bio.ir/f/arc/text/all~1~all~bst.json'
		headers = {'User-Agent': 'Mozilla/5.0'}

		try:
			response = requests.get(url, headers=headers, timeout=5)
			response.raise_for_status()
			data = response.json()

			items = data.get("items", [])
			if not items:
				return "هیچ بیویی پیدا نشد"

			random_item = choice(items)
			raw_text = random_item.get("fa", "متنی موجود نیست")
			soup = BeautifulSoup(raw_text, 'html.parser')
			return soup.get_text(separator='\n').strip()

		except requests.RequestException as e:
			return f"❌ خطا در ارتباط با سرور: {e}"

		except Exception as e:
			return f"❌ خطا در پردازش داده: {e}"

	def dastan(self):
		page = randint(1, 164)
		url = f"https://4jok.com/text/63/{page}"
		headers = {'User-Agent': 'Mozilla/5.0'}
		response = requests.get(url, headers=headers)
		if response.status_code != 200:
			return "خطا در بارگذاری محتوا."
		soup = BeautifulSoup(response.text, 'html.parser')
		ps = soup.find_all("p")
		if not ps:
			return "هیچ متنی پیدا نشد."
		max_index = min(15, len(ps) - 1)
		return ps[randint(0, max_index)].get_text(strip=True)

	def dialog(self):
		page = randint(1, 107)
		url = f"https://4jok.com/text/81/{page}"
		headers = {'User-Agent': 'Mozilla/5.0'}
		response = requests.get(url, headers=headers)
		if response.status_code != 200:
			return "خطا در بارگذاری محتوا."
		soup = BeautifulSoup(response.text, 'html.parser')
		ps = soup.find_all("p")
		if not ps:
			return "هیچ متنی پیدا نشد."
		max_index = min(15, len(ps) - 1)
		return ps[randint(0, max_index)].get_text(strip=True)
	
	def alaky(self):
		page = randint(1, 37)
		url = f"https://4jok.com/jok/76/{page}"
		headers = {'User-Agent': 'Mozilla/5.0'}
		response = requests.get(url, headers=headers)
		if response.status_code != 200:
			return "خطا در بارگذاری محتوا."
		soup = BeautifulSoup(response.text, 'html.parser')
		ps = soup.find_all("p")
		if not ps:
			return "هیچ متنی پیدا نشد."
		max_index = min(15, len(ps) - 1)
		return ps[randint(0, max_index)].get_text(strip=True)
		
	def chalesh(self):
		try:
			result = requests.get("https://litebase.ir/code/servers/list-hagigat.json").text
			result = result.split("\n")
			read = list(result)
			read = choice(read)
			return read
		except Exception as e:
			print(e)
