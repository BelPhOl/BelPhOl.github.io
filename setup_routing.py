#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup strong URL routing for alumni profiles
Creates short, memorable URLs like /ipho/melnichenka
"""

import json
import re
from pathlib import Path

class URLRouter:
    def __init__(self):
        self.load_alumni_data()
        
    def load_alumni_data(self):
        """Load alumni data from JSON file"""
        with open('data/alumni.json', 'r', encoding='utf-8') as f:
            self.alumni_data = json.load(f)
        print(f"Loaded {len(self.alumni_data)} alumni records")
        
    def sanitize_filename(self, name):
        """Create a URL-friendly filename from alumni name"""
        if isinstance(name, dict):
            english_name = name.get('englishName', '')
            if english_name:
                clean_name = english_name.lower()
            else:
                clean_name = name.get('name', '').lower()
        else:
            clean_name = str(name).lower()
            
        # Remove special characters and replace spaces with hyphens
        clean_name = re.sub(r'[^\w\s-]', '', clean_name)
        clean_name = re.sub(r'[-\s]+', '-', clean_name)
        return clean_name.strip('-')
        
    def create_htaccess(self):
        """Create .htaccess file for Apache URL rewriting"""
        htaccess_content = """# Alumni Profile URL Rewriting
RewriteEngine On

# Force HTTPS
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Remove .html extension from URLs
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^([^\.]+)$ $1.html [NC,L]

# IPhO Alumni Profile Routes
"""
        
        for alumni in self.alumni_data:
            safe_name = self.sanitize_filename(alumni.get('englishName') or alumni['name'])
            
            # Create short URL routes
            htaccess_content += f"RewriteRule ^ipho/{safe_name}/?$ /profiles/ipho/{safe_name}.html [L,R=301]\n"
            htaccess_content += f"RewriteRule ^ipho/{safe_name}/en/?$ /profiles/ipho/{safe_name}-en.html [L,R=301]\n"
            htaccess_content += f"RewriteRule ^ipho/{safe_name}/ru/?$ /profiles/ipho/{safe_name}-ru.html [L,R=301]\n"
            
            # Special route for Melnichenka (featured alumni)
            if 'melnichenka' in safe_name.lower():
                htaccess_content += f"RewriteRule ^melnichenka/?$ /profiles/ipho/{safe_name}.html [L,R=301]\n"
                htaccess_content += f"RewriteRule ^featured/?$ /profiles/ipho/{safe_name}.html [L,R=301]\n"
        
        htaccess_content += """
# Alumni index routes
RewriteRule ^ipho/?$ /alumni.html [L,R=301]
RewriteRule ^alumni/?$ /alumni.html [L,R=301]

# Error pages
ErrorDocument 404 /404.html

# Cache control
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType text/css "access plus 1 year"
    ExpiresByType application/javascript "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/svg+xml "access plus 1 year"
</IfModule>

# Gzip compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/plain
    AddOutputFilterByType DEFLATE text/html
    AddOutputFilterByType DEFLATE text/xml
    AddOutputFilterByType DEFLATE text/css
    AddOutputFilterByType DEFLATE application/xml
    AddOutputFilterByType DEFLATE application/xhtml+xml
    AddOutputFilterByType DEFLATE application/rss+xml
    AddOutputFilterByType DEFLATE application/javascript
    AddOutputFilterByType DEFLATE application/x-javascript
</IfModule>
"""
        
        with open('.htaccess', 'w', encoding='utf-8') as f:
            f.write(htaccess_content)
        
        print("Created .htaccess file with URL rewriting rules")
        
    def create_nginx_config(self):
        """Create nginx configuration for URL rewriting"""
        nginx_content = """# Alumni Profile URL Rewriting for Nginx
server {
    listen 80;
    server_name belpho.by www.belpho.by;
    
    # Force HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name belpho.by www.belpho.by;
    
    # SSL configuration (add your SSL certificate paths)
    # ssl_certificate /path/to/certificate.crt;
    # ssl_certificate_key /path/to/private.key;
    
    root /var/www/belpho.by;
    index index.html;
    
    # Remove .html extension
    location / {
        try_files $uri $uri.html $uri/ =404;
    }
    
    # IPhO Alumni Profile Routes
"""
        
        for alumni in self.alumni_data:
            safe_name = self.sanitize_filename(alumni.get('englishName') or alumni['name'])
            
            nginx_content += f"""    location /ipho/{safe_name} {{
        return 301 /profiles/ipho/{safe_name}.html;
    }}
    
    location /ipho/{safe_name}/en {{
        return 301 /profiles/ipho/{safe_name}-en.html;
    }}
    
    location /ipho/{safe_name}/ru {{
        return 301 /profiles/ipho/{safe_name}-ru.html;
    }}
    
"""
            
            # Special routes for Melnichenka
            if 'melnichenka' in safe_name.lower():
                nginx_content += f"""    location /melnichenka {{
        return 301 /profiles/ipho/{safe_name}.html;
    }}
    
    location /featured {{
        return 301 /profiles/ipho/{safe_name}.html;
    }}
    
"""
        
        nginx_content += """    # Alumni index routes
    location /ipho {
        return 301 /alumni.html;
    }
    
    location /alumni {
        return 301 /alumni.html;
    }
    
    # Static file caching
    location ~* \.(css|js|png|jpg|jpeg|gif|svg|ico)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}
"""
        
        with open('nginx.conf', 'w', encoding='utf-8') as f:
            f.write(nginx_content)
        
        print("Created nginx.conf file with URL rewriting rules")
        
    def create_url_map(self):
        """Create a URL mapping file for reference"""
        url_map = {
            "description": "URL mapping for BelPhO Alumni profiles",
            "base_url": "https://belpho.by",
            "routes": {}
        }
        
        for alumni in self.alumni_data:
            safe_name = self.sanitize_filename(alumni.get('englishName') or alumni['name'])
            display_name = alumni.get('englishName') or alumni['name']
            
            url_map["routes"][safe_name] = {
                "name": display_name,
                "year": alumni.get('year'),
                "award": alumni.get('award'),
                "urls": {
                    "main": f"/ipho/{safe_name}",
                    "english": f"/ipho/{safe_name}/en",
                    "russian": f"/ipho/{safe_name}/ru"
                },
                "files": {
                    "main": f"/profiles/ipho/{safe_name}.html",
                    "english": f"/profiles/ipho/{safe_name}-en.html",
                    "russian": f"/profiles/ipho/{safe_name}-ru.html"
                }
            }
            
            # Add special routes for featured alumni
            if 'melnichenka' in safe_name.lower():
                url_map["routes"][safe_name]["special_urls"] = [
                    "/melnichenka",
                    "/featured"
                ]
                url_map["featured_alumni"] = safe_name
        
        # Create data directory if it doesn't exist
        Path('data').mkdir(exist_ok=True)
        
        with open('data/url_map.json', 'w', encoding='utf-8') as f:
            json.dump(url_map, f, ensure_ascii=False, indent=2)
        
        print("Created URL mapping file: data/url_map.json")
        
    def create_sitemap(self):
        """Create XML sitemap for search engines"""
        sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    
    <!-- Main pages -->
    <url>
        <loc>https://belpho.by/</loc>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    
    <url>
        <loc>https://belpho.by/alumni</loc>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
    
    <url>
        <loc>https://belpho.by/ipho</loc>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
    
    <!-- Alumni profiles -->
"""
        
        for alumni in self.alumni_data:
            safe_name = self.sanitize_filename(alumni.get('englishName') or alumni['name'])
            
            # Main profile URL
            sitemap_content += f"""    <url>
        <loc>https://belpho.by/ipho/{safe_name}</loc>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    
    <url>
        <loc>https://belpho.by/ipho/{safe_name}/en</loc>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
    
    <url>
        <loc>https://belpho.by/ipho/{safe_name}/ru</loc>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
    
"""
            
            # Higher priority for featured alumni
            if 'melnichenka' in safe_name.lower():
                sitemap_content += f"""    <url>
        <loc>https://belpho.by/melnichenka</loc>
        <changefreq>weekly</changefreq>
        <priority>0.95</priority>
    </url>
    
    <url>
        <loc>https://belpho.by/featured</loc>
        <changefreq>weekly</changefreq>
        <priority>0.95</priority>
    </url>
    
"""
        
        sitemap_content += "</urlset>"
        
        with open('sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        
        print("Created sitemap.xml for search engines")
        
    def create_robots_txt(self):
        """Create robots.txt file"""
        robots_content = """User-agent: *
Allow: /

# Sitemap location
Sitemap: https://belpho.by/sitemap.xml

# Crawl delay (be respectful)
Crawl-delay: 1

# Disallow temporary files
Disallow: /temp/
Disallow: /*.tmp
Disallow: /*.bak

# Allow all profile pages
Allow: /ipho/
Allow: /profiles/
"""
        
        with open('robots.txt', 'w', encoding='utf-8') as f:
            f.write(robots_content)
        
        print("Created robots.txt file")
        
    def setup_all_routing(self):
        """Setup all routing configurations"""
        print("Setting up URL routing system...")
        
        self.create_htaccess()
        self.create_nginx_config()
        self.create_url_map()
        self.create_sitemap()
        self.create_robots_txt()
        
        print("\n✅ URL routing system setup complete!")
        print("\nStrong URLs created:")
        
        # Show some examples
        examples = [
            ("Main alumni page", "https://belpho.by/ipho/"),
            ("Featured alumni (Melnichenka)", "https://belpho.by/melnichenka"),
            ("Specific profile", "https://belpho.by/ipho/aliaksandr-melnichenka"),
            ("English version", "https://belpho.by/ipho/aliaksandr-melnichenka/en"),
            ("Russian version", "https://belpho.by/ipho/aliaksandr-melnichenka/ru")
        ]
        
        for desc, url in examples:
            print(f"  {desc}: {url}")

def main():
    router = URLRouter()
    router.setup_all_routing()

if __name__ == '__main__':
    main()
