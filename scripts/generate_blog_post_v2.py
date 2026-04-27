#!/usr/bin/env python3
import os, sys, json, datetime, re, random
from pathlib import Path
from openai import OpenAI
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent.absolute()
BLOG_DIR = PROJECT_ROOT / "blog"
POSTS_DIR = BLOG_DIR / "posts"
IMAGES_DIR = BLOG_DIR / "images"
CONFIG_FILE = SCRIPT_DIR / "blog_config.json"
POSTS_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY: sys.exit(1)
client = OpenAI(api_key=OPENAI_API_KEY)
def load_config():
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f: return json.load(f)
def select_topic(config): return random.choice(config['blog_topics'])
def generate_post_content(topic, config):
    prompt = f"Você é um advogado. Gere um artigo em Markdown sobre {topic['title']} para o blog do Gabriel Corrêa. Use ## para subtítulos, inclua FAQ e CTA para WhatsApp (47) 99675-6766."
    response = client.chat.completions.create(model=config['generation_settings']['model'], messages=[{"role": "system", "content": prompt}], temperature=0.7)
    return response.choices[0].message.content
def extract_metadata(content, topic):
    slug = re.sub(r'[^a-z0-9]+', '-', topic['title'].lower()).strip('-')
    return {'title': topic['title'], 'excerpt': content[:200], 'slug': slug, 'keywords': topic['keywords'], 'category': topic['category']}
def create_blog_post(content, metadata, config):
    front_matter = f"---\ntitle: \"{metadata['title']}\"\ndate: {datetime.datetime.now().isoformat()}\nauthor: \"Advogado Gabriel Corrêa\"\ncategories: [\"{metadata['category']}\"]\ntags: {json.dumps(metadata['keywords'])}\nimage: \"/site_escritorio/blog/images/{metadata['slug']}.jpg\"\nexcerpt: \"{metadata['excerpt']}\"\n---\n\n"
    filename = POSTS_DIR / f"{metadata['slug']}.md"
    with open(filename, 'w', encoding='utf-8') as f: f.write(front_matter + content)
    return {'title': metadata['title'], 'slug': metadata['slug'], 'url': f"/site_escritorio/blog/posts/{metadata['slug']}.html", 'date': datetime.datetime.now().isoformat(), 'author': "Advogado Gabriel Corrêa", 'excerpt': metadata['excerpt'], 'image': f"/site_escritorio/blog/images/{metadata['slug']}.jpg", 'tags': metadata['keywords'], 'categories': [metadata['category']]}
def update_posts_index(post_metadata):
    index_file = POSTS_DIR / "index.json"
    posts = json.load(open(index_file, 'r')) if index_file.exists() else []
    posts = [p for p in posts if p['slug'] != post_metadata['slug']]
    posts.append(post_metadata)
    posts.sort(key=lambda x: x['date'], reverse=True)
    json.dump(posts, open(index_file, 'w'), ensure_ascii=False, indent=2)
def main():
    config = load_config()
    topic = select_topic(config)
    content = generate_post_content(topic, config)
    metadata = extract_metadata(content, topic)
    post_metadata = create_blog_post(content, metadata, config)
    update_posts_index(post_metadata)
if __name__ == "__main__": main()
