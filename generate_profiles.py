#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate individual profile pages for each alumni
Creates modern, credible profiles optimized for MIT admissions
"""

import json
import re
from pathlib import Path
from urllib.parse import quote
from datetime import datetime

class ProfileGenerator:
    def __init__(self):
        self.load_alumni_data()
        self.create_directories()
        
    def load_alumni_data(self):
        """Load alumni data from JSON file"""
        with open('data/alumni.json', 'r', encoding='utf-8') as f:
            self.alumni_data = json.load(f)
        print(f"Loaded {len(self.alumni_data)} alumni records")
        
    def create_directories(self):
        """Create necessary directories for profile pages"""
        directories = [
            'profiles',
            'profiles/ipho',
            'profiles/css',
            'profiles/js'
        ]
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            
    def sanitize_filename(self, name):
        """Create a URL-friendly filename from alumni name"""
        # Use English name if available, otherwise transliterate Russian name
        if hasattr(name, 'get'):
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
        
    def get_medal_emoji(self, award):
        """Get emoji for medal type"""
        medal_map = {
            'gold': '🥇',
            'silver': '🥈', 
            'bronze': '🥉',
            'mention': '📜'
        }
        return medal_map.get(award, '🏆')
        
    def format_university_with_emblem(self, university):
        """Add emblems for prestigious universities"""
        if not university or university == '—':
            return university
            
        emblems = {
            'MIT': '🏛️',
            'Harvard': '🏛️',
            'Stanford': '🏛️',
            'Cambridge': '🏛️',
            'Oxford': '🏛️',
            'Caltech': '🔬',
            'Princeton': '🏛️',
            'Yale': '🏛️',
            'Berkeley': '🌟',
            'ETH Zurich': '🏔️',
            'Berea College': '⭐',
            'Skoltech': '🚀',
            'МФТИ': '🚀',
            'МГУ': '🏛️',
            'ИТМО': '💻'
        }
        
        for key, emblem in emblems.items():
            if key in university:
                return f"{emblem} {university}"
        return university
        
    def generate_profile_html(self, alumni, language='ru'):
        """Generate HTML for individual alumni profile"""
        
        # Determine names based on language
        if language == 'en':
            display_name = alumni.get('englishName') or alumni['name']
            page_title = f"{display_name} - IPhO Alumni Profile"
        else:
            display_name = alumni['name']
            page_title = f"{display_name} - Профиль выпускника IPhO"
            
        # Create safe filename
        safe_name = self.sanitize_filename(alumni.get('englishName') or alumni['name'])
        
        # Get medal emoji
        medal_emoji = self.get_medal_emoji(alumni.get('award', 'mention'))
        
        # Format university
        university = self.format_university_with_emblem(alumni.get('university', ''))
        
        # Generate achievement highlights
        achievements = alumni.get('achievements', [])
        if language == 'en':
            achievement_title = "Key Achievements"
        else:
            achievement_title = "Ключевые достижения"
            
        # Special highlighting for Melnichenka
        is_melnichenka = 'melnichenka' in safe_name.lower()
        
        # Generate structured data for SEO
        structured_data = {
            "@context": "https://schema.org",
            "@type": "Person",
            "name": display_name,
            "alumniOf": alumni.get('school', ''),
            "nationality": "Belarusian",
            "award": alumni.get('award'),
            "description": f"International Physics Olympiad participant from Belarus ({alumni.get('year')})"
        }
        
        if alumni.get('university'):
            structured_data["affiliation"] = alumni['university']
            
        html_content = f"""<!DOCTYPE html>
<html lang="{language}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    
    <!-- SEO Meta Tags -->
    <meta name="description" content="Profile of {display_name}, International Physics Olympiad participant from Belarus. Academic achievements, research, and career highlights.">
    <meta name="keywords" content="Physics Olympiad, Belarus, {display_name}, IPhO, academic excellence, STEM education">
    <meta name="author" content="BelPhO Alumni Network">
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="{page_title}">
    <meta property="og:description" content="International Physics Olympiad Alumni Profile - {display_name}">
    <meta property="og:type" content="profile">
    <meta property="og:url" content="https://belpho.by/profiles/ipho/{safe_name}">
    {"<meta property='og:image' content='https://belpho.by/" + alumni.get('profileImage', 'img/logo.png') + "'>" if alumni.get('profileImage') else ""}
    
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{page_title}">
    <meta name="twitter:description" content="International Physics Olympiad Alumni Profile">
    
    <!-- Structured Data -->
    <script type="application/ld+json">
    {json.dumps(structured_data, ensure_ascii=False, indent=2)}
    </script>
    
    <!-- Stylesheets -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="../css/profile-styles.css" rel="stylesheet">
    
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    {"<!-- Special styling for featured profile -->" if is_melnichenka else ""}
    {"<link href='../css/featured-profile.css' rel='stylesheet'>" if is_melnichenka else ""}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
        <div class="container">
            <a class="navbar-brand d-flex align-items-center" href="../../index.html">
                <img src="../../img/logo.png" alt="BelPhO" height="32" class="me-2">
                <span class="fw-bold">BelPhO</span>
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="../../index.html">{"Home" if language == 'en' else "Главная"}</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="../../alumni.html">{"Alumni" if language == 'en' else "Выпускники"}</a>
                    </li>
                </ul>
                
                <div class="navbar-nav">
                    {"<a class='nav-link' href='" + safe_name + "-ru.html'>RU</a>" if language == 'en' else "<a class='nav-link' href='" + safe_name + "-en.html'>EN</a>"}
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section {"featured-hero" if is_melnichenka else ""}">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-4 text-center mb-4 mb-lg-0">
                    {"<div class='profile-image-container featured'>" if is_melnichenka else "<div class='profile-image-container'>"}
                        {f"<img src='../../{alumni['profileImage']}' alt='{display_name}' class='profile-image'>" if alumni.get('profileImage') else f"<div class='profile-placeholder'><i class='fas fa-user'></i></div>"}
                        <div class="medal-overlay">
                            <span class="medal">{medal_emoji}</span>
                        </div>
                    </div>
                </div>
                
                <div class="col-lg-8">
                    <div class="hero-content">
                        {"<div class='featured-badge mb-3'>" if is_melnichenka else ""}
                            {"<i class='fas fa-star'></i> Featured Alumni" if is_melnichenka and language == 'en' else ""}
                            {"<i class='fas fa-star'></i> Рекомендуемый выпускник" if is_melnichenka and language == 'ru' else ""}
                        {"</div>" if is_melnichenka else ""}
                        
                        <h1 class="hero-title">{display_name}</h1>
                        
                        <div class="hero-subtitle">
                            <span class="year-badge">{alumni.get('year', '')}</span>
                            <span class="award-badge {alumni.get('award', 'mention')}">{alumni.get('award', '').title()}</span>
                        </div>
                        
                        <p class="hero-description">
                            {alumni.get('ipho', '')}
                        </p>
                        
                        {f"<p class='current-status'><strong>{'Current Status' if language == 'en' else 'Текущий статус'}:</strong> {alumni.get('currentStatus', alumni.get('profession', ''))}</p>" if alumni.get('currentStatus') or alumni.get('profession') else ""}
                        
                        {f"<p class='university'><strong>{'University' if language == 'en' else 'Университет'}:</strong> {university}</p>" if university and university != '—' else ""}
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Main Content -->
    <main class="main-content">
        <div class="container">
            <div class="row">
                <!-- Left Column - Details -->
                <div class="col-lg-8">
                    <!-- Competition Results -->
                    <div class="content-card">
                        <h2 class="section-title">
                            <i class="fas fa-trophy text-warning"></i>
                            {"Competition Results" if language == 'en' else "Результаты соревнований"}
                        </h2>
                        
                        <div class="competition-stats">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="stat-item">
                                        <span class="stat-label">{"Competition" if language == 'en' else "Соревнование"}:</span>
                                        <span class="stat-value">{alumni.get('ipho', 'N/A')}</span>
                                    </div>
                                    {f"<div class='stat-item'><span class='stat-label'>{'Rank' if language == 'en' else 'Место'}:</span><span class='stat-value rank-{alumni.get('award', 'mention')}'>{alumni.get('rank', 'N/A')} / {alumni.get('totalContestants', 'N/A')}</span></div>" if alumni.get('rank') else ""}
                                </div>
                                <div class="col-md-6">
                                    {f"<div class='stat-item'><span class='stat-label'>{'Theory' if language == 'en' else 'Теория'}:</span><span class='stat-value'>{alumni.get('theory', 'N/A')}</span></div>" if alumni.get('theory') is not None else ""}
                                    {f"<div class='stat-item'><span class='stat-label'>{'Experiment' if language == 'en' else 'Эксперимент'}:</span><span class='stat-value'>{alumni.get('experiment', 'N/A')}</span></div>" if alumni.get('experiment') is not None else ""}
                                    {f"<div class='stat-item'><span class='stat-label'>{'Total Score' if language == 'en' else 'Общий балл'}:</span><span class='stat-value total-score'>{alumni.get('total', 'N/A')}</span></div>" if alumni.get('total') is not None else ""}
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Achievements -->
                    {f'''
                    <div class="content-card">
                        <h2 class="section-title">
                            <i class="fas fa-medal text-success"></i>
                            {achievement_title}
                        </h2>
                        
                        <div class="achievements-list">
                            {"".join([f"<div class='achievement-item {'featured-achievement' if is_melnichenka else ''}'><i class='fas fa-check-circle'></i><span>{achievement}</span></div>" for achievement in achievements])}
                        </div>
                    </div>
                    ''' if achievements else ""}

                    <!-- Research & Publications -->
                    {f'''
                    <div class="content-card">
                        <h2 class="section-title">
                            <i class="fas fa-microscope text-info"></i>
                            {"Research & Publications" if language == 'en' else "Исследования и публикации"}
                        </h2>
                        
                        {f"<p><strong>{'Research Area' if language == 'en' else 'Область исследований'}:</strong> {alumni.get('researchArea')}</p>" if alumni.get('researchArea') else ""}
                        {f"<p><strong>{'Publications' if language == 'en' else 'Публикации'}:</strong> {alumni.get('publications')}</p>" if alumni.get('publications') else ""}
                        {f"<p><strong>{'Impact Metrics' if language == 'en' else 'Показатели влияния'}:</strong> {alumni.get('impactMetrics')}</p>" if alumni.get('impactMetrics') else ""}
                    </div>
                    ''' if alumni.get('researchArea') or alumni.get('publications') or alumni.get('impactMetrics') else ""}
                </div>

                <!-- Right Column - Sidebar -->
                <div class="col-lg-4">
                    <!-- Quick Facts -->
                    <div class="sidebar-card">
                        <h3 class="sidebar-title">{"Quick Facts" if language == 'en' else "Краткая информация"}</h3>
                        
                        <div class="fact-list">
                            <div class="fact-item">
                                <span class="fact-label">{"School" if language == 'en' else "Школа"}:</span>
                                <span class="fact-value">{alumni.get('school', 'N/A')}</span>
                            </div>
                            
                            {f"<div class='fact-item'><span class='fact-label'>{'Teacher' if language == 'en' else 'Учитель'}:</span><span class='fact-value'>{alumni.get('teacher')}</span></div>" if alumni.get('teacher') else ""}
                            
                            <div class="fact-item">
                                <span class="fact-label">{"Year" if language == 'en' else "Год"}:</span>
                                <span class="fact-value">{alumni.get('year', 'N/A')}</span>
                            </div>
                            
                            <div class="fact-item">
                                <span class="fact-label">{"Award" if language == 'en' else "Награда"}:</span>
                                <span class="fact-value award-{alumni.get('award', 'mention')}">{medal_emoji} {alumni.get('award', 'N/A').title()}</span>
                            </div>
                            
                            {f"<div class='fact-item'><span class='fact-label'>{'Country' if language == 'en' else 'Страна'}:</span><span class='fact-value'>{alumni.get('country')}</span></div>" if alumni.get('country') else ""}
                        </div>
                    </div>

                    <!-- Social Links -->
                    {f'''
                    <div class="sidebar-card">
                        <h3 class="sidebar-title">{"Connect" if language == 'en' else "Связаться"}</h3>
                        
                        <div class="social-links">
                            {"".join([self.format_social_link(link) for link in alumni.get('socialLinks', [])])}
                        </div>
                    </div>
                    ''' if alumni.get('socialLinks') else ""}

                    <!-- Call to Action for Melnichenka -->
                    {f'''
                    <div class="sidebar-card featured-cta">
                        <h3 class="sidebar-title">
                            <i class="fas fa-graduation-cap"></i>
                            {"MIT Transfer Candidate" if language == 'en' else "Кандидат на перевод в MIT"}
                        </h3>
                        
                        <p class="cta-text">
                            {"Outstanding physics researcher and EdTech founder seeking transfer to MIT. Proven track record in astrophysics research and educational technology." if language == 'en' else "Выдающийся исследователь в области физики и основатель образовательных технологий, стремящийся к переводу в MIT. Доказанный опыт в астрофизических исследованиях и образовательных технологиях."}
                        </p>
                        
                        <div class="cta-stats">
                            <div class="cta-stat">
                                <span class="cta-number">135k+</span>
                                <span class="cta-label">{"Monthly Learners" if language == 'en' else "Пользователей в месяц"}</span>
                            </div>
                            <div class="cta-stat">
                                <span class="cta-number">3M+</span>
                                <span class="cta-label">{"Annual Pageviews" if language == 'en' else "Просмотров в год"}</span>
                            </div>
                        </div>
                    </div>
                    ''' if is_melnichenka else ""}
                </div>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <p>&copy; {datetime.now().year} BelPhO Alumni Network. All rights reserved.</p>
                </div>
                <div class="col-md-6 text-end">
                    <a href="mailto:aliaksandr@melnichenka.com" class="footer-link">
                        {"Contact" if language == 'en' else "Контакт"}
                    </a>
                </div>
            </div>
        </div>
    </footer>

    <!-- Scripts -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
    <script src="../js/profile-scripts.js"></script>
    
    <!-- Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'GA_MEASUREMENT_ID');
    </script>
</body>
</html>"""
        
        return html_content
        
    def format_social_link(self, link):
        """Format social media links with appropriate icons"""
        icons = {
            'github': 'fab fa-github',
            'linkedin': 'fab fa-linkedin',
            'twitter': 'fab fa-twitter',
            'instagram': 'fab fa-instagram',
            'telegram': 'fab fa-telegram',
            'researchgate': 'fab fa-researchgate',
            'other': 'fas fa-external-link-alt',
            'savchenko': 'fas fa-book'
        }
        
        icon = icons.get(link.get('type', 'other'), 'fas fa-link')
        name = link.get('name', link.get('type', 'Link').title())
        url = link.get('url', '#')
        
        return f'''
        <a href="{url}" class="social-link" target="_blank" rel="noopener noreferrer">
            <i class="{icon}"></i>
            <span>{name}</span>
        </a>
        '''
        
    def generate_all_profiles(self):
        """Generate profile pages for all alumni"""
        print("Generating profile pages...")
        
        generated_count = 0
        for alumni in self.alumni_data:
            try:
                # Create safe filename
                safe_name = self.sanitize_filename(alumni.get('englishName') or alumni['name'])
                
                # Generate Russian version
                html_ru = self.generate_profile_html(alumni, 'ru')
                ru_path = f"profiles/ipho/{safe_name}-ru.html"
                with open(ru_path, 'w', encoding='utf-8') as f:
                    f.write(html_ru)
                
                # Generate English version
                html_en = self.generate_profile_html(alumni, 'en')
                en_path = f"profiles/ipho/{safe_name}-en.html"
                with open(en_path, 'w', encoding='utf-8') as f:
                    f.write(html_en)
                
                # Create main profile redirect (defaults to English)
                main_path = f"profiles/ipho/{safe_name}.html"
                with open(main_path, 'w', encoding='utf-8') as f:
                    f.write(html_en)
                
                generated_count += 1
                
                if 'melnichenka' in safe_name.lower():
                    print(f"✨ Generated featured profile: {safe_name}")
                
            except Exception as e:
                print(f"Error generating profile for {alumni.get('name', 'Unknown')}: {e}")
                continue
        
        print(f"Generated {generated_count} profile pages")
        return generated_count

def main():
    generator = ProfileGenerator()
    generator.generate_all_profiles()
    print("Profile generation complete!")

if __name__ == '__main__':
    main()
